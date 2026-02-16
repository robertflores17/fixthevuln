#!/usr/bin/env python3
"""
Etsy CSV → Pinterest Bulk Upload CSV Converter

Reads the Etsy listing CSV export and generates a Pinterest-ready CSV
with board routing based on title keywords.

No API keys needed. No approval needed.

How to get your Etsy CSV:
  1. Go to Etsy.com → Shop Manager → Settings → Options
  2. Click "Download Data" tab
  3. Click "Download CSV" under "Currently for Sale Listings"
  4. Save the file (e.g., EtsyListingsDownload.csv)

Usage:
  python3 etsy_csv_to_pinterest.py EtsyListingsDownload.csv
  python3 etsy_csv_to_pinterest.py EtsyListingsDownload.csv --preview
  python3 etsy_csv_to_pinterest.py EtsyListingsDownload.csv -o my_pins.csv

Then upload the output CSV to Pinterest:
  Pinterest → Settings → Import content → Upload .csv file
"""

import argparse
import csv
import os
import sys

# ── Board Mapping ───────────────────────────────────────────────────────────

BOARD_MAPPING = {
    "CompTIA Study Planners": [
        "CompTIA", "Security+", "Network+", "CySA+", "PenTest+",
        "A+", "CASP+", "Cloud+", "Linux+", "Data+",
        "SY0-701", "N10-009", "CS0-003", "PT0-003",
        "220-1201", "220-1202", "CAS-005", "CV0-004", "XK0-006",
    ],
    "CISSP & ISC2 Study Planners": [
        "CISSP", "CCSP", "ISC2", "(ISC)2",
        "Certified in Cybersecurity", "CC Certified",
    ],
    "AWS Certification Planners": [
        "AWS", "Cloud Practitioner", "Solutions Architect",
        "CLF-C02", "SAA-C03", "SCS-C03", "DVA-C02", "SOA-C03",
    ],
    "Cisco Certification Planners": [
        "Cisco", "CCNA", "CCNP", "CyberOps",
        "200-301", "350-401", "200-201",
    ],
    "Microsoft Azure Study Planners": [
        "Microsoft", "Azure", "AZ-900", "AZ-104", "AZ-305",
        "AZ-500", "SC-900", "SC-200", "AI-900", "MS-900",
    ],
    "Google Cloud Study Planners": [
        "Google Cloud", "GCP",
        "Associate Cloud Engineer", "Professional Cloud Architect",
    ],
    "ISACA Certification Planners": [
        "ISACA", "CISA", "CISM", "CRISC", "CGEIT",
    ],
    "GIAC & SANS Study Planners": [
        "GIAC", "GSEC", "SANS", "GCIH", "GPEN",
    ],
}

DEFAULT_BOARD = "Cybersecurity Study Planners"


# ── Helpers ─────────────────────────────────────────────────────────────────

def match_board(title):
    """Route a listing title to the best Pinterest board."""
    title_upper = title.upper()
    best_board = DEFAULT_BOARD
    best_score = 0

    for board_name, keywords in BOARD_MAPPING.items():
        score = 0
        for kw in keywords:
            if kw.upper() in title_upper:
                score += len(kw)
        if score > best_score:
            best_score = score
            best_board = board_name

    return best_board


def truncate(text, max_len):
    if not text:
        return ""
    text = text.strip().replace("\n", " ").replace("\r", " ")
    # Collapse multiple spaces
    while "  " in text:
        text = text.replace("  ", " ")
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rsplit(" ", 1)[0] + "..."


def find_image_url(row):
    """Find the primary image URL from Etsy CSV columns."""
    # Etsy CSV has IMAGE1, IMAGE2, ... IMAGE10 columns
    for key in ["IMAGE1", "Image1", "image1", "IMAGE 1", "Image 1"]:
        if key in row and row[key].strip():
            return row[key].strip()

    # Fallback: check all columns for etsystatic image URLs
    for key, val in row.items():
        if val and "etsystatic.com" in val and ("/il_" in val or "/il/" in val):
            return val.strip()

    return ""


def find_title(row):
    """Find the title from Etsy CSV columns."""
    for key in ["TITLE", "Title", "title"]:
        if key in row and row[key].strip():
            return row[key].strip()
    return ""


def find_description(row):
    """Find the description from Etsy CSV columns."""
    for key in ["DESCRIPTION", "Description", "description"]:
        if key in row and row[key].strip():
            return row[key].strip()
    return ""


def find_tags(row):
    """Find tags from Etsy CSV columns."""
    tags = []
    # Etsy CSV has TAGS columns or comma-separated tags
    for key in ["TAGS", "Tags", "tags"]:
        if key in row and row[key].strip():
            tags.extend([t.strip() for t in row[key].split(",") if t.strip()])
            return tags

    # Check for TAG1, TAG2, ... TAG13 columns
    for i in range(1, 14):
        for prefix in ["TAG", "Tag", "tag"]:
            key = f"{prefix}{i}"
            if key in row and row[key].strip():
                tags.append(row[key].strip())

    return tags


def find_url(row):
    """Find the listing URL from Etsy CSV columns."""
    for key in ["URL", "Url", "url", "LISTING_URL", "listing_url"]:
        if key in row and row[key].strip():
            return row[key].strip()
    return ""


def add_utm(url):
    """Add UTM tracking parameters to a URL."""
    if not url:
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source=pinterest&utm_medium=social&utm_campaign=bulk_pin"


# ── Main ────────────────────────────────────────────────────────────────────

def convert(input_path, output_path, preview=False):
    # Detect encoding
    for encoding in ["utf-8-sig", "utf-8", "latin-1", "cp1252"]:
        try:
            with open(input_path, "r", encoding=encoding) as f:
                f.read(1000)
            break
        except (UnicodeDecodeError, UnicodeError):
            continue

    with open(input_path, "r", encoding=encoding) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("ERROR: No listings found in CSV.")
        sys.exit(1)

    print(f"Read {len(rows)} listings from {os.path.basename(input_path)}")
    print(f"Columns: {', '.join(rows[0].keys())}\n")

    # Process each listing
    pins = []
    board_counts = {}
    skipped = 0

    for row in rows:
        title = find_title(row)
        if not title:
            skipped += 1
            continue

        image_url = find_image_url(row)
        if not image_url:
            print(f"  SKIP (no image): {title[:60]}")
            skipped += 1
            continue

        description = find_description(row)
        listing_url = find_url(row)
        tags = find_tags(row)
        board = match_board(title)

        pin = {
            "Title": truncate(title, 100),
            "Media URL": image_url,
            "Pinterest board": board,
            "Description": truncate(description, 500),
            "Link": add_utm(listing_url),
            "Keywords": ", ".join(tags[:10]) if tags else "",
        }
        pins.append(pin)

        board_counts[board] = board_counts.get(board, 0) + 1

    # Preview mode
    if preview:
        print(f"{'─' * 60}")
        print(f"PREVIEW — {len(pins)} pins would be created:\n")
        for pin in pins:
            print(f"  [{pin['Pinterest board']}]")
            print(f"    Title: {pin['Title'][:70]}")
            print(f"    Image: ...{pin['Media URL'][-50:]}")
            print(f"    Link:  {pin['Link'][:70]}")
            print()
    else:
        # Write Pinterest CSV
        # Pinterest needs: Title, Media URL, Pinterest board, Description, Link, Keywords
        fieldnames = ["Title", "Media URL", "Pinterest board", "Description", "Link", "Keywords"]

        # Handle batching if > 200 pins
        if len(pins) <= 200:
            batches = [pins]
            batch_paths = [output_path]
        else:
            batches = [pins[i : i + 200] for i in range(0, len(pins), 200)]
            base, ext = os.path.splitext(output_path)
            batch_paths = [f"{base}_batch{i + 1}{ext}" for i in range(len(batches))]

        for batch, path in zip(batches, batch_paths):
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(batch)
            print(f"  Wrote {len(batch)} pins → {os.path.basename(path)}")

    # Summary
    print(f"\n{'─' * 60}")
    print(f"  Total pins:  {len(pins)}")
    print(f"  Skipped:     {skipped}")
    if len(pins) > 200:
        print(f"  Batches:     {len(batches)} files (Pinterest max 200 per upload)")
    print(f"\n  Pins per board:")
    for board, count in sorted(board_counts.items(), key=lambda x: -x[1]):
        print(f"    {board}: {count}")
    print(f"{'─' * 60}")

    if not preview:
        print(f"\nNext steps:")
        print(f"  1. Log into Pinterest (desktop only)")
        print(f"  2. Click menu → Settings → Import content")
        print(f"  3. Upload: {', '.join(os.path.basename(p) for p in batch_paths)}")
        if len(pins) > 200:
            print(f"  4. Upload each batch file one at a time")
        print(f"\n  Pinterest will process and create all pins automatically.")
        print(f"  You'll get a confirmation email when done.")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Etsy listing CSV to Pinterest bulk upload CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "How to get your Etsy CSV:\n"
            "  1. Etsy.com → Shop Manager → Settings → Options\n"
            "  2. Click 'Download Data' tab\n"
            "  3. Click 'Download CSV' under 'Currently for Sale Listings'\n\n"
            "Then run:\n"
            "  python3 etsy_csv_to_pinterest.py EtsyListingsDownload.csv\n"
        ),
    )
    parser.add_argument("input", help="Path to Etsy CSV export file")
    parser.add_argument("-o", "--output", help="Output CSV path (default: pinterest_pins.csv)")
    parser.add_argument("--preview", action="store_true", help="Preview without writing CSV")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: File not found: {args.input}")
        sys.exit(1)

    output = args.output or os.path.join(SCRIPT_DIR, "pinterest_pins.csv")
    convert(args.input, output, preview=args.preview)


if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    main()
