#!/usr/bin/env python3
"""
AI Security News Aggregator for FixTheVuln.com

Pulls RSS/Atom feeds from authoritative AI security sources, dedupes against a
local seen-cache, and emits a weekly markdown digest with full source
attribution (name + link + original post URL).

Usage:
    python3 scripts/aggregate_ai_security_news.py                # Fetch + write digest
    python3 scripts/aggregate_ai_security_news.py --dry-run      # Preview, no writes
    python3 scripts/aggregate_ai_security_news.py --list-sources # Print source list and exit
    python3 scripts/aggregate_ai_security_news.py --days 14      # Lookback window (default 7)

Design:
  - stdlib only (urllib + xml.etree + json) — no new deps
  - Resilient: per-source HTTP/parse failures are logged, never fatal
  - Dedup cache: data/ai_news_seen.json (hashes of item URLs)
  - Output: drafts/ai-security-roundup-YYYY-MM-DD.md + data/ai-security-trends.json
  - Attribution: every item shows Source (with site link) AND the original URL
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import quote, urlparse
from xml.etree import ElementTree as ET


# ─── Source registry ──────────────────────────────────────────────────────────
# Edit this list to add/remove sources. Keep attribution fields populated —
# every item emitted in the digest credits `name` + `site` so creators get credit.
SOURCES = [
    {
        'name': 'OWASP GenAI Security Project',
        'site': 'https://genai.owasp.org/',
        'feed': 'https://genai.owasp.org/feed/',
        'category': 'standards',
    },
    {
        'name': 'Simon Willison',
        'site': 'https://simonwillison.net/',
        'feed': 'https://simonwillison.net/atom/everything/',
        'category': 'prompt-injection',
        # His feed is everything he posts (games, music, release notes); keep security posts only.
        # Whole-word match (no stemming), so inflected forms are listed explicitly.
        'filter_keywords': ['prompt injection', 'prompt injections', 'injection', 'injections',
                            'jailbreak', 'jailbreaks', 'vulnerability', 'vulnerabilities',
                            'exploit', 'exploits', 'exfiltrate', 'exfiltrates', 'exfiltrated',
                            'exfiltration', 'security', 'cve', 'malware', 'attack', 'attacks',
                            'attacked', 'attacker', 'sandbox', 'sandbox escape', 'supply chain',
                            'compromise', 'compromised', 'compromising', 'backdoor', 'poisoning',
                            'zero-day', 'hack', 'hacked', 'hackers', 'hacking',
                            'leaking', 'lethal trifecta', 'mcp', 'guardrail', 'guardrails',
                            'red team', 'red teaming', 'worm', 'worming', 'lockdown mode',
                            'tricked', 'secrets', 'intrusion', 'cyberattack', 'cyberattacks',
                            'cyber attack', 'cyber attacks', 'steal', 'stealing', 'stole',
                            'runaway', 'unsanctioned'],
    },
    {
        'name': 'arXiv cs.CR',
        'site': 'https://arxiv.org/list/cs.CR/recent',
        'feed': 'http://export.arxiv.org/rss/cs.CR',
        'category': 'research',
        'filter_keywords': ['llm', 'agent', 'prompt', 'gpt', 'diffusion', 'jailbreak',
                            'adversarial', 'generative', 'rag', 'machine learning',
                            'neural', 'alignment', 'fine-tune', 'fine-tuned', 'fine-tuning'],
    },
    # NOTE: Protect AI's feed returned 404 at every plausible URL on 2026-10-25, so it was removed.
    # HiddenLayer, Lakera, Anthropic, and MITRE ATLAS do not publish
    # stable public RSS feeds at well-known URLs (all returned 404 on last
    # probe). Leaving them out rather than shipping dead links. If/when they
    # publish feeds, add entries here with the correct URL.
    {
        'name': 'Google Project Zero',
        'site': 'https://googleprojectzero.blogspot.com/',
        # /summary, not /default: the default feed is every post ever (11 MB); summary is about 16 KB.
        'feed': 'https://googleprojectzero.blogspot.com/feeds/posts/summary?max-results=25',
        'category': 'research',
        'filter_keywords': ['ai', 'ml', 'llm', 'model', 'agent', 'prompt'],
    },
    {
        'name': 'CISA Cybersecurity Advisories',
        'site': 'https://www.cisa.gov/news-events/cybersecurity-advisories',
        # all.xml is 5.7 MB (mostly ICS advisories); this joint-advisory feed is about 1.4 MB.
        'feed': 'https://www.cisa.gov/cybersecurity-advisories/cybersecurity-advisories.xml',
        'category': 'government',
        'filter_keywords': ['ai', 'artificial intelligence', 'ml', 'llm', 'model',
                            'langflow', 'ollama', 'pytorch', 'tensorflow'],
    },
    {
        'name': 'NIST Cybersecurity News',
        'site': 'https://www.nist.gov/cybersecurity',
        'feed': 'https://www.nist.gov/news-events/cybersecurity/rss.xml',
        'category': 'standards',
        'filter_keywords': ['ai', 'artificial intelligence', 'generative', 'ml',
                            'model', 'llm'],
    },
    {
        'name': 'Hacker News (AI Security)',
        'site': 'https://news.ycombinator.com/',
        'feed': 'https://hnrss.org/newest?q=%22AI+security%22+OR+%22prompt+injection%22+OR+%22LLM+vulnerability%22&points=20',
        'category': 'community',
    },
]


# ─── Feed fetching ────────────────────────────────────────────────────────────

USER_AGENT = 'FixTheVuln-AISecurityAggregator/1.0 (+https://fixthevuln.com)'
HTTP_TIMEOUT = 20  # seconds
MAX_ITEMS_PER_SOURCE = 25  # cap to keep digest sane
MAX_FEED_BYTES = 2_000_000  # cap raw feed size before parsing


def fetch_feed(url: str) -> bytes | None:
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml, */*'})
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            raw = resp.read(MAX_FEED_BYTES + 1)
        if len(raw) > MAX_FEED_BYTES:
            # Truncating here used to cut the XML mid-document and the source silently yielded 0 items.
            print(f'    [fetch-error] {url}: feed over {MAX_FEED_BYTES} bytes, skipped (use a smaller feed URL)', file=sys.stderr)
            return None
        return raw
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print(f'    [fetch-error] {url}: {e}', file=sys.stderr)
        return None


def _strip_ns(tag: str) -> str:
    return tag.split('}', 1)[1] if '}' in tag else tag


def _find_first(el, *local_names):
    for child in el.iter():
        if _strip_ns(child.tag) in local_names:
            return child
    return None


def _text(el) -> str:
    if el is None:
        return ''
    return (el.text or '').strip()


def parse_feed(raw: bytes, source: dict, errors: list | None = None) -> list[dict]:
    """Parse RSS 2.0 or Atom. Returns normalized list of {title, link, summary, published}."""
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"    [parse-error] {source['feed']}: {e}", file=sys.stderr)
        if errors is not None:
            errors.append(str(e))
        return []

    items: list[dict] = []
    root_local = _strip_ns(root.tag)

    # RSS 2.0: <rss><channel><item>...
    # Atom: <feed><entry>...
    entry_names = {'item', 'entry'}
    for el in root.iter():
        if _strip_ns(el.tag) not in entry_names:
            continue

        title = ''
        link = ''
        summary = ''
        published = ''

        for child in el:
            tag = _strip_ns(child.tag)
            if tag == 'title' and not title:
                title = _text(child)
            elif tag == 'link':
                href = child.attrib.get('href')
                if href:
                    link = href
                elif _text(child):
                    link = _text(child)
            elif tag in ('description', 'summary', 'content') and not summary:
                summary = _text(child)
            elif tag in ('pubDate', 'published', 'updated') and not published:
                published = _text(child)

        # Only web links: feed text is untrusted and would otherwise reach an href as-is.
        if not title or not link or urlparse(link).scheme not in ('http', 'https'):
            continue

        items.append({
            'title': title,
            'link': link,
            'summary': _clean_html(summary)[:500],
            'published': published,
            'published_dt': _parse_date(published),
        })

        if len(items) >= MAX_ITEMS_PER_SOURCE:
            break

    return items


_HTML_TAG_RE = re.compile(r'<[^<>]*>')  # no backtracking on unclosed '<'
_WS_RE = re.compile(r'\s+')
_ARXIV_PREFIX_RE = re.compile(r'^arXiv:\S+ Announce Type: \S+ Abstract: ?')


def _md_text(s: str) -> str:
    """HTML-escape feed text, then escape markdown punctuation so the publisher cannot build links or emphasis from it."""
    s = html.escape(s, quote=True)
    for ch, ent in (('[', '&#91;'), (']', '&#93;'), ('(', '&#40;'), (')', '&#41;'),
                    ('*', '&#42;'), ('_', '&#95;'), ('`', '&#96;')):
        s = s.replace(ch, ent)
    return s


def _strip_em_dash(s: str) -> str:
    return re.sub(r' ?— ?', ', ', s)


def _clean_html(s: str) -> str:
    if not s:
        return ''
    s = _HTML_TAG_RE.sub('', s)
    # Decode every entity once (named, &#39;, &#x27;) so _md_text escapes exactly once later.
    s = html.unescape(_WS_RE.sub(' ', s))
    # Em-dashes are banned in consumer-facing copy (anti-AI-tell rule); feeds send them as entities
    # or literals, so strip after decoding. Whitespace is already collapsed, so no backtracking.
    s = _strip_em_dash(s)
    # Feeds sometimes drop the space after a sentence ("Hacker News.I'm").
    s = re.sub(r'([a-z]{2})\.([A-Z])', r'\1. \2', s)
    s = _WS_RE.sub(' ', s).strip()
    # arXiv RSS prefixes every abstract with "arXiv:<id> Announce Type: <kind> Abstract:".
    return _ARXIV_PREFIX_RE.sub('', s)


def _parse_date(s: str) -> datetime | None:
    if not s:
        return None
    s = s.strip()
    try:
        dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (TypeError, ValueError):
        pass
    for fmt in ('%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d'):
        try:
            dt = datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def _item_matches_filter(item: dict, keywords: list[str] | None) -> bool:
    if not keywords:
        return True
    blob = (item['title'] + ' ' + item['summary']).lower()
    for kw in keywords:
        kw = kw.lower().strip()
        if not kw:
            continue
        pattern = r'\b' + re.escape(kw) + (r'' if kw.endswith('-') else r'\b')
        if re.search(pattern, blob):
            return True
    return False


def _item_id(source: dict, item: dict) -> str:
    key = f"{source['name']}|{item['link']}".encode('utf-8')
    return hashlib.sha1(key).hexdigest()[:16]


# ─── Digest building ──────────────────────────────────────────────────────────

CATEGORY_ORDER = [
    ('standards', 'Standards & Frameworks'),
    ('government', 'Government Advisories'),
    ('frontier-lab', 'Frontier Lab Disclosures'),
    ('vendor-research', 'Vendor Research'),
    ('research', 'Academic & Research'),
    ('prompt-injection', 'Prompt Injection & LLM Security'),
    ('community', 'Community Signal'),
]


def build_digest(grouped: dict, cutoff_dt: datetime, today: datetime) -> str:
    week_start = (today - timedelta(days=7)).strftime('%b %d')
    week_end = today.strftime('%b %d, %Y')
    total = sum(len(v) for v in grouped.values())
    # Name only the sources that produced items, not every configured feed.
    contributing = list(dict.fromkeys(e['source']['name'] for v in grouped.values() for e in v))
    source_names = ', '.join(contributing)
    iso_date = today.strftime('%Y-%m-%d')
    slug = f'ai-security-roundup-{iso_date}'

    lines: list[str] = []
    # Frontmatter — required by scripts/publish_editorial.py to convert to blog post.
    lines.append('---')
    lines.append(f'title: "AI Security Trend Roundup: {week_end}"')
    lines.append(f'description: "{total} AI security update{"" if total == 1 else "s"} from {source_names}, covering {week_start}–{today.strftime("%b %d")}. Every item credited to its original author."')
    lines.append('keywords: "AI security, LLM security, prompt injection, agentic AI, GenAI threats, AI vulnerabilities, AI red team"')
    # No `date:` field here deliberately: publish_editorial.py's setdefault() stamps the page
    # with the day it goes live. ai-trend-roundup.yml publishes right after this runs, so that
    # is the aggregation day; the week covered is stated in the title and body copy.
    lines.append(f'slug: "{slug}"')
    lines.append('author: "FixTheVuln Team"')
    lines.append(f'sources: "{source_names}"')
    # Machine-built digest: the publisher omits the byline so no editorial role is implied.
    lines.append('auto_digest: "true"')
    lines.append('cta_section: "comptia"')
    lines.append('---')
    lines.append('')
    lines.append(f'# AI Security Trend Roundup: {week_end}')
    lines.append('')
    n_src = len(contributing)
    lines.append(f"*Covering {week_start} → {week_end}. {total} new item{'' if total == 1 else 's'} from {n_src} source{'' if n_src == 1 else 's'}.*")
    lines.append('')
    lines.append('> This digest credits every source by name and links directly to each original post. '
                 'Items are selected automatically by keyword and feed filters. All rights and attribution belong to the original authors.')
    lines.append('')

    for cat_key, cat_title in CATEGORY_ORDER:
        items = grouped.get(cat_key, [])
        if not items:
            continue
        lines.append(f'## {cat_title}')
        lines.append('')
        for entry in items:
            src = entry['source']
            it = entry['item']
            pub = it['published_dt'].strftime('%b %d') if it.get('published_dt') else it.get('published', '')[:16]
            # Feed text is untrusted and the publisher emits this markdown as raw HTML, so escape it here.
            title = _md_text(_strip_em_dash(it['title']))
            href = quote(it['link'], safe=":/?#[]@!$&'*+,;=%~-._")
            lines.append(f"- **[{title}]({href})**  ")
            credit = f"  Source: [{src['name']}]({src['site']})"
            if pub:
                credit += f', {_md_text(pub)}.'
            lines.append(credit)
            if it.get('summary'):
                lines.append(f"  {_md_text(it['summary'][:280])}")
            lines.append('')
        lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('## Source List')
    lines.append('')
    lines.append('Sources in this roundup, credited to their original authors/organizations:')
    lines.append('')
    for s in SOURCES:
        if s['name'] not in contributing:
            continue
        lines.append(f"- [{s['name']}]({s['site']}), feed: `{s['feed']}`")
    lines.append('')
    return '\n'.join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────

def carry_framework_advisories(existing, digest):
    """Keep a "## Framework Advisories" section the AI Vuln Intel Reviewer routine
    already appended to this week's draft. Without this, regenerating the draft
    overwrote it: 19 published advisories were lost this way (Sep 18, Oct 09)."""
    m = re.search(r"^## Framework Advisories\n.*?(?=^## |\Z)", existing, re.M | re.S)
    if not m or "## Framework Advisories" in digest or "## Source List" not in digest:
        return digest
    return digest.replace("## Source List", m.group(0).rstrip("\n") + "\n\n## Source List", 1)


def report_source_health(source_stats):
    """Say which sources produced nothing and why, so a dead or truncated feed is not silent."""
    live = [s for s in source_stats if s['status'] == 'ok' and s['parsed'] > 0]
    broken = [f"{s['source']} ({s['status']})" for s in source_stats if s['status'] != 'ok']
    empty = [s['source'] for s in source_stats if s['status'] == 'ok' and s['parsed'] == 0]
    lines = [f'sources_with_items={len(live)}/{len(source_stats)}']
    if broken:
        lines.append('BROKEN: ' + ', '.join(broken))
    if empty:
        lines.append('empty (can be legitimate, e.g. arXiv on weekends): ' + ', '.join(empty))
    for line in lines:
        print('  ' + line)
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a', encoding='utf-8') as f:
            f.write('### AI roundup source health\n' + '\n'.join(f'- {l}' for l in lines) + '\n')
    return len(live)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Preview; write nothing')
    parser.add_argument('--list-sources', action='store_true', help='Print sources and exit')
    parser.add_argument('--days', type=int, default=7, help='Lookback window in days (default 7)')
    args = parser.parse_args()

    if args.list_sources:
        for s in SOURCES:
            print(f"{s['name']:<38} {s['category']:<18} {s['feed']}")
        return 0

    repo_root = Path(__file__).resolve().parent.parent
    data_dir = repo_root / 'data'
    drafts_dir = repo_root / 'drafts'
    data_dir.mkdir(exist_ok=True)
    drafts_dir.mkdir(exist_ok=True)

    seen_path = data_dir / 'ai_news_seen.json'
    trends_path = data_dir / 'ai-security-trends.json'

    seen: dict = json.loads(seen_path.read_text(encoding='utf-8')) if seen_path.exists() else {}

    today = datetime.now(timezone.utc)
    cutoff = today - timedelta(days=args.days)

    grouped: dict = {}
    source_stats: list[dict] = []
    new_seen: dict = {}

    for source in SOURCES:
        name = source['name']
        print(f'→ {name}')
        raw = fetch_feed(source['feed'])
        if raw is None:
            source_stats.append({'source': name, 'status': 'fetch-failed', 'count': 0})
            continue

        parse_errors: list = []
        items = parse_feed(raw, source, parse_errors)
        kept = 0
        for it in items:
            if not _item_matches_filter(it, source.get('filter_keywords')):
                continue
            pub_dt = it.get('published_dt')
            if pub_dt and pub_dt < cutoff:
                continue

            iid = _item_id(source, it)
            new_seen[iid] = {
                'source': name,
                'title': it['title'],
                'link': it['link'],
                'first_seen': today.isoformat(),
            }
            if iid in seen:
                continue

            grouped.setdefault(source['category'], []).append({
                'source': source,
                'item': it,
                'id': iid,
            })
            kept += 1

        status = 'parse-failed' if parse_errors else 'ok'
        source_stats.append({'source': name, 'status': status, 'count': kept, 'parsed': len(items)})
        print(f'    parsed={len(items)}  new={kept}')

    for cat in grouped:
        grouped[cat].sort(key=lambda e: e['item'].get('published_dt') or datetime.min.replace(tzinfo=timezone.utc), reverse=True)

    report_source_health(source_stats)
    total_new = sum(len(v) for v in grouped.values())
    print(f'\nTotal new items: {total_new}')

    if total_new == 0:
        print('  Nothing new this week — skipping digest write.')
        if not args.dry_run:
            merged = {**seen, **new_seen}
            seen_path.write_text(json.dumps(merged, indent=2), encoding='utf-8')
        return 0

    digest = build_digest(grouped, cutoff, today)
    digest_path = drafts_dir / f"ai-security-roundup-{today.strftime('%Y-%m-%d')}.md"

    trends_payload = {
        'generated_at': today.isoformat(),
        'window_days': args.days,
        'total_items': total_new,
        'by_category': {
            cat: [
                {
                    'source': e['source']['name'],
                    'source_url': e['source']['site'],
                    'title': e['item']['title'],
                    'url': e['item']['link'],
                    'published': e['item'].get('published', ''),
                    'summary': e['item'].get('summary', ''),
                }
                for e in entries
            ]
            for cat, entries in grouped.items()
        },
        'source_stats': source_stats,
    }

    if args.dry_run:
        print('\n--- DIGEST PREVIEW ---')
        print(digest[:2000])
        print('...(truncated)')
        return 0

    if digest_path.exists():
        digest = carry_framework_advisories(digest_path.read_text(encoding='utf-8'), digest)
    digest_path.write_text(digest, encoding='utf-8')
    trends_path.write_text(json.dumps(trends_payload, indent=2), encoding='utf-8')
    merged = {**seen, **new_seen}
    seen_path.write_text(json.dumps(merged, indent=2), encoding='utf-8')

    print(f'\n✓ Digest:  {digest_path.relative_to(repo_root)}')
    print(f'✓ Trends:  {trends_path.relative_to(repo_root)}')
    print(f'✓ Seen:    {seen_path.relative_to(repo_root)} ({len(merged)} entries)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
