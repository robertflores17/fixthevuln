#!/usr/bin/env python3
"""
Renders the live disclosure table into
blog/ai-ide-security-vulnerabilities-2026.html from data/ai-ide-vulns.json.

Idempotent by design: the run is a no-op unless the rendered table differs
from what is already between the markers. Only then does it bump the visible
"Last updated" line and the schema's dateModified. A daily job that rewrote
those dates unconditionally would advertise fresh content on days with no new
disclosures, which is the freshness signal search engines discount and exactly
what the project's timestamp rules exist to prevent.

The narrative above the table is never touched. The headline count stays at the
[un]prompted 2026 research figure it has always cited; the live count lives in
the table's own caption.

Usage: python3 scripts/generate_ai_ide_tracker.py [--limit 12]
"""
import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / 'scripts'))

from lib.templates import (esc, html_head, nav, share_bar, footer,
                           cf_analytics, breadcrumb_schema)
from aggregate_ai_ide_vulns import GHSA_REPOS

DATA_FILE = REPO_ROOT / "data" / "ai-ide-vulns.json"
PAGE = REPO_ROOT / "blog" / "ai-ide-security-vulnerabilities-2026.html"

START = "<!-- AI-IDE-TRACKER-START -->"
END = "<!-- AI-IDE-TRACKER-END -->"
RESEARCH_START = "<!-- AI-IDE-RESEARCH-START -->"
RESEARCH_END = "<!-- AI-IDE-RESEARCH-END -->"
DEFAULT_LIMIT = 10
RESEARCH_LIMIT = 5

SEVERITY_COLORS = {
    'Critical': '#d32f2f',
    'High': '#f57c00',
    'Medium': '#f9a825',
    'Low': '#388e3c',
}

# The sources the collector queries, named in a fixed order. Deriving this
# from the stored entries instead would drop GitHub Security Advisories from
# the caption whenever NVD happened to publish the same CVE first, which is
# most days -- claiming fewer sources than are actually consulted.
# "GitHub Security Advisories" unqualified reads as the whole GHSA database.
# It is 9 hand-listed repositories, and dedup means GHSA only contributes a row
# NVD has not published yet. Say the scope.
SOURCES_SENTENCE = (f"NVD, GitHub security advisories for {len(GHSA_REPOS)} MCP "
                    "and AI-agent repositories, and the CISA KEV catalog")


def long_date(iso):
    """YYYY-MM-DD to "September 19, 2026". The project writes dates this way in
    body copy, and a bare ISO date three lines under a "March 16, 2026" byline
    reads as machine output."""
    try:
        return datetime.strptime(iso, '%Y-%m-%d').strftime('%B %-d, %Y')
    except (ValueError, TypeError):
        # str(), not the bare value: a non-string here would reach esc() and
        # raise mid-render, which is the bug field() exists to prevent.
        return str(iso or '')


def field(entry, key):
    """Escaped string value for one entry field. The str() is not decoration:
    data/ai-ide-vulns.json is edited by the daily review pass, and a number
    where a string belongs would crash esc() mid-render."""
    return esc(str(entry.get(key) or ''))


def safe_url(url):
    """Only http(s) links are rendered. Two of the three sources build the URL
    from a fixed https prefix, but GHSA's html_url arrives from an API and the
    review pass can write this field while reading attacker-authored CVE text.
    A javascript: or data: value would otherwise become a live one-click XSS
    link in a published page."""
    url = str(url or '')
    return url if url.startswith(('https://', 'http://')) else ''


# "RMCP is an official Rust SDK for the Model Context Protocol." Once the
# product has its own column, that opening sentence is pure boilerplate: it
# fires on 65 of 88 stored entries and removes roughly 23% of the text.
# Both quantifiers are bounded, so this stays linear on adversarial input.
# [^.] in the prefix, not '.': with '.' the strip can span a sentence break and
# delete a real impact sentence sitting before the gloss. Verified: an opening
# "Unauthenticated remote code execution is possible ... Foo is a server for
# MCP. Prior to 1.2, ..." lost the RCE sentence from the cell entirely.
DEFINITION_RE = re.compile(r'^[^.]{0,80}?\s+is\s+(?:an?|the)\s+[^.]{0,120}\.\s+')
# Budget chosen by measurement, not taste. Counting cells that retain any
# impact language (allows/exposes/bypass/unauthenticated/traversal/...):
#
#   260 no strip (original)   48 of 88 without impact   avg 249 chars
#   260 + strip               48 of 88                  avg 191
#   130 + strip               66 of 88                  avg 123
#
# Stripping the boilerplate is free: same meaning, 23% shorter. Truncating to
# 130 is not: it cost 18 more cells their statement of what actually goes
# wrong, and it landed on the two Critical 9.8 Cursor rows, which ended up
# describing the sandbox that was supposed to stop the bug.
#
# A genuine ~90-char impact clause needs rewriting, not truncation, and that is
# what `review_summary` is for. Clause-selection heuristics were tried and
# rejected: they improved the aggregate but still missed those two rows.
SUMMARY_CHARS = 260


def short_summary(entry, limit=SUMMARY_CHARS):
    """The summary with its definitional opener removed, then truncated.

    This is presentation only: the stored summary stays long so the archive's
    search haystack keeps matching on text the cell no longer shows.

    Known ceiling: stripping is not rewriting. What survives is the advisory's
    own second clause, so it often starts mid-sentence and is heavy with file
    paths. A real impact clause needs `review_summary`, which summary_of()
    already prefers. Do not try to synthesise one with more regex.
    """
    # Coerce before the branch below, not after. data/ai-ide-vulns.json is
    # written by the daily review pass, and a non-string here used to be caught
    # by str() at the call sites; returning it raw would crash esc() mid-render.
    text = str(summary_of(entry) or '')
    if entry.get('review_summary'):
        # A reviewer wrote this to be read. Do not chop it up.
        return text
    text = ' '.join(text.split())
    stripped = DEFINITION_RE.sub('', text)
    # Only take the strip when something is left worth showing.
    if len(stripped) > 40:
        text = stripped
    if len(text) <= limit:
        return text
    # rsplit avoids cutting mid-word, but collapses to "A..." when the only
    # space is near the start, which CNA-controlled text can force. Fall back
    # to a hard cut rather than render an empty-looking cell.
    cut = text[:limit].rsplit(' ', 1)[0]
    if len(cut) < limit // 3:
        cut = text[:limit]
    return cut + '...'


def summary_of(entry):
    """A reviewer's rewritten summary when one exists, else the raw feed text.
    Lets the daily Claude review improve wording without the renderer needing
    to know whether a review has run yet."""
    return entry.get('review_summary') or entry.get('summary', '')


def displayable(entries):
    """Entries the reviewer has not excluded. A reviewer marks an advisory
    'excluded' when a tracked name appears but the product is not an AI IDE or
    MCP component; the keyword gate cannot make that call on its own."""
    return [e for e in entries if e.get('status') != 'excluded']


def render_row(entry):
    label = str(entry.get('severity_label') or '')
    score = str(entry.get('severity') or '')
    color = SEVERITY_COLORS.get(label, 'var(--text-muted,#666)')
    severity = f"{label} {score}".strip() or 'Unrated'
    url = safe_url(entry.get('url'))
    ident = field(entry, 'id')
    # A dropped scheme must not silently drop the identifier too.
    id_cell = f'<a href="{esc(url)}" target="_blank" rel="noopener">{ident}</a>' if url else ident
    return (
        '                        <tr>\n'
        f'                            <td style="padding:0.6rem;white-space:nowrap;">{field(entry, "published")}</td>\n'
        f'                            <td style="padding:0.6rem;white-space:nowrap;">{id_cell}</td>\n'
        f'                            <td style="padding:0.6rem;white-space:nowrap;">{field(entry, "product")}</td>\n'
        f'                            <td style="padding:0.6rem;white-space:nowrap;color:{color};font-weight:700;">{esc(severity)}</td>\n'
        f'                            <td style="padding:0.6rem;">{esc(short_summary(entry))}</td>\n'
        '                        </tr>'
    )


def render_block(entries, limit=DEFAULT_LIMIT):
    """The table plus its caption. Returns only the inner HTML; the caller
    puts the markers back around it."""
    entries = displayable(entries)
    shown = entries[:limit]
    if not shown:
        return ('<h2 id="latest-disclosures">Latest AI IDE and MCP disclosures</h2>\n'
                '<p>No disclosures have been recorded yet. This section fills in as '
                'advisories are published.</p>')

    # State the span the data actually covers rather than the collector's
    # lookback window: entries persist past 120 days, so a fixed "last 120
    # days" claim would quietly become false as the file accumulates. And say
    # "published", not "recorded": the first collection ran long after the
    # earliest entry was disclosed, so "recorded since" would claim an
    # observation history this site does not have.
    earliest = min((str(e.get('published')) for e in entries if e.get('published')),
                   default='')
    # "earliest dated", not "published since": KEV rows carry no publication
    # date, so a claim about all N entries would be computed from fewer.
    since = f" The earliest dated entry is from {esc(long_date(earliest))}." if earliest else ""
    # Most entries are MCP servers and SDKs, not the IDE vendors the article
    # counts. Leaving that unsaid makes the page look self-contradictory.
    mcp = sum(1 for e in entries if e.get('vendor') == 'MCP')
    # No "rather than the IDE vendors" complement: that count comes from
    # vendor_of(), the same heuristic pulled out of the table for being
    # unreliable, so the implied "the other N are IDE bugs" is not supportable.
    scope = f" Most are MCP servers and SDKs: {mcp} of the {len(entries)}." if mcp else ""
    rows = '\n'.join(render_row(e) for e in shown)
    return f'''<h2 id="latest-disclosures">Latest AI IDE and MCP disclosures</h2>

<p>The research above covers early 2026. This table stays current. It lists {len(entries)} AI IDE and MCP vulnerabilities, collected daily from {SOURCES_SENTENCE}.{since}{scope} {SCORE_CAVEAT} The {len(shown)} most recent are shown; <a href="/ai-ide-mcp-disclosures.html">the full tracker</a> has all {len(entries)}, filterable by severity and searchable by product.</p>

<div style="overflow-x:auto;margin-bottom:1.5rem;">
    <table style="width:100%;border-collapse:collapse;font-size:0.85rem;">
        <thead>
            <tr style="text-align:left;border-bottom:2px solid var(--border-color,#e0e0e0);">
                <th style="padding:0.6rem;">Published</th>
                <th style="padding:0.6rem;">ID</th>
                <th style="padding:0.6rem;">Affected product</th>
                <th style="padding:0.6rem;">Severity</th>
                <th style="padding:0.6rem;">Summary</th>
            </tr>
        </thead>
        <tbody>
{rows}
        </tbody>
    </table>
</div>'''


def byline(authors):
    """"A, B and 4 others" — the honest count, not a truncated list that hides
    how many people wrote the paper."""
    authors = [a for a in (authors or []) if a]
    if not authors:
        return ''
    if len(authors) <= 2:
        return ' and '.join(authors)
    rest = len(authors) - 2
    return f"{authors[0]}, {authors[1]} and {rest} other{'s' if rest > 1 else ''}"


def render_research(papers, limit=RESEARCH_LIMIT):
    """Papers are context for the disclosures, so they get their own section
    rather than rows in the CVE table: a paper has no CVE id and no CVSS score,
    which is three of that table's five columns."""
    shown = (papers or [])[:limit]
    if not shown:
        return ('<h2 id="related-research">Related research</h2>\n'
                '<p>No papers are currently tracked for this section.</p>')
    items = []
    for paper in shown:
        title = esc(str(paper.get('title') or ''))
        url = safe_url(paper.get('url'))
        heading = (f'<a href="{esc(url)}" target="_blank" rel="noopener"><strong>{title}</strong></a>'
                   if url else f'<strong>{title}</strong>')
        items.append(
            '        <li style="margin-bottom:1rem;">\n'
            f'            {heading}<br>\n'
            f'            <span style="font-size:0.8rem;color:var(--text-muted,#666);">{esc(byline(paper.get("authors")))} &middot; {esc(long_date(paper.get("published", "")))} &middot; arXiv {esc(str(paper.get("id") or ""))}</span><br>\n'
            f'            <span style="font-size:0.85rem;">{esc(str(paper.get("summary") or ""))}</span>\n'
            '        </li>')
    return f'''<h2 id="related-research">Related research</h2>

<p>The table above lists disclosures. The papers below are agent-security research co-authored by Ron F. del Rosario, co-lead of the <a href="https://genai.owasp.org/contributors/" target="_blank" rel="noopener">OWASP Agentic Security Initiative</a> and Head of AI Security for SAP Intelligent Spend and Business Network. They sit adjacent to this attack class rather than surveying it. FixTheVuln already credits his work: the vulnerability classifier and entity extractor adapt patterns from his MIT-licensed <a href="https://github.com/guerilla7/CyberMoE" target="_blank" rel="noopener">CyberMoE</a> framework, and the quiz feedback system was inspired by it. He is not involved with this site. The list is pulled from arXiv cs.CR by author name and refreshes daily. Each byline shows the first two authors in arXiv's order plus a count of the rest. The {len(shown)} most recent are shown.</p>

<ul style="list-style:none;padding-left:0;margin-bottom:1.5rem;">
{chr(10).join(items)}
</ul>'''


def _block_re(start, end):
    return re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)


def replace_block(html, block, start=START, end=END):
    pattern = _block_re(start, end)
    if not pattern.search(html):
        raise ValueError(f"{start} / {end} markers not found in {PAGE.name}")
    return pattern.sub(lambda _: f"{start}\n{block}\n{end}", html, count=1)


def current_block(html, start=START, end=END):
    """The inner HTML currently between the markers, or None if absent."""
    m = re.search(re.escape(start) + r"\n?(.*?)\n?" + re.escape(end), html, re.S)
    return m.group(1) if m else None


def stamp_dates(html, today, label="disclosure table"):
    """Update the visible "Last updated" line and the schema dateModified.
    `label` names which block moved: a research-only refresh must not claim the
    disclosure table was updated."""
    html = re.sub(
        r'(<span id="tracker-last-updated">)Last updated: [^<]*(</span>)',
        lambda m: (f"{m.group(1)}Last updated: {today.strftime('%B %-d, %Y')}"
                   f" ({label}){m.group(2)}"),
        html)
    return re.sub(r'("dateModified":\s*")[^"]*(")',
                  lambda m: f"{m.group(1)}{today.isoformat()}{m.group(2)}", html)



# ---------------------------------------------------------------- archive page

ARCHIVE_PAGE = REPO_ROOT / "ai-ide-mcp-disclosures.html"
ARCHIVE_URL = "https://fixthevuln.com/ai-ide-mcp-disclosures.html"
ARCHIVE_TITLE = "AI IDE and MCP Vulnerability Tracker - FixTheVuln"
# "checked daily", not "updated daily": archive_changed() exists so the page is
# rewritten only when the data moves. And GHSA here is 9 hand-listed repos, not
# the whole advisory database.
ARCHIVE_DESC = ("Every AI IDE and Model Context Protocol disclosure this site tracks, "
                "checked daily against NVD, GitHub advisories for 9 MCP repositories, "
                "and the CISA KEV catalog. Filter by severity, search by product.")
# Scoped to this page: every class here (d-chip, d-search, d-table, ...) exists
# only on the archive. Site-wide classes belong in style.css, but adding these
# there would mean re-minifying and bumping ?v= across 740 pages for styling
# nothing else uses.
ARCHIVE_CSS = """        .d-controls { display:flex; flex-wrap:wrap; gap:.5rem; align-items:center; margin-bottom:1rem; }
        .d-chip { border:2px solid var(--border-color,#e0e0e0); background:var(--bg-primary,#fff);
            color:var(--text-primary,#333); border-radius:999px; padding:.35rem .8rem; font-size:.85rem;
            font-weight:600; cursor:pointer; transition:all .15s; }
        .d-chip:hover { border-color:#667eea; }
        .d-chip.on { background:#667eea; border-color:#667eea; color:#fff; }
        .d-chip-n { opacity:.7; font-weight:400; }
        .d-search { flex:1; min-width:200px; padding:.45rem .8rem; font-size:.9rem;
            border:2px solid var(--border-color,#e0e0e0); border-radius:8px;
            background:var(--bg-primary,#fff); color:var(--text-primary,#333); }
        .d-search:focus { outline:none; border-color:#667eea; }
        .d-count { font-size:.85rem; color:var(--text-muted,#666); margin-bottom:.75rem; }
        .d-wrap { overflow-x:auto; }
        table.d-table { width:100%; border-collapse:collapse; font-size:.85rem; }
        .d-table th { text-align:left; padding:.6rem; border-bottom:2px solid var(--border-color,#e0e0e0);
            white-space:nowrap; }
        .d-table th[data-sort] { cursor:pointer; user-select:none; }
        .d-table th[data-sort]:hover, .d-table th[data-sort]:focus { color:#667eea; }
        .d-table td { padding:.6rem; border-bottom:1px solid var(--border-color,#eee);
            vertical-align:top; }
        .d-date, .d-id, .d-product, .d-sev { white-space:nowrap; }
        .d-sev { font-weight:700; }
        .d-empty { padding:2rem; text-align:center; color:var(--text-muted,#666); }
        @media (max-width:640px) { .d-sum { display:none; } }"""

# One sentence, both pages, so the teaser and the archive cannot drift.
# Verified against NVD 2026-09-19: roughly a fifth of stored entries carry only
# a v4.0 rating (CVE-2026-58201, CVE-2026-73218, CVE-2026-48124 have no v3.1
# metric at all), so claiming "v3.1" flat is wrong on a site that teaches CVSS.
# "until NVD completes its analysis" was wrong too: NVD marks a growing share of
# 2026 CVEs vulnStatus Deferred, meaning it has stopped enriching them and the
# promised correction never arrives.
SCORE_CAVEAT = (
    "Scores are CVSS base scores, v3.1 where NVD carries one and v4.0 where "
    "that is the only rating published, taking the rating NVD marks primary "
    "when one exists. Entries NVD has not yet analysed, or has deferred, show "
    "the reporting CNA's own assessment instead."
)

# Sort weight for the severity column. Unrated entries sort below Low rather
# than above Critical, which is what an empty string would do.
SEVERITY_ORDER = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}


def search_text(entry):
    """Lowercased haystack for the client-side search box. Built here rather
    than in JS so the page works the moment it loads and the browser never has
    to re-derive it per keystroke."""
    parts = (entry.get('id'), entry.get('product'), entry.get('vendor'),
             summary_of(entry))
    return ' '.join(str(p or '') for p in parts).lower()


def sort_key(label, score):
    """One number for the severity column: band first, base score second.
    Concatenating the score into a decimal position instead ranks CVSS 10.0
    ("4.100" -> 4.1) below 9.8 ("4.98"), putting the worst entry mid-table."""
    try:
        value = float(score)
    except (TypeError, ValueError):
        value = 0.0
    return SEVERITY_ORDER.get(label, 0) * 100 + value


def render_archive_row(entry):
    """One archive row. Carries its own filter and sort keys as data
    attributes so filtering is a display toggle and sorting reads a number,
    with no per-keystroke DOM parsing."""
    label = str(entry.get('severity_label') or '')
    score = str(entry.get('severity') or '')
    color = SEVERITY_COLORS.get(label, 'var(--text-muted,#666)')
    severity = f"{label} {score}".strip() or 'Unrated'
    url = safe_url(entry.get('url'))
    ident = field(entry, 'id')
    id_cell = f'<a href="{esc(url)}" target="_blank" rel="noopener">{ident}</a>' if url else ident
    published = str(entry.get('published') or '')
    return (
        f'<tr data-severity="{esc(label or "Unrated")}" '
        f'data-search="{esc(search_text(entry))}" '
        f'data-date="{esc(published)}" '
        f'data-score="{sort_key(label, score):.1f}">'
        f'<td class="d-date">{esc(long_date(published)) if published else "&mdash;"}</td>'
        f'<td class="d-id">{id_cell}</td>'
        f'<td class="d-product">{field(entry, "product")}</td>'
        f'<td class="d-sev" style="color:{color};">{esc(severity)}</td>'
        f'<td class="d-sum">{esc(short_summary(entry))}</td>'
        '</tr>'
    )


def render_archive_page(entries, today):
    """The standalone archive. Every stored entry, filterable and sortable in
    the browser with no backend: the whole dataset is already in the DOM, so a
    filter is a hidden toggle and a sort reads a data attribute.

    Page chrome comes from lib.templates, not pasted markup. A hand-copied
    nav, footer, favicon, beacon token or CSS version would keep working right
    up until the next site-wide change reached 740 pages and missed this one.
    """
    # ponytail: whole dataset ships in the HTML. 92 KB at 88 rows, so roughly
    # 500 KB uncompressed at MAX_STORED = 500, most of it data-search
    # duplicating each summary. Gzip handles the repetition well. Revisit with
    # server-side paging or a JSON fetch only if the archive nears the cap.
    entries = displayable(entries)
    counts = {k: sum(1 for e in entries if e.get('severity_label') == k)
              for k in SEVERITY_ORDER}
    rows = '\n'.join(render_archive_row(e) for e in entries)
    earliest = min((str(e.get('published')) for e in entries if e.get('published')),
                   default='')
    # "earliest dated", not "published since": KEV rows carry no publication
    # date, so a claim about all N entries would be computed from fewer.
    since = f" The earliest dated entry is from {esc(long_date(earliest))}." if earliest else ""
    chips = '\n'.join(
        f'        <button class="d-chip" data-filter="{k}" type="button">{k} '
        f'<span class="d-chip-n">{counts[k]}</span></button>'
        for k in ('Critical', 'High', 'Medium', 'Low') if counts[k])
    head = html_head(
        "AI IDE and MCP Vulnerability Tracker",
        ARCHIVE_DESC,
        ARCHIVE_URL,
        keywords=("MCP vulnerabilities, Model Context Protocol security, AI IDE "
                  "vulnerabilities, AI coding assistant CVE, MCP server CVE"),
        schema_blocks=[breadcrumb_schema([
            ("Home", "https://fixthevuln.com/"),
            ("AI IDE and MCP vulnerability tracker", ARCHIVE_URL),
        ])],
    )
    head = head.replace('</head>', f'    <style>\n{ARCHIVE_CSS}\n    </style>\n</head>')
    return f"""<!DOCTYPE html>
<html lang="en">
{head}
<body>
{nav()}
{share_bar()}
<div class="container">
    <a href="blog/ai-ide-security-vulnerabilities-2026.html" class="back-link">&larr; Back to the AI IDE security analysis</a>
    <h1>AI IDE and MCP vulnerability tracker</h1>
    <p>This page lists every AI IDE and Model Context Protocol disclosure the site tracks, {len(entries)} in total, collected daily from {SOURCES_SENTENCE}.{since} {SCORE_CAVEAT}</p>
    <p id="d-updated" style="font-size:.9rem;color:var(--text-muted,#666);">Last updated: {today.strftime('%B %-d, %Y')}</p>

    <div class="d-controls">
{chips}
        <button class="d-chip" data-filter="all" type="button">Clear</button>
        <input class="d-search" id="d-search" type="search" placeholder="Search product, CVE, or text" aria-label="Search disclosures" autocomplete="off">
    </div>
    <p class="d-count" id="d-count" aria-live="polite"></p>

    <div class="d-wrap">
        <table class="d-table" id="d-table">
            <thead>
                <tr>
                    <th data-sort="date" tabindex="0" role="button" aria-sort="none" title="Sort by date">Published</th>
                    <th>ID</th>
                    <th>Affected product</th>
                    <th data-sort="score" tabindex="0" role="button" aria-sort="none" title="Sort by severity">Severity</th>
                    <th>Summary</th>
                </tr>
            </thead>
            <tbody id="d-body">
{rows}
            </tbody>
        </table>
        <p class="d-empty" id="d-empty" hidden>No disclosures match that filter.</p>
    </div>
</div>
{footer()}

<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode" title="Toggle dark/light mode">
    <span id="theme-icon">&#9790;</span>
</button>

<script>
function toggleTheme() {{
    const html = document.documentElement;
    const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('fixthevuln-theme', next);
    document.getElementById('theme-icon').textContent = next === 'dark' ? '☀️' : '🌙';
}}
(function () {{
    const saved = localStorage.getItem('fixthevuln-theme');
    const theme = saved || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    if (theme === 'dark') {{
        document.documentElement.setAttribute('data-theme', 'dark');
        document.getElementById('theme-icon').textContent = '☀️';
    }}
}})();
</script>

<script>
(function () {{
    var body = document.getElementById('d-body');
    var rows = Array.prototype.slice.call(body.querySelectorAll('tr'));
    var search = document.getElementById('d-search');
    var countEl = document.getElementById('d-count');
    var emptyEl = document.getElementById('d-empty');
    var heads = document.querySelectorAll('th[data-sort]');
    var active = 'all';
    var sortKey = null, sortAsc = false;

    function apply() {{
        var q = search.value.trim().toLowerCase();
        var shown = 0;
        rows.forEach(function (row) {{
            var visible = (active === 'all' || row.dataset.severity === active)
                && (!q || row.dataset.search.indexOf(q) !== -1);
            // Only touch the attribute when it actually changes: at MAX_STORED
            // this is 500 rows per keystroke otherwise.
            if (row.hidden === visible) row.hidden = !visible;
            if (visible) shown++;
        }});
        // textContent, never innerHTML: the query is user input and must not
        // be parsed as markup on its way back to the page.
        countEl.textContent = shown === rows.length
            ? 'Showing all ' + rows.length + ' disclosures'
            : 'Showing ' + shown + ' of ' + rows.length + ' disclosures';
        emptyEl.hidden = shown !== 0;
    }}

    document.querySelectorAll('.d-chip').forEach(function (chip) {{
        chip.addEventListener('click', function () {{
            var f = chip.dataset.filter;
            active = (f === 'all' || f === active) ? 'all' : f;
            document.querySelectorAll('.d-chip').forEach(function (c) {{
                c.classList.toggle('on', c.dataset.filter === active && active !== 'all');
            }});
            apply();
        }});
    }});

    search.addEventListener('input', apply);

    function sortBy(th) {{
        var key = th.dataset.sort;
        sortAsc = sortKey === key ? !sortAsc : false;
        sortKey = key;
        rows.sort(function (a, b) {{
            var x = a.dataset[key], y = b.dataset[key];
            if (key === 'score') {{ x = parseFloat(x) || 0; y = parseFloat(y) || 0; }}
            if (x < y) return sortAsc ? -1 : 1;
            if (x > y) return sortAsc ? 1 : -1;
            return 0;
        }});
        // One insertion instead of 500 against the live tree.
        var frag = document.createDocumentFragment();
        rows.forEach(function (r) {{ frag.appendChild(r); }});
        body.appendChild(frag);
        heads.forEach(function (h) {{
            h.setAttribute('aria-sort',
                h === th ? (sortAsc ? 'ascending' : 'descending') : 'none');
        }});
    }}

    heads.forEach(function (th) {{
        th.addEventListener('click', function () {{ sortBy(th); }});
        th.addEventListener('keydown', function (e) {{
            if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); sortBy(th); }}
        }});
    }});

    apply();
}})();
</script>
{cf_analytics()}
<script src="/js/error-reporter.js?v=1"></script>
</body>
</html>
"""


def archive_changed(new_html, path=None):
    """True when the archive differs by more than its own timestamp. Without
    this the page would be rewritten every day and the daily job would commit
    a date change on days with no new disclosures, which is the freshness
    signal the tracker exists to avoid."""
    path = path or ARCHIVE_PAGE
    if not path.exists():
        return True
    # Anchored to the element that carries the line. An unanchored
    # 'Last updated: [^<]*' also eats any summary containing that literal,
    # which could mask a real content delta and freeze the published archive.
    strip = lambda h: re.sub(r'(?<=<p id="d-updated")([^>]*>)Last updated: [^<]*',
                             r'\1', h)
    return strip(path.read_text(encoding='utf-8')) != strip(new_html)

def main():
    parser = argparse.ArgumentParser(description="Render the AI IDE vulnerability tracker")
    parser.add_argument('--limit', type=int, default=DEFAULT_LIMIT,
                        help=f"rows to display (default {DEFAULT_LIMIT})")
    args = parser.parse_args()

    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE.name} not found. Run aggregate_ai_ide_vulns.py first.")
        return 1

    data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
    entries = data.get('entries', [])
    papers = data.get('research', [])
    html = PAGE.read_text(encoding='utf-8')
    block = render_block(entries, args.limit)
    research = render_research(papers)

    archive = render_archive_page(entries, date.today())
    if archive_changed(archive):
        ARCHIVE_PAGE.write_text(archive, encoding='utf-8')
        print(f"Archive page rewritten: {len(displayable(entries))} disclosures")
    else:
        print("Archive page unchanged — not touched")

    table_same = current_block(html) == block
    research_same = current_block(html, RESEARCH_START, RESEARCH_END) == research
    if table_same and research_same:
        print(f"Tracker unchanged ({len(entries)} entries, {len(papers)} papers) — "
              "page not touched")
        return 0

    changed = ([] if table_same else ['disclosure table']) + \
              ([] if research_same else ['research list'])
    updated = replace_block(html, block)
    updated = replace_block(updated, research, RESEARCH_START, RESEARCH_END)
    PAGE.write_text(stamp_dates(updated, date.today(), ' and '.join(changed)),
                    encoding='utf-8')
    print(f"Tracker updated: {min(len(entries), args.limit)} of {len(entries)} entries, "
          f"{min(len(papers), RESEARCH_LIMIT)} of {len(papers)} papers shown")
    return 0


if __name__ == '__main__':
    sys.exit(main())
