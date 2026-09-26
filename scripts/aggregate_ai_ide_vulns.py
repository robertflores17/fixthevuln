#!/usr/bin/env python3
"""
Collects AI IDE / MCP vulnerability disclosures into data/ai-ide-vulns.json,
which feeds the live tracker block in
blog/ai-ide-security-vulnerabilities-2026.html.

Three sources, all stdlib-only:
  - NVD keyword search, filtered by *publication* date
  - GitHub Security Advisories for MCP server + AI coding agent repos
  - CISA KEV entries already on disk (data/kev-data.json), no extra fetch

Why pubStartDate and not lastModStartDate: NVD re-enriches ancient CVEs, so a
lastMod window returns 2002-era ncurses and Windows .ANI bugs for the keyword
"cursor". Filtering on publication date collapsed the "zed" result set from 28
to 6 and dropped every pre-2025 false positive.

Why the two-gate relevance filter on top: a pub-date window alone still leaves
69 hits for "cursor", because database cursors and kernel cursors exist. An
entry is kept only if its text names a tracked product AND carries AI-tooling
context. See is_relevant().

Usage: python3 scripts/aggregate_ai_ide_vulns.py [--days 120]
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import http.client
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / 'scripts'))

from aggregate_ai_vuln_intel import fetch_ghsa_advisories, _parse_ghsa_date
from fetch_kev import _validate_nvd_key, cvss_from_metrics

DATA_DIR = REPO_ROOT / "data"
STATE_FILE = DATA_DIR / "ai-ide-vulns.json"
ARCHIVE_FILE = DATA_DIR / "ai-ide-vulns-archive.json"
KEV_DATA_FILE = DATA_DIR / "kev-data.json"

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_KEY = os.environ.get('NVD_API_KEY', '')
# Same limits fetch_kev.py works to: 5 req/30s anonymous, 50 req/30s with key.
NVD_DELAY_WITH_KEY = 0.6
NVD_DELAY_ANON = 6.0
# NVD rejects a pub window wider than 120 days.
MAX_WINDOW_DAYS = 120
# Newest N kept. The table shows 12; the rest only feed the caption's count.
# Without a cap this file is committed daily and grows without bound. The cap
# sits far outside the 120-day collection window, so a pruned entry can never
# be re-collected and re-added.
MAX_STORED = 500

# Exact-match phrases. Single ambiguous words (cursor, zed) are safe here only
# because is_relevant() gates the results afterward.
NVD_KEYWORDS = [
    "model context protocol",
    "github copilot",
    "claude code",
    "cursor",
    "windsurf",
    "cline",
    "aider",
    "zed",
    "roo code",
    "kilo code",
]

# Repos that actually publish GHSA advisories for MCP servers and AI coding
# agents. fetch_ghsa_advisories warns and returns [] per repo on failure, so a
# renamed or advisory-less repo degrades this list instead of aborting the run.
GHSA_REPOS = [
    "modelcontextprotocol/servers",
    "modelcontextprotocol/python-sdk",
    "modelcontextprotocol/typescript-sdk",
    "cline/cline",
    "RooCodeInc/Roo-Code",
    "Aider-AI/aider",
    "continuedev/continue",
    "zed-industries/zed",
    "block/goose",
]

ARXIV_RSS = "https://export.arxiv.org/rss"
RSS_NS = {'dc': 'http://purl.org/dc/elements/1.1/'}
# Researchers whose AI-agent security work this page draws on. FixTheVuln
# already credits del Rosario: the quiz-feedback analytics, entity extractor
# and vulnerability classifier are adapted from his MIT-licensed CyberMoE
# framework. Google Scholar has no API and blocks automated access, so arXiv
# is the feed that can actually be polled.
#
# This scans every cs.CR RSS item and filters locally against
# ARXIV_AUTHOR_NAMES, rather than querying export.arxiv.org/api/query with an
# au: surname search. That query endpoint answers every request from a GitHub
# Actions runner with an empty-body 406, regardless of headers (confirmed
# 2026-09-26: identical failure across three User-Agent/Accept variants) --
# while the RSS endpoint on the same domain serves Actions runners fine (it's
# what aggregate_ai_security_news.py's Friday roundup already polls). cs.CR
# submission is open to anyone, so the filter matches full names, not the
# surname alone: a different Del Rosario could otherwise put an arbitrary
# title, abstract and outbound link on this page, under a heading that names
# him. Both spellings appear on his own papers, so both are accepted.
ARXIV_AUTHOR_NAMES = ("ron f. del rosario", "ronald f. del rosario")
ARXIV_CATEGORY = "cs.CR"
MAX_RESEARCH = 20
# Hard ceiling on the arXiv response before it reaches the XML parser. A full
# day's cs.CR RSS feed measured ~80 KB for ~75 entries, so this is >10x headroom.
MAX_ARXIV_BYTES = 1_000_000


# Unambiguous product names: safe to match anywhere in the advisory text.
STRONG_PRODUCT_RE = re.compile(
    r'\b(copilot|windsurf|cline|aider|roo[\s-]?code|kilo[\s-]?code|'
    r'claude[\s-]?code|continue\.dev|mcp|model context protocol)\b', re.I)
# Product names that are also ordinary English words. Counted only in the
# subject position, i.e. the opening clause where an advisory names the
# affected product ("Cursor is a code editor built for programming with AI").
# Matching these anywhere pulled in database and kernel cursors: Semantic
# MediaWiki, node-tar, Ruby JSON and async-tar all landed in the Cursor bucket.
WEAK_PRODUCT_RE = re.compile(r'\b(cursor|zed)\b', re.I)
SUBJECT_CHARS = 80
# Plural-tolerant: an advisory saying "Claude Code extensions" must not fall
# through a pattern that only matches the singular.
CONTEXT_RE = re.compile(
    r'\b(ai|llm|agents?|agentic|mcp|model context protocol|ide|code editors?|'
    r'coding|prompt injection|extensions?)\b', re.I)

# Display names for the tracker's Vendor column, keyed by the PRODUCT_RE match.
VENDOR_NAMES = {
    'cursor': 'Cursor', 'copilot': 'GitHub Copilot', 'windsurf': 'Windsurf',
    'cline': 'Cline', 'aider': 'Aider', 'zed': 'Zed', 'roocode': 'Roo Code',
    'kilocode': 'Kilo Code', 'claudecode': 'Claude Code',
    'continue.dev': 'Continue', 'mcp': 'MCP', 'modelcontextprotocol': 'MCP',
}


def use_nvd_key():
    """True only if a key is present AND NVD accepts it. A rejected key must
    not be sent: NVD answers an unrecognised apiKey with 404, so every query
    silently returns nothing instead of erroring. Reuses fetch_kev's validator
    (single live probe, cached) rather than repeating the probe here."""
    return bool(NVD_API_KEY) and _validate_nvd_key()


# The affected product is the grammatical subject of an advisory, and NVD and
# GHSA descriptions name it in the opening clause with a small number of
# recognisable shapes. Matching a tracked name anywhere instead filed "Ruflo is
# an agent meta-harness for Claude Code and Codex" under Claude Code, and an
# Open VSX Registry marketplace bug under Windsurf: a name reached through a
# "for X" clause is context, not the affected product.
_NAME = r"[A-Za-z0-9@][\w.@/&+'-]*"
# Separator is a space only. A hyphen must never appear in both _NAME's body
# and the separator class: that makes every hyphen in a run ambiguous, giving
# a chain of n hyphens O(n^6) partitions to enumerate before the pattern can
# fail. A 144-char hyphen chain measured 0.5s, ~1.75x per 4 tokens added, so a
# ~300-byte CVE description hangs the daily job. _NAME already carries '-' in
# its body, so "roo-code" and "@zereight/mcp-gitlab" still match as one token.
_SUBJ = rf"({_NAME}(?: {_NAME}){{0,5}}?)"
SUBJECT_PATTERNS = [re.compile(x) for x in (
    rf'^(?:The\s+){{0,1}}{_SUBJ}\s*(?:,[^,]{{0,40}},)?\s+is\s+(?:an?|the)\s',
    rf'^In\s+(?:the\s+)?{_SUBJ}\s+(?:before|version|prior\s+to|through)\b',
    rf'^(?:The\s+)?{_SUBJ}\s+(?:before|version|prior\s+to|through)\b',
    rf'^(?:The\s+)?{_SUBJ}\s+v?\d+\.\d',
    rf'\b(?:discovered|found|identified|detected|exists?)\s+in\s+(?:the\s+)?{_SUBJ}\s+(?:up\s+to|prior\s+to|before|version|v?\d)',
    rf'\bin\s+(?:the\s+)?{_SUBJ}\s+(?:before|version|v?\d+\.\d)',
    # Advisories that open "X provides/contains/gives ..." instead of "X is a".
    # A closed verb set, not a general verb match: "^SUBJ <any verb>" would
    # capture the opening noun phrase of almost any sentence and start naming
    # things like "A vulnerability" as the affected product.
    rf'^(?:The\s+)?{_SUBJ}\s+(?:provides|contains|gives|implements|enables)\s',
)]
# Words a pattern can capture when an advisory opens unusually. Better to show
# nothing than to name "version" as the affected product.
SUBJECT_JUNK = {'version', 'a', 'an', 'the', 'it', 'this', 'that', 'and',
                'vulnerability', 'issue', 'all', 'some', 'use', 'flaw',
                'affected', 'crafted request', 'a crafted request', 'attacker',
                'remote attacker', 'default', 'insecure default'}


def affected_product(description):
    """The product an advisory is actually about, or '' when its opening does
    not name one clearly. Blank is deliberate: an empty cell claims nothing,
    a guessed one misattributes someone else's bug to a named IDE vendor."""
    # Only the opening clause ever names the product, so bounding the input
    # keeps worst-case matching work fixed no matter how the patterns evolve.
    text = (description or '')[:400].replace('`', '').replace('"', '')
    # Drop parentheticals before matching. Advisories routinely gloss the
    # product with its package name -- "AWS HealthLake MCP Server
    # (awslabs.healthlake-mcp-server) is a ..." -- and the subject patterns
    # cannot cross the parens, so the whole row came out blank. Bounded length
    # keeps this linear.
    text = re.sub(r'\s*\([^)]{0,80}\)', '', text)
    for pattern in SUBJECT_PATTERNS:
        m = pattern.search(text)
        if not m:
            continue
        name = m.group(1).strip(" ,.'")
        # A capture that swallowed a version clause is not a product name.
        # "mcp-security provides support ... in Spring AI. Prior to 0.1.9"
        # yielded "Spring AI. Prior to" by matching across the sentence break.
        if re.search(r'\b(prior|before|through|version)\b', name, re.I):
            continue
        # "<noun> in <Product>" is a phrase about the product, not the product.
        # "The vulnerability in Cline enables ..." would otherwise publish
        # "vulnerability in Cline", putting a real vendor's name inside a
        # fabricated one. Printing a wrong product is worse than printing none,
        # which is why this function returns '' rather than guessing.
        #
        # Only " in " is rejected, not prepositions generally: "Cursor for
        # Windows" is a real product name and "for|of|with" appear inside
        # legitimate ones. Rejecting those cost two correct captures when tried.
        if re.search(r'\bin\b', name, re.I):
            continue
        # Generic words that survive as a capture when an advisory opens with a
        # description of the flaw instead of the product.
        if name.lower() in SUBJECT_JUNK:
            continue
        # "IBM Langflow OSS 1.0.0" names one version where the advisory covers
        # 1.0.0 through 1.10.3. In an "Affected product" column that reads as
        # "1.0.0 is affected, 1.10.0 is not", which is a patching decision.
        name = re.sub(r'\s+v?\d+(?:\.\d+)*$', '', name).strip(" ,.'")
        # "WebSocket endpoint of gpt-researcher" names a component; the product
        # is what follows.
        name = re.sub(r'^(?:the\s+)?[\w-]+\s+endpoint of\s+', '', name, flags=re.I)
        if 1 < len(name) <= 60 and name.lower() not in SUBJECT_JUNK \
                and not name.lower().startswith('version'):
            return name
    return ''


def product_match(text):
    """The tracked product this advisory is about, or None. Strong names count
    anywhere; ambiguous ones only as the subject. GHSA and KEV text is built
    with the repo or title first, so their subject window works the same way."""
    return (STRONG_PRODUCT_RE.search(text)
            or WEAK_PRODUCT_RE.search(text[:SUBJECT_CHARS]))


def is_relevant(text):
    """Keep an advisory only if it names a tracked product AND reads like AI
    tooling. Either gate alone is too loose: 'zed' matches Zed Attack Proxy,
    and 'agent' matches every user-agent bug in the catalog."""
    return bool(product_match(text) and CONTEXT_RE.search(text))


# "@agenticmail/claudecode" names what the package integrates WITH, not who
# ships it. Same principle as the "for X is context" note above:
# CVE-2026-57495 is an AgenticMail advisory and was filed under Claude Code,
# which surfaced it whenever a reader searched "claude code".
SCOPED_PACKAGE_RE = re.compile(r'@[\w.-]+/[\w.-]+')


def vendor_of(text):
    # Only the vendor decision ignores scoped paths. product_match() and
    # is_relevant() still see them, so an advisory naming a tracked product
    # only inside a package path stays TRACKED; it is just not attributed
    # to that vendor.
    #
    # The strip is applied only to the strong-name search, not to the text the
    # weak-name subject window is sliced from. Stripping first and then slicing
    # text[:SUBJECT_CHARS] shortens the string, which can pull a name that was
    # previously outside the 80-char window inside it. Reproduced: a scoped
    # path early in the text pushed a later, unrelated "database cursor"
    # mention into the window and mislabelled it "Cursor" -- a new false
    # attribution introduced by fixing the old one. Windowing on the original,
    # unstripped text keeps that boundary exactly where it was before this
    # function started stripping anything.
    text = str(text or '')
    m = (STRONG_PRODUCT_RE.search(SCOPED_PACKAGE_RE.sub(' ', text))
         or WEAK_PRODUCT_RE.search(text[:SUBJECT_CHARS]))
    if not m:
        return 'Unknown'
    key = re.sub(r'[\s-]+', '', m.group(1)).lower()
    return VENDOR_NAMES.get(key, m.group(1).title())


def _cvss_from_metrics(metrics):
    """Best available CVSS base score as a string.

    Thin wrapper over fetch_kev.cvss_from_metrics, which owns the version
    precedence for the whole site. This function used to carry its own copy
    that ordered v4.0 before v2 while fetch_kev did the reverse, so one CVE
    could publish two different scores on two pages.
    """
    return cvss_from_metrics(metrics)[0]


def cvss_version_of(metrics):
    """Which CVSS spec produced the score _cvss_from_metrics returns."""
    return cvss_from_metrics(metrics)[1]


def severity_label(score, version='v3.1'):
    """Qualitative rating band for a CVSS base score.

    `version` matters: CVSS v2 has no Critical band. Its top rating is High
    (7.0-10.0), so applying v3.1 bands to a v2 score can print a rating that
    does not exist in that scale. v3.0, v3.1 and v4.0 share the same bands.
    Defaults to v3.1 for entries stored before the version was recorded; every
    such entry was checked to be v3.1 or v4.0, which band identically.
    """
    try:
        s = float(score)
    except (TypeError, ValueError):
        return ''
    if s >= 9.0:
        return 'High' if version == 'v2.0' else 'Critical'
    if s >= 7.0:
        return 'High'
    if s >= 4.0:
        return 'Medium'
    return 'Low' if s > 0 else ''


def _trim(text, limit=260):
    text = ' '.join((text or '').split())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(' ', 1)[0] + '...'


def fetch_nvd_keyword(keyword, start_dt, end_dt):
    """One exact-match NVD keyword query over a publication-date window.
    Returns raw vulnerability records; relevance filtering happens in collect_nvd.
    No pagination: every tracked keyword returns well under the 200-result page
    size, and a keyword that outgrows it is a signal to narrow the keyword."""
    fmt = lambda d: d.strftime('%Y-%m-%dT%H:%M:%S.000')
    query = urllib.parse.urlencode({
        'keywordSearch': keyword,
        'keywordExactMatch': '',
        'pubStartDate': fmt(start_dt),
        'pubEndDate': fmt(end_dt),
        'resultsPerPage': 200,
    })
    headers = {'User-Agent': 'FixTheVuln-AIIDE-Tracker/1.0'}
    if use_nvd_key():
        headers['apiKey'] = NVD_API_KEY
    try:
        req = urllib.request.Request(f"{NVD_API_URL}?{query}", headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8')).get('vulnerabilities', [])
    except (OSError, http.client.HTTPException, json.JSONDecodeError) as e:
        print(f"  Warning: NVD query for {keyword!r} failed: {e}")
        return []


def fetch_nvd_by_id(cve_id):
    """Single-CVE lookup for the re-verification pass in reverify_entries().
    Same host and auth as fetch_nvd_keyword. Returns the raw `cve` record, or
    None on any failure -- the caller must leave last_verified_at untouched
    on None so a transient failure gets retried next run instead of being
    mistaken for 'checked and fine'."""
    headers = {'User-Agent': 'FixTheVuln-AIIDE-Tracker/1.0'}
    if use_nvd_key():
        headers['apiKey'] = NVD_API_KEY
    try:
        query = urllib.parse.urlencode({'cveId': cve_id})
        req = urllib.request.Request(f"{NVD_API_URL}?{query}", headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            vulns = json.loads(resp.read().decode('utf-8')).get('vulnerabilities', [])
    except (OSError, http.client.HTTPException, json.JSONDecodeError) as e:
        print(f"  Warning: NVD re-verify lookup for {cve_id!r} failed: {e}")
        return None
    return vulns[0]['cve'] if vulns else None


CVE_ID_RE = re.compile(r'^CVE-\d{4}-\d+$')
# Unanchored twin of CVE_ID_RE for scanning free text rather than validating
# a whole id field -- ^...$ never matches mid-string, so findall() over a
# description needs this one instead.
CVE_ID_SCAN_RE = re.compile(r'CVE-\d{4}-\d+')
REVERIFY_BATCH = 20


def _superseding_id(own_id, description):
    """Best-effort successor lookup from a Rejected record's own description.
    NVD/MITRE rejection notes conventionally list the replacement under
    'ConsultIDs:', but the exact phrasing isn't guaranteed across CNAs, so
    this takes any OTHER CVE id mentioned in the text rather than matching
    that literal phrase. Returns '' when the record names no other CVE."""
    for match in CVE_ID_SCAN_RE.findall(description or ''):
        if match != own_id:
            return match
    return ''


def reverify_entries(state, limit=REVERIFY_BATCH):
    """Re-checks NVD's vulnStatus for the `limit` stalest-verified stored
    entries (oldest or missing last_verified_at first), so a CVE rejected or
    merged into another ID AFTER we first captured it doesn't sit on the page
    forever looking like a live disclosure. merge()'s dedup means an entry is
    otherwise never revisited once stored -- this is the only thing that
    ever looks at a stored entry again. Only entries whose id is a CVE id are
    checked; GHSA-only ids (no CVE assigned) have no NVD record to check
    against. At REVERIFY_BATCH=20/week against MAX_STORED=500, a full sweep
    takes ~25 weeks -- a CVE rejected right after capture can display at its
    original severity for months before this reaches it. Returns the count
    newly marked rejected this run."""
    candidates = [e for e in state['entries'] if CVE_ID_RE.match(e.get('id', ''))]
    candidates.sort(key=lambda e: e.get('last_verified_at') or '')
    candidates = candidates[:limit]
    delay = NVD_DELAY_WITH_KEY if use_nvd_key() else NVD_DELAY_ANON
    newly_rejected = 0
    for i, entry in enumerate(candidates):
        if i:
            time.sleep(delay)
        record = fetch_nvd_by_id(entry['id'])
        if record is None:
            continue
        entry['last_verified_at'] = datetime.now(timezone.utc).isoformat()
        if record.get('vulnStatus') == 'Rejected':
            if entry.get('status') != 'rejected':
                desc = next((d['value'] for d in record.get('descriptions', [])
                             if d.get('lang') == 'en'), '')
                entry['status'] = 'rejected'
                entry['superseded_by'] = _superseding_id(entry['id'], desc)
                newly_rejected += 1
        elif entry.get('status') == 'rejected':
            # A CNA dispute can get a rejection reinstated. Rare, but a CVE
            # that's live again must not stay permanently mislabeled because
            # this pass only ever checked for the forward transition before.
            entry['status'] = 'new'
            entry.pop('superseded_by', None)
    return newly_rejected


def collect_nvd(start_dt, end_dt):
    entries = []
    delay = NVD_DELAY_WITH_KEY if use_nvd_key() else NVD_DELAY_ANON
    for i, keyword in enumerate(NVD_KEYWORDS):
        if i:
            time.sleep(delay)
        for record in fetch_nvd_keyword(keyword, start_dt, end_dt):
            cve = record.get('cve', {})
            cve_id = cve.get('id', '')
            desc = next((d['value'] for d in cve.get('descriptions', [])
                         if d.get('lang') == 'en'), '')
            if not cve_id or not is_relevant(desc):
                continue
            score, score_version = cvss_from_metrics(cve.get('metrics', {}))
            entries.append({
                'id': cve_id,
                'source': 'nvd',
                'vendor': vendor_of(desc),
                'product': affected_product(desc),
                'published': (cve.get('published') or '')[:10],
                'severity': score,
                'score_version': score_version,
                'severity_label': severity_label(score, score_version or 'v3.1'),
                'summary': _trim(desc),
                'url': f"https://nvd.nist.gov/vuln/detail/{cve_id}",
            })
    return entries


def collect_ghsa(cutoff_dt, github_token=None):
    # github_token stays None in the workflow on purpose: these are public
    # advisories, and the only token available there is the write-scoped
    # GITHUB_TOKEN. urllib copies request headers across redirects, including
    # cross-host ones, so authenticating a call that needs no auth is a
    # needless way to forward a write-capable credential.
    entries = []
    for repo in GHSA_REPOS:
        for adv in fetch_ghsa_advisories(repo, github_token):
            pub_dt = _parse_ghsa_date(adv.get('published_at', ''))
            if pub_dt is not None and pub_dt < cutoff_dt:
                continue
            summary = adv.get('summary') or ''
            text = f"{repo} {summary} {adv.get('description') or ''}"
            if not is_relevant(text):
                continue
            score = adv.get('cvss', {}).get('score') if isinstance(adv.get('cvss'), dict) else None
            entries.append({
                'id': adv.get('cve_id') or adv.get('ghsa_id', ''),
                'source': 'ghsa',
                'vendor': vendor_of(text),
                'product': affected_product(summary) or affected_product(adv.get('description') or ''),
                'published': (adv.get('published_at') or '')[:10],
                'severity': str(score) if score is not None else '',
                # GHSA's own vocabulary says "Moderate" where CVSS v3.1 says
                # "Medium". Derive from the score so the column holds one scale.
                'severity_label': severity_label(score) or (adv.get('severity') or '').title(),
                'summary': _trim(summary),
                'url': adv.get('html_url', ''),
            })
    return entries


def collect_kev():
    """Filter the KEV catalog already fetched daily by fetch_kev.py. Low yield
    (KEV rarely lists developer tooling) but costs no network call."""
    if not KEV_DATA_FILE.exists():
        return []
    data = json.loads(KEV_DATA_FILE.read_text(encoding='utf-8'))
    entries = []
    for v in data.get('vulnerabilities', []):
        text = f"{v.get('title','')} {v.get('description','')}"
        if not is_relevant(text):
            continue
        score = v.get('cvss') or ''
        entries.append({
            'id': v.get('id', ''),
            'source': 'kev',
            'vendor': vendor_of(text),
            'product': affected_product(v.get('description', '')),
            # kev-data.json carries only the CISA catalog-add date, which is
            # not a publication date: CVE-2026-59822 was added 2026-09-02 but
            # NVD published it 2026-07-08. Blank beats an 8-week-wrong date
            # under a "Published" header. The real date is kept under its own
            # name so nothing is lost; blank sorts these rows last, which is
            # correct for an entry whose disclosure date we do not know.
            'published': '',
            'kev_added': (v.get('dateAdded') or '')[:10],
            'severity': str(score),
            'severity_label': severity_label(score),
            'summary': _trim(v.get('description', '')),
            'url': f"https://nvd.nist.gov/vuln/detail/{v.get('id','')}",
        })
    return entries


def _author_matches(authors, accepted):
    """True when a paper carries one of the accepted full author names. A
    surname substring cannot tell two people apart, and the page asserts the
    attribution by name."""
    return any(' '.join(a.split()).lower() in accepted for a in authors)


def _split_rss_authors(creator):
    """dc:creator's comma-joined author list to individual names, without
    splitting inside a parenthesized affiliation -- arXiv's optional
    '(Institute A, Institute B)' suffix contains its own commas."""
    names, current, depth = [], [], 0
    for ch in creator:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth = max(0, depth - 1)
        if ch == ',' and depth == 0:
            names.append(''.join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        names.append(''.join(current).strip())
    return [n for n in names if n]


def _rss_pubdate_to_iso(text):
    """RFC 822 'Thu, 04 Sep 2025 00:00:00 -0400' -> '2025-09-04'."""
    try:
        return parsedate_to_datetime(text).date().isoformat()
    except (TypeError, ValueError):
        return ''


def parse_arxiv_rss(body, accepted_names=ARXIV_AUTHOR_NAMES):
    """RSS 2.0 bytes to paper dicts, refusing input that should never come
    from arXiv. Split out from the fetch so the guards are testable offline."""
    if len(body) > MAX_ARXIV_BYTES:
        print(f"  Warning: arXiv response over {MAX_ARXIV_BYTES} bytes; skipped")
        return []
    # Python's ElementTree refuses external entities but does expand internal
    # ones, so a DTD is a billion-laughs vector. Verified on this interpreter:
    # the external-entity case raises, the expansion case parses. arXiv's RSS
    # feed never sends a doctype, so refusing one costs nothing and removes the
    # vector without taking a defusedxml dependency.
    if b'<!DOCTYPE' in body[:2048].upper():
        print("  Warning: arXiv response carried a doctype; skipped")
        return []
    try:
        # Safe against XXE on CPython: _elementtree installs no external-entity
        # handler, so an external entity raises rather than resolving. The
        # remaining internal-expansion risk is capped by libexpat >= 2.4's
        # amplification guard, which is a property of the runner image, not of
        # this code. If the workflow's Python or base image is ever pinned to
        # an older expat, revisit this.
        root = ET.fromstring(body)
    except ET.ParseError as e:
        print(f"  Warning: arXiv response did not parse: {e}")
        return []

    papers = []
    for item in root.findall('channel/item'):
        creator = item.findtext('dc:creator', default='', namespaces=RSS_NS)
        authors = _split_rss_authors(creator)
        if not _author_matches(authors, accepted_names):
            continue
        guid = item.findtext('guid', default='')
        paper_id = guid.rsplit(':', 1)[-1] if guid else ''
        abstract = re.sub(r'^arXiv:\S+\s+Announce Type:\s*\S+\s*',
                           '', item.findtext('description', default=''))
        abstract = re.sub(r'^Abstract:\s*', '', abstract)
        papers.append({
            'id': paper_id,
            'title': ' '.join(item.findtext('title', default='').split()),
            'authors': authors,
            'published': _rss_pubdate_to_iso(item.findtext('pubDate', default='')),
            'summary': _trim(abstract, 240),
            'url': f"https://arxiv.org/abs/{paper_id}" if paper_id else '',
        })
    return papers


def fetch_arxiv_author(category=ARXIV_CATEGORY):
    """Every paper in `category`'s daily RSS feed whose dc:creator carries an
    accepted full author name (see ARXIV_AUTHOR_NAMES above). Replaces a
    surname query against export.arxiv.org/api/query, which answers every
    request from a GitHub Actions runner with an empty-body 406 regardless of
    headers -- see the comment above ARXIV_AUTHOR_NAMES."""
    url = f"{ARXIV_RSS}/{category}"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'FixTheVuln-AIIDE-Tracker/1.0',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*',
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read(MAX_ARXIV_BYTES + 1)
    # OSError covers URLError, HTTPError and ConnectionResetError; a mid-transfer
    # reset during read() is not a URLError and would otherwise crash the job.
    except (OSError, http.client.HTTPException) as e:
        print(f"  Warning: arXiv RSS fetch for {category!r} failed: {e}")
        return []
    return parse_arxiv_rss(body)


def collect_research():
    papers = fetch_arxiv_author()
    seen, unique = set(), []
    for paper in sorted(papers, key=lambda p: p['published'], reverse=True):
        if paper['id'] and paper['id'] not in seen:
            seen.add(paper['id'])
            unique.append(paper)
    return unique[:MAX_RESEARCH]


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding='utf-8'))
    return {"last_updated": None, "entries": [], "research": []}


def save_state(state):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding='utf-8')


def load_archive():
    """Entries evicted from the MAX_STORED-capped active list, kept
    permanently. Uncapped by design: the cap exists to bound what the live
    tracker page embeds and ships to every visitor, not to bound how much
    history this repo is allowed to remember."""
    if ARCHIVE_FILE.exists():
        return json.loads(ARCHIVE_FILE.read_text(encoding='utf-8'))
    return {"entries": []}


def save_archive(archive):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_FILE.write_text(json.dumps(archive, indent=2) + "\n", encoding='utf-8')


def merge(state, found, archive=None):
    """Add entries whose id isn't already stored. Returns the count added.
    Dedup is a plain id set rather than lib.ai_vuln_intel_store.add_entry: that
    store is bound to ai-vuln-intel.json and stamps every entry with the
    loop_rounds/notes fields of its claim-verification loop, which this
    pipeline does not run.

    Entries pushed out by the MAX_STORED cap are appended to `archive` (a
    list) when one is given, rather than discarded -- see load_archive()."""
    known = {e['id'] for e in state['entries']}
    added = 0
    for entry in found:
        if not entry['id'] or entry['id'] in known:
            continue
        entry['detected_at'] = datetime.now(timezone.utc).isoformat()
        entry['status'] = 'new'
        state['entries'].append(entry)
        known.add(entry['id'])
        added += 1
    # Eviction order: least-recently-DETECTED first. `published` is not a
    # usable eviction key -- KEV entries never carry one (see fetch_kev.py),
    # so sorting eviction by `published` would evict every KEV entry before
    # any dated CVE, no matter how recently the KEV entry was actually found.
    state['entries'].sort(key=lambda e: e.get('detected_at') or '', reverse=True)
    evicted = state['entries'][MAX_STORED:]
    del state['entries'][MAX_STORED:]
    if archive is not None and evicted:
        archive.extend(evicted)
    # Storage/display order is separate from eviction order: newest published
    # first. A KEV row with no date sorts last here, which only affects
    # display position, not survival.
    state['entries'].sort(key=lambda e: (e.get('published') or '', e['id']), reverse=True)
    return added


def main():
    parser = argparse.ArgumentParser(description="Collect AI IDE / MCP vulnerability disclosures")
    parser.add_argument('--days', type=int, default=MAX_WINDOW_DAYS,
                        help=f"publication lookback window (max {MAX_WINDOW_DAYS})")
    parser.add_argument('--reverify', action='store_true',
                        help="Skip collection; instead re-check NVD's vulnStatus for "
                             f"the {REVERIFY_BATCH} stalest-verified stored entries")
    args = parser.parse_args()

    if args.reverify:
        state = load_state()
        newly_rejected = reverify_entries(state)
        if newly_rejected:
            save_state(state)
        print(f"Re-verified up to {REVERIFY_BATCH} entries; "
              f"{newly_rejected} newly marked rejected")
        return 0

    days = min(args.days, MAX_WINDOW_DAYS)
    end_dt = datetime.now(timezone.utc)
    start_dt = end_dt - timedelta(days=days)

    state = load_state()
    archive = load_archive()
    archived_before = len(archive['entries'])
    found = []
    found += collect_nvd(start_dt, end_dt)
    found += collect_ghsa(start_dt)
    found += collect_kev()

    added = merge(state, found, archive=archive['entries'])
    if len(archive['entries']) > archived_before:
        save_archive(archive)
    # Papers are replaced wholesale rather than merged: the list is small and
    # the source is authoritative. An empty result is treated as a failed fetch
    # and keeps the last known-good list, so a genuine "every paper withdrawn"
    # state will not clear the section on its own.
    research = collect_research()
    # arXiv intermittently returns a short list. Replacing wholesale would
    # publish a 1-paper section over a good 5-paper one until the next clean
    # run, so a shrunken response is treated as a failed fetch.
    research_changed = (research
                        and len(research) >= len(state.get('research') or [])
                        and research != state.get('research'))
    if research_changed:
        state['research'] = research

    if added or research_changed:
        save_state(state)
        print(f"Added {added} new disclosure(s); {len(state.get('research', []))} paper(s) "
              f"tracked in {STATE_FILE.name}")
    else:
        print(f"No new AI IDE/MCP disclosures ({len(state['entries'])} stored, "
              f"{len(state.get('research', []))} paper(s))")
    return 0


if __name__ == '__main__':
    sys.exit(main())
