#!/usr/bin/env python3
"""
Generate HTML cards from reviewed vulnerabilities.
Run this after filling in pending_review.json.

Output: Ready-to-paste HTML for index.html KEV section.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
PENDING_FILE = DATA_DIR / "pending_review.json"
OUTPUT_FILE = DATA_DIR / "kev_cards.html"


def generate_card(vuln):
    """Generate a single KEV card HTML."""
    title = vuln.get('title', f"{vuln.get('vendor', '')} {vuln.get('product', '')}").strip()
    cve_id = vuln.get('cveID', 'Unknown')
    cvss = vuln.get('cvss', 'Unknown')
    description = vuln.get('short_description', vuln.get('description', ''))
    fix = vuln.get('fix', 'Apply vendor patches.')

    # Truncate description if too long
    if len(description) > 120:
        description = description[:117] + "..."

    return f'''                <div class="kev-card">
                    <h4>{title}</h4>
                    <div class="cve-id">{cve_id} | {cvss}</div>
                    <p>{description}</p>
                    <div class="kev-fix"><strong>Fix:</strong> {fix}</div>
                </div>'''


def main():
    print("=" * 50)
    print("KEV HTML Card Generator")
    print("=" * 50)

    if not PENDING_FILE.exists():
        print("No pending_review.json found. Run fetch_kev.py first.")
        return 1

    with open(PENDING_FILE, 'r') as f:
        data = json.load(f)

    vulns = data.get('vulnerabilities', [])

    # Filter to only items marked for site
    to_publish = [v for v in vulns if v.get('include_on_site', False)]

    if not to_publish:
        print("\nNo vulnerabilities marked for publishing.")
        print("Edit pending_review.json and set 'include_on_site': true")
        print("\nExample:")
        print('  "cvss": "CVSS 9.8",')
        print('  "short_description": "RCE via malicious file upload.",')
        print('  "fix": "Update to version 2.0.1 or later.",')
        print('  "include_on_site": true')
        return 0

    print(f"\nGenerating HTML for {len(to_publish)} vulnerabilities...\n")

    # Generate HTML
    cards = []
    for vuln in to_publish:
        cards.append(generate_card(vuln))

    html_output = "\n\n".join(cards)

    # Save to file
    with open(OUTPUT_FILE, 'w') as f:
        f.write("<!-- Copy and paste into index.html kev-grid section -->\n\n")
        f.write(html_output)

    print("-" * 50)
    print("COPY THE HTML BELOW INTO index.html (kev-grid div):")
    print("-" * 50)
    print()
    print(html_output)
    print()
    print("-" * 50)
    print(f"\nAlso saved to: {OUTPUT_FILE}")

    return 0


if __name__ == "__main__":
    exit(main())
