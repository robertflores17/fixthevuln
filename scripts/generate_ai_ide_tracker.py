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

from lib.templates import esc
from aggregate_ai_ide_vulns import GHSA_REPOS

DATA_FILE = REPO_ROOT / "data" / "ai-ide-vulns.json"
PAGE = REPO_ROOT / "blog" / "ai-ide-security-vulnerabilities-2026.html"

START = "<!-- AI-IDE-TRACKER-START -->"
END = "<!-- AI-IDE-TRACKER-END -->"
RESEARCH_START = "<!-- AI-IDE-RESEARCH-START -->"
RESEARCH_END = "<!-- AI-IDE-RESEARCH-END -->"
DEFAULT_LIMIT = 12
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
        f'                            <td style="padding:0.6rem;">{esc(str(summary_of(entry) or ""))}</td>\n'
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
    since = f" published since {esc(long_date(earliest))}" if earliest else ""
    # Most entries are MCP servers and SDKs, not the IDE vendors the article
    # counts. Leaving that unsaid makes the page look self-contradictory.
    mcp = sum(1 for e in entries if e.get('vendor') == 'MCP')
    # No "rather than the IDE vendors" complement: that count comes from
    # vendor_of(), the same heuristic pulled out of the table for being
    # unreliable, so the implied "the other N are IDE bugs" is not supportable.
    scope = f" Most are MCP servers and SDKs: {mcp} of the {len(entries)}." if mcp else ""
    rows = '\n'.join(render_row(e) for e in shown)
    return f'''<h2 id="latest-disclosures">Latest AI IDE and MCP disclosures</h2>

<p>The research above covers early 2026. This table stays current. It lists {len(entries)} AI IDE and MCP vulnerabilities{since}, collected daily from {SOURCES_SENTENCE}.{scope} Scores are CVSS v3.1 base scores where available, taking the rating NVD marks primary when one exists. Most entries here are days old, and NVD has not scored them yet, so the number shown is the reporting CNA's own assessment until NVD completes its analysis. The {len(shown)} most recent are shown.</p>

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
