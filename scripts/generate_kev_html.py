#!/usr/bin/env python3
"""
Generate HTML snippet for the KEV section from reviewed vulnerabilities.
Run this after reviewing pending_review.json to get copy-paste HTML.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
REVIEWED_FILE = DATA_DIR / "reviewed_kev.json"


def load_reviewed():
    """Load reviewed vulnerabilities."""
    if REVIEWED_FILE.exists():
        with open(REVIEWED_FILE, 'r') as f:
            return json.load(f)
    return {"vulnerabilities": []}


def generate_kev_card(vuln):
    """Generate HTML for a single KEV card."""
    cve_id = vuln.get('cveID', 'Unknown')
    vendor = vuln.get('vendor', 'Unknown')
    product = vuln.get('product', '')
    description = vuln.get('description', vuln.get('name', 'No description available'))
    remediation = vuln.get('custom_remediation', 'Apply vendor patches.')
    cvss = vuln.get('cvss', 'Unknown CVSS')

    title = f"{vendor} {product}".strip() if product else vendor

    return f'''                <div class="kev-card">
                    <h4>{title}</h4>
                    <div class="cve-id">{cve_id} | {cvss}</div>
                    <p>{description}</p>
                    <div class="kev-fix"><strong>Fix:</strong> {remediation}</div>
                </div>
'''


def main():
    print("=" * 60)
    print("KEV HTML Generator")
    print("=" * 60)

    data = load_reviewed()
    vulns = data.get('vulnerabilities', [])

    # Filter to only include items marked for site
    to_publish = [v for v in vulns if v.get('include_on_site', False)]

    if not to_publish:
        print("\nNo vulnerabilities marked for publishing.")
        print("Set 'include_on_site: true' in reviewed_kev.json")
        return

    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    to_publish.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))

    print(f"\nGenerating HTML for {len(to_publish)} vulnerabilities...\n")
    print("-" * 60)

    # Generate HTML
    html_parts = []
    for vuln in to_publish:
        html_parts.append(generate_kev_card(vuln))

    full_html = "\n".join(html_parts)

    # Output
    print("Copy the following HTML into the kev-grid div in index.html:\n")
    print(full_html)

    # Also save to file
    output_file = DATA_DIR / "kev_cards.html"
    with open(output_file, 'w') as f:
        f.write(full_html)
    print(f"\nSaved to {output_file}")


if __name__ == "__main__":
    main()
