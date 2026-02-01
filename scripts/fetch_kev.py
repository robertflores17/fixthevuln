#!/usr/bin/env python3
"""
Fetch CISA Known Exploited Vulnerabilities (KEV) catalog.
Auto-fills CVSS (from NVD), short description, and fix fields.

Usage:
  python scripts/fetch_kev.py              # Fetch new CVEs, auto-fill fields
  python scripts/fetch_kev.py --status     # Show status of all pending entries
  python scripts/fetch_kev.py --backfill   # Fill empty fields on existing entries
  python scripts/fetch_kev.py --clean      # Remove already-posted entries from pending
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import urllib.request
import urllib.error

# Configuration
CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
DATA_DIR = Path(__file__).parent.parent / "data"
KEV_FILE = DATA_DIR / "kev.json"
KEV_DATA_FILE = DATA_DIR / "kev-data.json"
PENDING_FILE = DATA_DIR / "pending_review.json"
SEEN_FILE = DATA_DIR / "seen_cves.json"

# Only fetch CVEs added in the last N days
LOOKBACK_DAYS = 14

# NVD rate limiting: 5 req/30s without key, 50 req/30s with key
NVD_API_KEY = os.environ.get('NVD_API_KEY', '')
NVD_DELAY = 0.6 if NVD_API_KEY else 6.0
_nvd_key_valid = None  # Cached result of API key validation


# ---------------------------------------------------------------------------
# NVD API: CVSS Lookup
# ---------------------------------------------------------------------------

def _validate_nvd_key():
    """Test if the NVD API key works. Returns True/False, caches result."""
    global _nvd_key_valid, NVD_DELAY
    if _nvd_key_valid is not None:
        return _nvd_key_valid

    if not NVD_API_KEY:
        _nvd_key_valid = False
        return False

    # Test with a well-known CVE
    url = f"{NVD_API_URL}?cveId=CVE-2021-44228"
    headers = {'User-Agent': 'FixTheVuln-KEV-Fetcher/1.0'}
    headers['apiKey'] = NVD_API_KEY
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            _nvd_key_valid = (resp.status == 200)
    except Exception:
        _nvd_key_valid = False

    if not _nvd_key_valid:
        print("  Note: NVD API key not accepted. Using rate-limited mode (6s between requests).")
        print("  The key may need email activation. Check your inbox from NVD/NIST.")
        NVD_DELAY = 6.0
    return _nvd_key_valid


def fetch_cvss_from_nvd(cve_id):
    """Fetch CVSS score from NVD API v2.0. Returns score as string or empty."""
    url = f"{NVD_API_URL}?cveId={cve_id}"
    headers = {'User-Agent': 'FixTheVuln-KEV-Fetcher/1.0'}
    if NVD_API_KEY and _validate_nvd_key():
        headers['apiKey'] = NVD_API_KEY

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))

        vulns = data.get('vulnerabilities', [])
        if not vulns:
            return ""

        cve_data = vulns[0].get('cve', {})
        metrics = cve_data.get('metrics', {})

        # Try CVSS v3.1, then v3.0, then v2.0
        for key in ('cvssMetricV31', 'cvssMetricV30'):
            metric_list = metrics.get(key, [])
            if metric_list:
                score = metric_list[0].get('cvssData', {}).get('baseScore')
                if score is not None:
                    return str(score)

        # Fallback to v2
        v2_list = metrics.get('cvssMetricV2', [])
        if v2_list:
            score = v2_list[0].get('cvssData', {}).get('baseScore')
            if score is not None:
                return str(score)

        return ""
    except Exception as e:
        print(f"    Warning: NVD lookup failed for {cve_id}: {e}")
        return ""


def fetch_cvss_batch(cve_ids):
    """Fetch CVSS scores for a list of CVE IDs with rate limiting."""
    results = {}
    total = len(cve_ids)
    api_status = "with API key" if NVD_API_KEY else "without API key (slower)"
    print(f"\nFetching CVSS scores from NVD ({api_status})...")

    for i, cve_id in enumerate(cve_ids, 1):
        print(f"  [{i}/{total}] {cve_id}...", end=" ", flush=True)
        score = fetch_cvss_from_nvd(cve_id)
        results[cve_id] = score
        print(f"CVSS {score}" if score else "no score found")

        if i < total:
            time.sleep(NVD_DELAY)

    return results


# ---------------------------------------------------------------------------
# CISA KEV Fetch
# ---------------------------------------------------------------------------

def fetch_cisa_kev():
    """Fetch the latest KEV catalog from CISA."""
    print("Fetching CISA KEV catalog...")
    try:
        req = urllib.request.Request(
            CISA_KEV_URL,
            headers={'User-Agent': 'FixTheVuln-KEV-Fetcher/1.0'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"Fetched {len(data.get('vulnerabilities', []))} total vulnerabilities")
            return data
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Data Loading / Saving
# ---------------------------------------------------------------------------

def load_seen_cves():
    """Load list of CVE IDs we've already seen."""
    if SEEN_FILE.exists():
        with open(SEEN_FILE, 'r') as f:
            return set(json.load(f).get('cves', []))
    return set()


def load_pending_reviews():
    """Load existing pending reviews to preserve in-progress work."""
    if PENDING_FILE.exists():
        with open(PENDING_FILE, 'r') as f:
            data = json.load(f)
            return {v['cveID']: v for v in data.get('vulnerabilities', [])}
    return {}


def load_posted_ids():
    """Load CVE IDs that are already posted on the site (kev-data.json)."""
    if KEV_DATA_FILE.exists():
        with open(KEV_DATA_FILE, 'r') as f:
            data = json.load(f)
            ids = set()
            for v in data.get('vulnerabilities', []):
                # Handle compound IDs like "CVE-2026-20952 & 20953"
                raw_id = v.get('id', '')
                ids.add(raw_id)
                # Also extract individual CVE IDs from compound entries
                for part in raw_id.replace('&', ',').split(','):
                    part = part.strip()
                    if part.startswith('CVE-'):
                        ids.add(part)
            return ids
    return set()


def save_seen_cves(cve_ids):
    """Save list of seen CVE IDs."""
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SEEN_FILE, 'w') as f:
        json.dump({
            'last_updated': datetime.now().isoformat(),
            'count': len(cve_ids),
            'cves': list(cve_ids)
        }, f)


def save_pending(pending_dict):
    """Save pending_review.json from a dict keyed by CVE ID."""
    data = {
        "last_updated": datetime.now().isoformat(),
        "total_pending": len(pending_dict),
        "instructions": "Review entries, then set include_on_site to true. Run: python scripts/generate_html.py",
        "vulnerabilities": list(pending_dict.values())
    }
    with open(PENDING_FILE, 'w') as f:
        json.dump(data, f, indent=2)


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def truncate(text, max_len=120):
    """Truncate text to max_len, adding ellipsis if needed."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[:max_len - 3].rsplit(' ', 1)[0] + "..."


def filter_recent(vulnerabilities, days=LOOKBACK_DAYS):
    """Filter to CVEs added within the last N days."""
    cutoff = datetime.now() - timedelta(days=days)
    recent = []
    for vuln in vulnerabilities:
        date_added = vuln.get('dateAdded', '')
        try:
            added_dt = datetime.strptime(date_added, '%Y-%m-%d')
            if added_dt >= cutoff:
                recent.append(vuln)
        except ValueError:
            continue
    return recent


def format_for_review(vuln, cvss_score=""):
    """Format a vulnerability for review with auto-filled fields."""
    cve_id = vuln.get('cveID', 'Unknown')
    vendor = vuln.get('vendorProject', 'Unknown')
    product = vuln.get('product', '')
    title = f"{vendor} {product}".strip() if product else vendor
    description = vuln.get('shortDescription', '')
    required_action = vuln.get('requiredAction', '')

    return {
        "cveID": cve_id,
        "title": title,
        "vendor": vendor,
        "product": product,
        "name": vuln.get('vulnerabilityName', ''),
        "description": description,
        "dateAdded": vuln.get('dateAdded', ''),
        "dueDate": vuln.get('dueDate', ''),
        "ransomware": vuln.get('knownRansomwareCampaignUse', 'Unknown'),
        "cisaNotes": vuln.get('notes', ''),

        # Expert review links
        "links": {
            "nvd": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
            "attackerKB": f"https://attackerkb.com/topics/{cve_id}",
            "bleepingComputer": f"https://www.bleepingcomputer.com/search/?q={cve_id}",
            "greynoise": f"https://viz.greynoise.io/query?gnql=cve%3A{cve_id}",
            "rapid7": f"https://www.rapid7.com/db/?q={cve_id}",
            "theRecord": f"https://therecord.media/?s={cve_id}",
        },

        # Auto-filled fields (review and edit if needed)
        "cvss": cvss_score,
        "short_description": truncate(description),
        "fix": required_action,
        "include_on_site": False,
        "priority": "high" if vuln.get('knownRansomwareCampaignUse') == 'Known' else ""
    }


def generate_html_card(vuln):
    """Generate HTML card in the exact format for index.html."""
    return f'''                <div class="kev-card">
                    <h4>{vuln['title']}</h4>
                    <div class="cve-id">{vuln['cveID']} | {vuln['cvss']}</div>
                    <p>{vuln['short_description']}</p>
                    <div class="kev-fix"><strong>Fix:</strong> {vuln['fix']}</div>
                </div>'''


def generate_review_markdown(vulns):
    """Generate markdown for weekend review with expert links."""
    lines = [
        "# KEV Review - Week of " + datetime.now().strftime('%Y-%m-%d'),
        "",
        f"**CVEs to review:** {len(vulns)}",
        "",
        "---",
        "",
    ]

    # Separate ransomware-related (priority)
    ransomware = [v for v in vulns if v.get('ransomware') == 'Known']
    other = [v for v in vulns if v.get('ransomware') != 'Known']

    all_vulns = ransomware + other  # Priority first

    for v in all_vulns:
        cve = v['cveID']
        is_ransomware = v.get('ransomware') == 'Known'

        lines.append(f"## {'[RANSOMWARE] ' if is_ransomware else ''}{cve}: {v['title']}")
        lines.append("")
        lines.append(f"**CVSS:** {v.get('cvss', 'N/A')}")
        lines.append(f"**Description:** {v['description']}")
        lines.append(f"**Fix:** {v.get('fix', 'N/A')}")
        lines.append(f"**Due Date:** {v['dueDate']}")
        lines.append(f"**CISA Notes:** {v['cisaNotes']}")
        lines.append("")
        lines.append("### Expert Reviews (click to check):")
        lines.append(f"- [NVD - Official Details]({v['links']['nvd']})")
        lines.append(f"- [AttackerKB - Exploitability Rating]({v['links']['attackerKB']})")
        lines.append(f"- [BleepingComputer - News Coverage]({v['links']['bleepingComputer']})")
        lines.append(f"- [GreyNoise - Active Scanning]({v['links']['greynoise']})")
        lines.append(f"- [Rapid7 - Technical Analysis]({v['links']['rapid7']})")
        lines.append(f"- [The Record - Threat Intel]({v['links']['theRecord']})")
        lines.append("")
        lines.append("### Your Review:")
        lines.append("Fields are auto-filled. Edit in pending_review.json if needed,")
        lines.append("then set `include_on_site` to `true`.")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## Publish to Site")
    lines.append("")
    lines.append("After setting `include_on_site: true`, run:")
    lines.append("```bash")
    lines.append("python scripts/generate_html.py")
    lines.append("```")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status():
    """Show status of all pending entries."""
    print("=" * 70)
    print("PENDING REVIEW STATUS")
    print("=" * 70)

    pending = load_pending_reviews()
    if not pending:
        print("\nNo pending entries. Run: python scripts/fetch_kev.py")
        return 0

    posted_ids = load_posted_ids()

    # Categorize
    posted = []
    ready = []
    needs_work = []

    for cve_id, v in pending.items():
        has_cvss = bool(v.get('cvss'))
        has_desc = bool(v.get('short_description'))
        has_fix = bool(v.get('fix'))
        is_posted = cve_id in posted_ids

        if is_posted:
            posted.append(v)
        elif has_cvss and has_desc and has_fix:
            ready.append(v)
        else:
            needs_work.append(v)

    # Print table
    print(f"\n{'STATUS':<10} {'CVE ID':<22} {'CVSS':<8} {'DATE':<12} TITLE")
    print("-" * 70)

    for v in posted:
        cvss = v.get('cvss', '-')
        print(f"{'POSTED':<10} {v['cveID']:<22} {cvss:<8} {v.get('dateAdded', ''):<12} {v['title'][:30]}")

    for v in ready:
        cvss = v.get('cvss', '-')
        print(f"{'READY':<10} {v['cveID']:<22} {cvss:<8} {v.get('dateAdded', ''):<12} {v['title'][:30]}")

    for v in needs_work:
        missing = []
        if not v.get('cvss'): missing.append('cvss')
        if not v.get('short_description'): missing.append('desc')
        if not v.get('fix'): missing.append('fix')
        cvss = v.get('cvss', '-')
        print(f"{'EMPTY':<10} {v['cveID']:<22} {cvss:<8} {v.get('dateAdded', ''):<12} {v['title'][:30]}")
        print(f"{'':>10} Missing: {', '.join(missing)}")

    # Summary
    print("-" * 70)
    print(f"POSTED: {len(posted)}  |  READY to post: {len(ready)}  |  NEEDS WORK: {len(needs_work)}")

    if posted:
        print(f"\nTip: Run --clean to remove {len(posted)} already-posted entries from pending.")
    if ready:
        print(f"\nTip: {len(ready)} entries are ready. Set include_on_site to true, then run:")
        print("     python scripts/generate_html.py")

    return 0


def cmd_clean():
    """Remove already-posted entries from pending_review.json."""
    print("=" * 50)
    print("CLEAN PENDING LIST")
    print("=" * 50)

    pending = load_pending_reviews()
    if not pending:
        print("\nNothing to clean.")
        return 0

    posted_ids = load_posted_ids()
    original_count = len(pending)

    removed = []
    for cve_id in list(pending.keys()):
        if cve_id in posted_ids:
            removed.append(cve_id)
            del pending[cve_id]

    if removed:
        save_pending(pending)
        print(f"\nRemoved {len(removed)} already-posted entries:")
        for cve_id in removed:
            print(f"  - {cve_id}")
        print(f"\nPending: {original_count} -> {len(pending)}")
    else:
        print("\nNo posted entries found in pending list. Nothing to clean.")

    return 0


def cmd_backfill():
    """Fill empty fields on existing pending entries using NVD + CISA data."""
    print("=" * 50)
    print("BACKFILL EMPTY FIELDS")
    print("=" * 50)

    pending = load_pending_reviews()
    if not pending:
        print("\nNo pending entries to backfill.")
        return 0

    # Find entries with empty fields
    needs_cvss = []
    needs_desc = []
    needs_fix = []

    for cve_id, v in pending.items():
        if not v.get('cvss'):
            needs_cvss.append(cve_id)
        if not v.get('short_description'):
            needs_desc.append(cve_id)
        if not v.get('fix'):
            needs_fix.append(cve_id)

    if not needs_cvss and not needs_desc and not needs_fix:
        print("\nAll entries already have cvss, short_description, and fix filled in.")
        return 0

    print(f"\nEntries needing CVSS:             {len(needs_cvss)}")
    print(f"Entries needing short_description: {len(needs_desc)}")
    print(f"Entries needing fix:              {len(needs_fix)}")

    # Fetch CVSS scores for entries that need them
    if needs_cvss:
        cvss_scores = fetch_cvss_batch(needs_cvss)
        for cve_id, score in cvss_scores.items():
            if score:
                pending[cve_id]['cvss'] = score

    # Fill short_description from existing description field
    for cve_id in needs_desc:
        v = pending[cve_id]
        desc = v.get('description', '')
        if desc:
            v['short_description'] = truncate(desc)

    # Fill fix from CISA data (need to fetch catalog for requiredAction)
    if needs_fix:
        print("\nFetching CISA catalog for fix/remediation data...")
        kev = fetch_cisa_kev()
        cisa_lookup = {v.get('cveID'): v for v in kev.get('vulnerabilities', [])}

        for cve_id in needs_fix:
            cisa_vuln = cisa_lookup.get(cve_id)
            if cisa_vuln:
                action = cisa_vuln.get('requiredAction', '')
                if action:
                    pending[cve_id]['fix'] = action

    # Save
    save_pending(pending)

    # Report
    print("\nBackfill complete. Updated entries:")
    for cve_id, v in pending.items():
        cvss = v.get('cvss', '-')
        has_desc = 'Y' if v.get('short_description') else 'N'
        has_fix = 'Y' if v.get('fix') else 'N'
        print(f"  {cve_id:<22} CVSS: {cvss:<8} Desc: {has_desc}  Fix: {has_fix}")

    return 0


def cmd_fetch():
    """Main fetch: get new CVEs, auto-fill fields, save to pending."""
    print("=" * 50)
    print("CISA KEV Fetcher")
    print("=" * 50)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Fetch catalog
    kev = fetch_cisa_kev()
    all_vulns = kev.get('vulnerabilities', [])

    # Filter to recent only
    recent = filter_recent(all_vulns, LOOKBACK_DAYS)
    print(f"CVEs added in last {LOOKBACK_DAYS} days: {len(recent)}")

    # Check what we've already seen
    seen = load_seen_cves()

    # Find new ones
    new_raw = []
    for vuln in recent:
        cve_id = vuln.get('cveID')
        if cve_id and cve_id not in seen:
            new_raw.append(vuln)

    print(f"New CVEs to review: {len(new_raw)}")

    if new_raw:
        # Fetch CVSS scores for all new CVEs
        cve_ids = [v.get('cveID') for v in new_raw]
        cvss_scores = fetch_cvss_batch(cve_ids)

        # Format with auto-filled fields
        new_vulns = []
        for vuln in new_raw:
            cve_id = vuln.get('cveID', '')
            score = cvss_scores.get(cve_id, '')
            new_vulns.append(format_for_review(vuln, cvss_score=score))

        # Load existing pending reviews to preserve in-progress work
        existing_pending = load_pending_reviews()

        # Merge: keep existing reviews, add new ones
        for vuln in new_vulns:
            cve_id = vuln['cveID']
            if cve_id not in existing_pending:
                existing_pending[cve_id] = vuln

        # Save
        save_pending(existing_pending)

        # Generate review markdown with expert links
        review_md = generate_review_markdown(new_vulns)
        with open(DATA_DIR / "REVIEW.md", 'w') as f:
            f.write(review_md)

        print(f"\nAdded {len(new_vulns)} new CVEs (total pending: {len(existing_pending)})")
        print(f"  - data/pending_review.json (review & set include_on_site: true)")
        print(f"  - data/REVIEW.md (review guide with expert links)")

        # Show what was auto-filled
        print(f"\nAuto-filled summary:")
        for v in new_vulns:
            cvss = v.get('cvss', '-') or '-'
            has_desc = 'Y' if v.get('short_description') else 'N'
            has_fix = 'Y' if v.get('fix') else 'N'
            print(f"  {v['cveID']:<22} CVSS: {cvss:<8} Desc: {has_desc}  Fix: {has_fix}")

        # GitHub Actions output
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                f.write(f"new_count={len(new_vulns)}\n")
                f.write("has_new=true\n")
    else:
        print("\nNo new CVEs to review.")
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                f.write("new_count=0\n")
                f.write("has_new=false\n")

    # Mark all recent as seen
    for vuln in recent:
        cve_id = vuln.get('cveID')
        if cve_id:
            seen.add(cve_id)
    save_seen_cves(seen)

    # Save full catalog
    kev['fetched_at'] = datetime.now().isoformat()
    with open(KEV_FILE, 'w') as f:
        json.dump(kev, f)

    print("\nDone!")
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="CISA KEV Fetcher - Auto-fills CVSS, description, and fix fields"
    )
    parser.add_argument('--status', action='store_true',
                        help='Show status of all pending entries (posted/ready/empty)')
    parser.add_argument('--backfill', action='store_true',
                        help='Fill empty fields on existing pending entries')
    parser.add_argument('--clean', action='store_true',
                        help='Remove already-posted entries from pending list')
    args = parser.parse_args()

    if args.status:
        return cmd_status()
    elif args.backfill:
        return cmd_backfill()
    elif args.clean:
        return cmd_clean()
    else:
        return cmd_fetch()


if __name__ == "__main__":
    sys.exit(main())
