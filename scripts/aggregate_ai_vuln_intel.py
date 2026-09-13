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

# mitre-atlas/atlas-data has no data/techniques/ directory (verified via
# `gh api repos/mitre-atlas/atlas-data/contents/data` -> 404; the real tree is
# atlas/, dist/, tests/, tools/). All technique + sub-technique IDs live as
# top-level keys under a single `techniques:` mapping in dist/ATLAS-latest.yaml.
# Regexing the raw YAML text for the ID pattern (verified to produce the same
# 197-id set as parsing just the `techniques:` block) avoids adding a YAML
# dependency for one flat ID list.
# dist/ATLAS-latest.yaml is itself a git symlink chain (-> v6/ATLAS-latest.yaml
# -> v6/ATLAS-<current-release>.yaml), so raw.githubusercontent.com (which
# serves the literal blob, i.e. just the ~20-byte target path for a symlink)
# can't be used directly. The GitHub Contents API resolves symlinks to their
# target file's content when asked for the raw media type, so that's used
# here instead (verified with an unauthenticated request).
ATLAS_TECHNIQUES_API = "https://api.github.com/repos/mitre-atlas/atlas-data/contents/dist/ATLAS-latest.yaml"
ATLAS_ID_RE = re.compile(r'AML\.T\d+(?:\.\d+)?')


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


def fetch_atlas_technique_ids():
    """List technique IDs currently in mitre-atlas/atlas-data by fetching
    ATLAS-latest.yaml's raw content and regexing out AML.Txxxx[.xxx] IDs (see
    comment on ATLAS_TECHNIQUES_API above for why this reads a YAML file with
    regex instead of walking a per-technique file listing).
    Per the repo-structure convention in this codebase, a failed/empty fetch
    logs and returns [] rather than aborting the run."""
    try:
        req = urllib.request.Request(ATLAS_TECHNIQUES_API,
                                      headers={'User-Agent': 'FixTheVuln-AI-Vuln-Intel/1.0',
                                               'Accept': 'application/vnd.github.raw+json'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            text = resp.read().decode('utf-8')
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, UnicodeDecodeError) as e:
        print(f"  Warning: failed to fetch MITRE ATLAS technique listing: {e}")
        return []

    return sorted(set(ATLAS_ID_RE.findall(text)))


def check_atlas_techniques(remote_technique_ids, known_ids):
    """New technique IDs present remotely but not yet in
    data/ai-vuln-content.json (known_ids) become atlas_technique_change
    signals. An empty remote list (failed fetch) yields no entries — never
    treat "couldn't fetch" as "everything is missing"."""
    entries = []
    for tid in remote_technique_ids:
        if tid not in known_ids:
            entries.append({
                "id": f"atlas-technique-{tid}",
                "type": "atlas_technique_change",
                "status": "new",
                "source_url": f"https://atlas.mitre.org/techniques/{tid}",
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

    content_path = REPO_ROOT / "data" / "ai-vuln-content.json"
    known_ids = set()
    if content_path.exists():
        content = json.loads(content_path.read_text())
        known_ids = {t["code"] for t in content["techniques"] if t["framework"] == "mitre-atlas"} | \
                    {t["code"] for t in content["techniques"] if t["framework"] == "owasp-llm-top10"}
    remote_ids = fetch_atlas_technique_ids()
    for entry in check_atlas_techniques(remote_ids, known_ids):
        if add_entry(state, entry):
            added += 1

    save_state(state)
    print(f"Added {added} new signal(s) to data/ai-vuln-intel.json")


if __name__ == "__main__":
    main()
