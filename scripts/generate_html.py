#!/usr/bin/env python3
"""
Add reviewed vulnerabilities to kev-data.json.
Run this after filling in pending_review.json.

This script:
1. Reads pending_review.json for items marked include_on_site: true
2. Converts them to kev-data.json format
3. Adds them to kev-data.json (avoids duplicates)
4. Homepage will automatically display them
"""

import json
import re
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / "data"
PENDING_FILE = DATA_DIR / "pending_review.json"
KEV_DATA_FILE = DATA_DIR / "kev-data.json"
COMMIT_SUMMARY_FILE = DATA_DIR / ".commit_summary.txt"
LATEST_PUBLISHED_FILE = DATA_DIR / ".latest_published.json"
LATEST_UPDATE_FILE = DATA_DIR / "latest-update.json"


def parse_cvss(cvss_str):
    """
    Parse CVSS string to number and detect Zero-Day.

    Returns: (cvss_number, is_zero_day)

    Examples:
        "9.8" -> (9.8, False)
        "CVSS 9.8" -> (9.8, False)
        "Zero-Day" -> (10, True)
        "" or None -> (None, False)
    """
    if not cvss_str:
        return None, False

    cvss_str = str(cvss_str).strip()

    # Check for Zero-Day
    if "zero" in cvss_str.lower() or "0-day" in cvss_str.lower():
        return 10, True

    # Extract number from string like "CVSS 9.8" or just "9.8"
    match = re.search(r'(\d+\.?\d*)', cvss_str)
    if match:
        return float(match.group(1)), False

    return None, False


def convert_to_kev_format(vuln):
    """Convert pending_review format to kev-data.json format."""

    # Parse CVSS
    cvss_num, is_zero_day = parse_cvss(vuln.get('cvss', ''))

    # Get title - prefer 'title', fallback to 'name' or vendor+product
    title = vuln.get('title', '').strip()
    if not title or title == f"{vuln.get('vendor', '')} {vuln.get('product', '')}".strip():
        # Use the 'name' field if title is just vendor+product
        title = vuln.get('name', title)

    # Get description - prefer short_description, fallback to description
    description = vuln.get('short_description', '').strip()
    if not description:
        description = vuln.get('description', '')
        # Truncate long descriptions
        if len(description) > 150:
            description = description[:147] + "..."

    return {
        "id": vuln.get('cveID', 'Unknown'),
        "title": title,
        "cvss": cvss_num,
        "isZeroDay": is_zero_day,
        "description": description,
        "fix": vuln.get('fix', 'Apply vendor patches.'),
        "dateAdded": vuln.get('dateAdded', datetime.now().strftime('%Y-%m-%d')),
        "archived": False  # New items go to homepage
    }


def load_kev_data():
    """Load existing kev-data.json or create empty structure."""
    if KEV_DATA_FILE.exists():
        with open(KEV_DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
        "vulnerabilities": []
    }


def save_kev_data(data):
    """Save kev-data.json with updated timestamp."""
    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d')
    with open(KEV_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def cleanup_pending(pending_data, processed_ids):
    """
    Remove processed CVEs from pending_review.json.
    Keeps it as a clean inbox of unreviewed items.
    """
    original_count = len(pending_data.get('vulnerabilities', []))

    # Filter out processed entries
    pending_data['vulnerabilities'] = [
        v for v in pending_data.get('vulnerabilities', [])
        if v.get('cveID') not in processed_ids
    ]

    # Update count
    pending_data['total_pending'] = len(pending_data['vulnerabilities'])
    pending_data['last_updated'] = datetime.now().isoformat()

    # Save
    with open(PENDING_FILE, 'w') as f:
        json.dump(pending_data, f, indent=2)

    removed = original_count - len(pending_data['vulnerabilities'])
    return removed


def write_commit_summary(added_ids, vulns_lookup):
    """Write a short commit summary for the workflow to use."""
    if not added_ids:
        # No summary needed
        if COMMIT_SUMMARY_FILE.exists():
            COMMIT_SUMMARY_FILE.unlink()
        return

    # Build vendor list from processed CVEs (deduplicated, order preserved)
    vendors = []
    seen = set()
    for cve_id in added_ids:
        v = vulns_lookup.get(cve_id, {})
        vendor = v.get('vendor', '').strip()
        if vendor and vendor not in seen:
            vendors.append(vendor)
            seen.add(vendor)

    count = len(added_ids)

    if count <= 3:
        # List CVE IDs directly
        title = f"Publish {', '.join(added_ids)}"
    else:
        # Summarize with count + vendor names
        shown = vendors[:5]
        title = f"Publish {count} new CVEs: {', '.join(shown)}"
        if len(vendors) > 5:
            title += ", more"

    summary = f"{title}\n\n-- Robert\n[skip ci]"
    with open(COMMIT_SUMMARY_FILE, 'w') as f:
        f.write(summary)


def write_latest_published(added_ids, vulns_lookup):
    """Save published CVE details so the social script can read them."""
    if not added_ids:
        if LATEST_PUBLISHED_FILE.exists():
            LATEST_PUBLISHED_FILE.unlink()
        return

    entries = []
    for cve_id in added_ids:
        v = vulns_lookup.get(cve_id, {})
        entries.append({
            "cveID": cve_id,
            "vendor": v.get('vendor', ''),
            "product": v.get('product', ''),
            "title": v.get('title', ''),
            "cvss": v.get('cvss', ''),
            "short_description": v.get('short_description', ''),
            "ransomware": v.get('ransomware', 'Unknown'),
        })

    with open(LATEST_PUBLISHED_FILE, 'w') as f:
        json.dump({"published": entries, "date": datetime.now().strftime('%Y-%m-%d')}, f, indent=2)


def write_latest_update(added_ids, vulns_lookup):
    """Write latest-update.json for the homepage to display."""
    if not added_ids:
        return

    # Build vendor list (deduplicated, order preserved)
    vendors = []
    seen = set()
    for cve_id in added_ids:
        v = vulns_lookup.get(cve_id, {})
        vendor = v.get('vendor', '').strip()
        if vendor and vendor not in seen:
            vendors.append(vendor)
            seen.add(vendor)

    count = len(added_ids)
    date = datetime.now().strftime('%Y-%m-%d')

    # Build summary text
    if count <= 3:
        vendor_str = ", ".join(vendors)
    else:
        shown = vendors[:5]
        vendor_str = ", ".join(shown)
        if len(vendors) > 5:
            vendor_str += ", and more"

    summary = f"Reviewed and published {count} new CVEs: {vendor_str}."

    update = {
        "date": date,
        "count": count,
        "summary": summary,
        "cves": added_ids,
        "signedBy": "Robert"
    }

    with open(LATEST_UPDATE_FILE, 'w') as f:
        json.dump(update, f, indent=2)


def main():
    print("=" * 60)
    print("KEV Data Importer")
    print("Adds reviewed vulnerabilities to kev-data.json")
    print("=" * 60)

    # Check for pending file
    if not PENDING_FILE.exists():
        print("\nNo pending_review.json found. Run fetch_kev.py first.")
        return 1

    # Load pending vulnerabilities
    with open(PENDING_FILE, 'r') as f:
        pending_data = json.load(f)

    vulns = pending_data.get('vulnerabilities', [])

    # Filter to only items marked for site
    to_publish = [v for v in vulns if v.get('include_on_site', False)]

    if not to_publish:
        print("\nNo vulnerabilities marked for publishing.")
        print("\nTo publish, edit pending_review.json and set:")
        print('  "include_on_site": true')
        print("\nAlso fill in these fields:")
        print('  "cvss": "9.8",')
        print('  "short_description": "Brief description here.",')
        print('  "fix": "How to fix it."')
        return 0

    # Load existing kev-data.json
    kev_data = load_kev_data()
    existing_ids = {v['id'] for v in kev_data['vulnerabilities']}

    # Process each vulnerability
    added = []
    skipped = []

    print(f"\nProcessing {len(to_publish)} vulnerabilities...\n")

    for vuln in to_publish:
        cve_id = vuln.get('cveID', 'Unknown')

        if cve_id in existing_ids:
            skipped.append(cve_id)
            continue

        # Convert and add
        converted = convert_to_kev_format(vuln)
        kev_data['vulnerabilities'].insert(0, converted)  # Add to beginning
        existing_ids.add(cve_id)
        added.append(cve_id)

        # Print preview
        cvss_display = "Zero-Day" if converted['isZeroDay'] else (converted['cvss'] or "N/A")
        print(f"  + {cve_id} | {cvss_display}")
        print(f"    Title: {converted['title']}")
        print(f"    Fix: {converted['fix'][:60]}...")
        print()

    # Save updated data
    if added:
        save_kev_data(kev_data)

    # Cleanup pending_review.json - remove processed entries
    # (both newly added AND already existing in kev-data.json)
    processed_ids = set(added + skipped)
    removed_count = 0
    if processed_ids:
        removed_count = cleanup_pending(pending_data, processed_ids)

    # Write commit summary and published CVE details for the workflow
    vulns_lookup = {v.get('cveID'): v for v in to_publish}
    write_commit_summary(added, vulns_lookup)
    write_latest_published(added, vulns_lookup)
    write_latest_update(added, vulns_lookup)

    # Summary
    print("-" * 60)
    print("SUMMARY")
    print("-" * 60)
    print(f"  Added to site:    {len(added)} vulnerabilities")
    print(f"  Already existed:  {len(skipped)} (skipped duplicates)")
    print(f"  Removed from pending: {removed_count} entries")
    print(f"  Total in database: {len(kev_data['vulnerabilities'])} vulnerabilities")

    if added:
        print(f"\nSaved to: {KEV_DATA_FILE}")
        print("\nThe homepage will automatically display these.")
        print("To move to archive later, set 'archived': true in kev-data.json")

    if removed_count:
        print(f"\nCleaned up: {PENDING_FILE}")
        print(f"Remaining in pending: {len(pending_data['vulnerabilities'])} CVEs to review")

    # Count active vs archived
    active = sum(1 for v in kev_data['vulnerabilities'] if not v.get('archived', False))
    archived = sum(1 for v in kev_data['vulnerabilities'] if v.get('archived', False))
    print(f"\nCurrent status:")
    print(f"  Homepage (active): {active}")
    print(f"  Archive: {archived}")

    return 0


if __name__ == "__main__":
    exit(main())
