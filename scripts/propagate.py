#!/usr/bin/env python3
"""Notify search engines of new/updated pages on fixthevuln.com.

Submission method:
  IndexNow — batch POST to api.indexnow.org (reaches Bing, Yandex, DuckDuckGo, Seznam, Naver)

Changed URL detection uses `git diff` to find HTML/XML files modified since last run.

Usage:
    python3 scripts/propagate.py                 # submit changed URLs since last run
    python3 scripts/propagate.py --full           # submit all sitemap URLs (initial seeding)
    python3 scripts/propagate.py --dry-run        # preview what would be submitted
    python3 scripts/propagate.py --generate-llms  # also regenerate llms.txt files

stdlib only: urllib.request, json, xml.etree.ElementTree, subprocess, argparse
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP_PATH = os.path.join(SITE_ROOT, "sitemap.xml")
LOG_PATH = os.path.join(SITE_ROOT, "data", ".propagation-log.json")
BASE_URL = "https://fixthevuln.com"
INDEXNOW_KEY = "5a07bd052d536ad031adb837450259ce"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
INDEXNOW_BATCH_SIZE = 10000

# File extensions that map to site URLs
TRACKABLE_EXTENSIONS = {".html", ".xml"}

# Files at site root that map directly to URLs
ROOT_SPECIAL_FILES = {"robots.txt", "llms.txt", "llms-full.txt", "sitemap.xml"}


def parse_sitemap(sitemap_path):
    """Parse sitemap.xml and return list of URLs."""
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for url_elem in root.findall("sm:url", ns):
        loc = url_elem.find("sm:loc", ns)
        if loc is not None and loc.text:
            urls.append(loc.text.strip())
    return urls


def load_log():
    """Load propagation log from disk."""
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            return json.load(f)
    return {"last_run": None, "last_commit": None, "total_submissions": 0, "runs": []}


def save_log(log):
    """Save propagation log to disk."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)


def get_current_commit():
    """Get current HEAD commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=SITE_ROOT
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except FileNotFoundError:
        return None


def get_changed_files(since_commit):
    """Get files changed between since_commit and HEAD."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", since_commit, "HEAD"],
            capture_output=True, text=True, cwd=SITE_ROOT
        )
        if result.returncode == 0:
            return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        return []
    except FileNotFoundError:
        return []


def file_to_url(filepath):
    """Convert a repo file path to its public URL, or None if not mappable."""
    # Normalize path separators
    filepath = filepath.replace("\\", "/")

    # Root special files
    basename = os.path.basename(filepath)
    if basename in ROOT_SPECIAL_FILES and "/" not in filepath:
        return f"{BASE_URL}/{basename}"

    # Check extension
    _, ext = os.path.splitext(filepath)
    if ext not in TRACKABLE_EXTENSIONS:
        return None

    # Skip template/data files
    if filepath.startswith("data/") or filepath.startswith("scripts/"):
        return None
    if filepath == "data/kev_cards.html":
        return None

    # Map file path to URL
    return f"{BASE_URL}/{filepath}"


def detect_changed_urls(since_commit):
    """Detect URLs that changed since a given commit."""
    changed_files = get_changed_files(since_commit)
    urls = set()
    for f in changed_files:
        url = file_to_url(f)
        if url:
            urls.add(url)
    return sorted(urls)


def submit_indexnow(urls, dry_run=False):
    """Submit URLs to IndexNow API (batch endpoint)."""
    if not urls:
        print("IndexNow: No URLs to submit")
        return True

    # Process in batches
    total_submitted = 0
    for i in range(0, len(urls), INDEXNOW_BATCH_SIZE):
        batch = urls[i : i + INDEXNOW_BATCH_SIZE]
        payload = {
            "host": "fixthevuln.com",
            "key": INDEXNOW_KEY,
            "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
            "urlList": batch,
        }

        if dry_run:
            print(f"IndexNow: Would submit {len(batch)} URLs (batch {i // INDEXNOW_BATCH_SIZE + 1})")
            total_submitted += len(batch)
            continue

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            INDEXNOW_ENDPOINT,
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                status = resp.status
                print(f"IndexNow: Submitted {len(batch)} URLs — HTTP {status}")
                total_submitted += len(batch)
        except urllib.error.HTTPError as e:
            # 200 = OK, 202 = Accepted (both are success)
            if e.code in (200, 202):
                print(f"IndexNow: Submitted {len(batch)} URLs — HTTP {e.code}")
                total_submitted += len(batch)
            else:
                print(f"IndexNow: Error HTTP {e.code} — {e.read().decode('utf-8', errors='replace')}")
                return False
        except Exception as e:
            print(f"IndexNow: Error — {e}")
            return False

    print(f"IndexNow: Total submitted: {total_submitted}")
    return True



def main():
    parser = argparse.ArgumentParser(description="Notify search engines of site updates")
    parser.add_argument("--dry-run", action="store_true", help="Preview without submitting")
    parser.add_argument("--full", action="store_true", help="Submit all sitemap URLs (initial seeding)")
    parser.add_argument("--generate-llms", action="store_true", help="Regenerate llms.txt files first")
    args = parser.parse_args()

    # Optionally regenerate llms.txt
    if args.generate_llms:
        print("Regenerating llms.txt files...")
        result = subprocess.run(
            [sys.executable, os.path.join(SITE_ROOT, "scripts", "generate_llms_txt.py")],
            cwd=SITE_ROOT,
        )
        if result.returncode != 0:
            print("Warning: llms.txt generation failed", file=sys.stderr)
        print()

    log = load_log()

    if args.full:
        # Submit all sitemap URLs
        if not os.path.exists(SITEMAP_PATH):
            print(f"Error: sitemap.xml not found at {SITEMAP_PATH}", file=sys.stderr)
            sys.exit(1)
        urls = parse_sitemap(SITEMAP_PATH)
        print(f"Full submission: {len(urls)} URLs from sitemap.xml")
    else:
        # Detect changed URLs since last run
        since_commit = log.get("last_commit")
        if not since_commit:
            print("No previous run found. Use --full for initial seeding.")
            print("Or run once with --full to establish baseline, then incremental after.")
            sys.exit(0)

        current_commit = get_current_commit()
        if current_commit == since_commit:
            print("No new commits since last propagation. Nothing to submit.")
            sys.exit(0)

        urls = detect_changed_urls(since_commit)
        if not urls:
            print(f"No trackable URL changes between {since_commit[:8]} and {current_commit[:8]}")
            # Still update log so we don't re-check
            if not args.dry_run:
                log["last_run"] = datetime.now(timezone.utc).isoformat()
                log["last_commit"] = current_commit
                save_log(log)
            sys.exit(0)

        print(f"Changed URLs since {since_commit[:8]}: {len(urls)}")

    if args.dry_run:
        print("\n--- URLs to submit ---")
        for url in urls:
            print(f"  {url}")
        print(f"\nTotal: {len(urls)}")
        print()

    # Submit to IndexNow
    submit_indexnow(urls, dry_run=args.dry_run)

    # Update log
    if not args.dry_run:
        current_commit = get_current_commit()
        run_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "commit": current_commit,
            "urls_submitted": len(urls),
            "mode": "full" if args.full else "incremental",
        }
        log["last_run"] = run_record["timestamp"]
        log["last_commit"] = current_commit
        log["total_submissions"] = log.get("total_submissions", 0) + len(urls)
        # Keep last 50 runs
        log.setdefault("runs", []).append(run_record)
        log["runs"] = log["runs"][-50:]
        save_log(log)
        print(f"\nLog updated: {LOG_PATH}")
    else:
        print("\n(Dry run — no submissions made, log not updated)")


if __name__ == "__main__":
    main()
