#!/usr/bin/env python3
"""
Fetch CISA Known Exploited Vulnerabilities (KEV) catalog.
Generates HTML cards ready to paste into index.html.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import urllib.request
import urllib.error

# Configuration
CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
DATA_DIR = Path(__file__).parent.parent / "data"
KEV_FILE = DATA_DIR / "kev.json"
PENDING_FILE = DATA_DIR / "pending_review.json"
SEEN_FILE = DATA_DIR / "seen_cves.json"

# Only fetch CVEs added in the last N days
LOOKBACK_DAYS = 14


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
            # Return dict keyed by CVE ID for easy lookup
            return {v['cveID']: v for v in data.get('vulnerabilities', [])}
    return {}


def save_seen_cves(cve_ids):
    """Save list of seen CVE IDs."""
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SEEN_FILE, 'w') as f:
        json.dump({
            'last_updated': datetime.now().isoformat(),
            'count': len(cve_ids),
            'cves': list(cve_ids)
        }, f)


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


def format_for_review(vuln):
    """Format a vulnerability for review."""
    cve_id = vuln.get('cveID', 'Unknown')
    vendor = vuln.get('vendorProject', 'Unknown')
    product = vuln.get('product', '')
    title = f"{vendor} {product}".strip() if product else vendor

    return {
        "cveID": cve_id,
        "title": title,
        "vendor": vendor,
        "product": product,
        "name": vuln.get('vulnerabilityName', ''),
        "description": vuln.get('shortDescription', ''),
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

        # Fields YOU fill in during review
        "cvss": "",  # e.g., "CVSS 9.8" or "Zero-Day"
        "short_description": "",  # Your 1-line summary
        "fix": "",  # Your remediation text
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
        lines.append(f"**Description:** {v['description']}")
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
        lines.append("### Your Review (fill in pending_review.json):")
        lines.append("```json")
        lines.append(f'"cveID": "{cve}",')
        lines.append('"cvss": "CVSS X.X",        // or "Zero-Day"')
        lines.append('"short_description": "",   // Your 1-line summary')
        lines.append('"fix": "",                 // Your remediation')
        lines.append('"include_on_site": true')
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Add HTML template section
    lines.append("## Ready-to-Paste HTML")
    lines.append("")
    lines.append("After filling in the fields above, run:")
    lines.append("```bash")
    lines.append("python scripts/generate_html.py")
    lines.append("```")
    lines.append("")
    lines.append("Or manually create cards in this format:")
    lines.append("```html")
    lines.append('<div class="kev-card">')
    lines.append('    <h4>Vendor Product</h4>')
    lines.append('    <div class="cve-id">CVE-XXXX-XXXXX | CVSS X.X</div>')
    lines.append('    <p>Your short description.</p>')
    lines.append('    <div class="kev-fix"><strong>Fix:</strong> Your remediation.</div>')
    lines.append('</div>')
    lines.append("```")

    return "\n".join(lines)


def main():
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
    new_vulns = []
    for vuln in recent:
        cve_id = vuln.get('cveID')
        if cve_id and cve_id not in seen:
            new_vulns.append(format_for_review(vuln))

    print(f"New CVEs to review: {len(new_vulns)}")

    if new_vulns:
        # Load existing pending reviews to preserve in-progress work
        existing_pending = load_pending_reviews()

        # Merge: keep existing reviews, add new ones
        for vuln in new_vulns:
            cve_id = vuln['cveID']
            if cve_id not in existing_pending:
                existing_pending[cve_id] = vuln

        # Save merged pending review JSON
        pending = {
            "last_updated": datetime.now().isoformat(),
            "total_pending": len(existing_pending),
            "instructions": "Fill in: cvss, short_description, fix, include_on_site",
            "vulnerabilities": list(existing_pending.values())
        }
        with open(PENDING_FILE, 'w') as f:
            json.dump(pending, f, indent=2)

        # Generate review markdown with expert links
        review_md = generate_review_markdown(new_vulns)
        with open(DATA_DIR / "REVIEW.md", 'w') as f:
            f.write(review_md)

        print(f"\nAdded {len(new_vulns)} new CVEs (total pending: {len(existing_pending)})")
        print(f"  - data/pending_review.json (edit this)")
        print(f"  - data/REVIEW.md (review guide with expert links)")

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


if __name__ == "__main__":
    sys.exit(main())
