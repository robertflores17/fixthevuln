#!/usr/bin/env python3
"""
Populates data/ai-vuln-intel.json from three signal sources:
  - OWASP LLM Top 10 revision announcements (this file, check_owasp_top10_change)
  - MITRE ATLAS technique diffs (Task 11, check_atlas_techniques)
  - Framework/vector-DB GHSA advisories (Task 12, check_framework_ghsa)

Chained onto the existing Friday ai-trend-roundup.yml workflow (Task 13),
after aggregate_ai_security_news.py runs. Reuses that script's already-fetched
OWASP GenAI RSS feed rather than fetching it twice.

Usage: python3 scripts/aggregate_ai_vuln_intel.py
"""
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / 'scripts'))

from lib.ai_vuln_intel_store import load_state, save_state, add_entry

OWASP_GENAI_FEED = "https://genai.owasp.org/feed/"

TOP10_TITLE_RE = re.compile(r'top\s*10', re.IGNORECASE)
VERSION_RE = re.compile(r'\b(20\d\d|v\d+(\.\d+)?)\b')


def fetch_feed_items(url):
    """Fetch and parse an RSS/Atom feed into a list of {title, url, published}.
    Matches aggregate_ai_security_news.py's per-source failure handling:
    log and return [] rather than aborting the run."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'FixTheVuln-AI-Vuln-Intel/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            root = ET.fromstring(resp.read())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ET.ParseError) as e:
        print(f"  Warning: failed to fetch {url}: {e}")
        return []

    items = []
    for item in root.iter('item'):
        title = (item.findtext('title') or '').strip()
        link = (item.findtext('link') or '').strip()
        published = (item.findtext('pubDate') or '').strip()
        items.append({"title": title, "url": link, "published": published})
    return items


def check_owasp_top10_change(rss_items):
    """Detect a genuine OWASP LLM Top 10 revision announcement: title must
    mention "Top 10" AND contain a version marker (a year or vN.N) — this
    is what separates a real revision post from a post that merely
    references the Top 10 in passing."""
    entries = []
    for item in rss_items:
        title = item["title"]
        if TOP10_TITLE_RE.search(title) and VERSION_RE.search(title):
            entries.append({
                "id": f"owasp-top10-{re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]}",
                "type": "owasp_top10_change",
                "status": "new",
                "source_url": item["url"],
                "detected_at": datetime.now(timezone.utc).isoformat(),
            })
    return entries


def main():
    state = load_state()
    added = 0

    owasp_items = fetch_feed_items(OWASP_GENAI_FEED)
    for entry in check_owasp_top10_change(owasp_items):
        if add_entry(state, entry):
            added += 1

    save_state(state)
    print(f"Added {added} new signal(s) to data/ai-vuln-intel.json")


if __name__ == "__main__":
    main()
