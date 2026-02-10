#!/usr/bin/env python3
"""
Auto-update sitemap.xml lastmod dates based on git commit history.
Run this before committing/pushing to keep sitemap dates accurate.

Usage: python3 scripts/update_sitemap.py
"""

import subprocess
import re
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent
SITEMAP_PATH = REPO_ROOT / "sitemap.xml"


def get_last_commit_date(filepath: str) -> str:
    """Get the last git commit date for a file in YYYY-MM-DD format."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", filepath],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        if result.stdout.strip():
            # Parse ISO date and return YYYY-MM-DD
            date_str = result.stdout.strip()
            return date_str[:10]
    except Exception:
        pass
    # Fallback to today's date
    return datetime.now().strftime("%Y-%m-%d")


def update_sitemap():
    """Read sitemap.xml and update lastmod dates from git history."""
    content = SITEMAP_PATH.read_text()

    # Find all <loc>...</loc> and <lastmod>...</lastmod> pairs
    loc_pattern = re.compile(
        r"(<loc>https://fixthevuln\.com/([^<]*)</loc>\s*\n\s*<lastmod>)(\d{4}-\d{2}-\d{2})(</lastmod>)"
    )

    updated = 0
    def replace_date(match):
        nonlocal updated
        prefix = match.group(1)
        page_path = match.group(2)
        old_date = match.group(3)
        suffix = match.group(4)

        # Map URL path to file path
        if page_path == "" or page_path == "/":
            filepath = "index.html"
        else:
            filepath = page_path.lstrip("/")

        new_date = get_last_commit_date(filepath)

        if new_date != old_date:
            updated += 1
            print(f"  {filepath}: {old_date} -> {new_date}")

        return f"{prefix}{new_date}{suffix}"

    new_content = loc_pattern.sub(replace_date, content)

    if updated > 0:
        SITEMAP_PATH.write_text(new_content)
        print(f"\nUpdated {updated} lastmod dates in sitemap.xml")
    else:
        print("All sitemap dates are already current.")


if __name__ == "__main__":
    print("Updating sitemap.xml lastmod dates from git history...\n")
    update_sitemap()
