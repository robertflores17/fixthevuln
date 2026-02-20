#!/usr/bin/env python3
"""
Generate copy-paste-ready social media and newsletter content
for newly published CVEs. Reads .latest_published.json written
by generate_html.py and outputs data/cve-social-posts.json.
"""

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / "data"
LATEST_FILE = DATA_DIR / ".latest_published.json"
OUTPUT_FILE = DATA_DIR / "cve-social-posts.json"


def build_highlights(cves):
    """Pick the top CVEs to highlight (critical CVSS, ransomware, etc.)."""
    highlights = []
    for c in sorted(cves, key=lambda x: float(x.get('cvss', 0) or 0), reverse=True):
        cvss = c.get('cvss', '')
        vendor = c.get('vendor', '')
        product = c.get('product', '')
        label = f"{vendor} {product}".strip() or c.get('title', '')
        entry = f"{label} (CVSS {cvss})" if cvss else label
        if c.get('ransomware', '').lower() == 'known':
            entry += " — ransomware linked"
        highlights.append(entry)
    return highlights


def generate_linkedin(count, highlights, date):
    top = highlights[:4]
    bullets = "\n".join(f"- {h}" for h in top)
    if count > len(top):
        bullets += f"\n- +{count - len(top)} more"

    return f"""{count} new vulnerabilities added to CISA's Known Exploited Vulnerabilities catalog.

Key entries:
{bullets}

Full breakdown with remediation steps at fixthevuln.com

#cybersecurity #vulnerabilitymanagement #CISAKEV #infosec"""


def generate_twitter(count, highlights, date):
    # Keep under 280 chars
    vendors = []
    seen = set()
    for h in highlights:
        v = h.split(" (")[0].strip()
        if v not in seen:
            vendors.append(v)
            seen.add(v)

    vendor_list = ", ".join(vendors[:4])
    if len(vendors) > 4:
        vendor_list += " and more"

    return f"""{count} new CVEs added to the CISA KEV catalog — {vendor_list}.

Remediation guides at fixthevuln.com

#cybersecurity #CISAKEV #infosec"""


def generate_reddit_title(count, highlights):
    vendors = []
    seen = set()
    for h in highlights:
        v = h.split(" (")[0].strip()
        if v not in seen:
            vendors.append(v)
            seen.add(v)
    vendor_str = ", ".join(vendors[:5])
    if len(vendors) > 5:
        vendor_str += ", more"
    return f"{count} New CISA KEV Entries — {vendor_str}"


def generate_reddit_body(count, highlights):
    bullets = "\n".join(f"- {h}" for h in highlights)
    return f"""CISA added {count} new vulnerabilities to the Known Exploited Vulnerabilities catalog this week.

{bullets}

Remediation steps for each one at [fixthevuln.com](https://fixthevuln.com)"""


def generate_newsletter_subject(count, highlights):
    top_vendor = highlights[0].split(" (")[0].strip() if highlights else "Multiple Vendors"
    if count <= 3:
        return f"Patch Now: {', '.join(h.split(' (')[0].strip() for h in highlights[:count])}"
    return f"{count} New Exploited Vulnerabilities — {top_vendor} and More"


def generate_newsletter_body(count, cves, highlights, date):
    bullets = "\n".join(f"  - {h}" for h in highlights)

    ransomware_entries = [c for c in cves if c.get('ransomware', '').lower() == 'known']
    ransomware_note = ""
    if ransomware_entries:
        names = ", ".join(f"{c['vendor']} {c['product']}".strip() for c in ransomware_entries)
        ransomware_note = f"\nRansomware linked: {names}. Prioritize these.\n"

    return f"""This week CISA added {count} new entries to the Known Exploited Vulnerabilities catalog:

{bullets}
{ransomware_note}
Remediation guidance for each vulnerability at https://fixthevuln.com

-- Robert"""


def generate_individual_posts(cves):
    """Generate per-CVE posts for high-severity entries."""
    posts = []
    for c in cves:
        cvss = float(c.get('cvss', 0) or 0)
        if cvss < 8.0:
            continue

        cve_id = c['cveID']
        vendor = c.get('vendor', '')
        product = c.get('product', '')
        label = f"{vendor} {product}".strip()
        desc = c.get('short_description', '')
        ransomware = c.get('ransomware', '').lower() == 'known'

        tag = " (ransomware linked)" if ransomware else ""

        posts.append({
            "cveID": cve_id,
            "cvss": c.get('cvss', ''),
            "twitter": f"{cve_id}: {label} — CVSS {cvss}{tag}. Patch now.\n\nDetails at fixthevuln.com\n\n#cybersecurity #CISAKEV",
            "linkedin": f"{cve_id} — {label} (CVSS {cvss}){tag}\n\n{desc}\n\nRemediation steps at fixthevuln.com\n\n#cybersecurity #vulnerabilitymanagement",
        })

    return posts


def main():
    if not LATEST_FILE.exists():
        print("No recently published CVEs found. Skipping social post generation.")
        return

    with open(LATEST_FILE) as f:
        data = json.load(f)

    cves = data.get('published', [])
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))

    if not cves:
        print("No CVEs in latest published. Skipping.")
        return

    count = len(cves)
    highlights = build_highlights(cves)

    output = {
        "generated": date,
        "cve_count": count,
        "batch_posts": {
            "linkedin": generate_linkedin(count, highlights, date),
            "twitter": generate_twitter(count, highlights, date),
            "reddit_title": generate_reddit_title(count, highlights),
            "reddit_body": generate_reddit_body(count, highlights),
            "newsletter_subject": generate_newsletter_subject(count, highlights),
            "newsletter_body": generate_newsletter_body(count, cves, highlights, date),
        },
        "individual_posts": generate_individual_posts(cves),
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Social posts generated: {OUTPUT_FILE}")
    print(f"  Batch posts for {count} CVEs")
    print(f"  Individual posts for {len(output['individual_posts'])} high-severity CVEs")


if __name__ == "__main__":
    main()
