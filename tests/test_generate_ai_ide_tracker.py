"""Covers the renderer's two risks: escaping and idempotency.

Escaping matters because every field in the table comes from NVD, GHSA or KEV.
An advisory summary is attacker-influenceable text (anyone can file a CVE
description) written straight into a published page.

Idempotency matters because the job runs daily. If a run with no new data still
rewrote the page, the "Last updated" line and dateModified would advertise
fresh content every day on a page that had not changed.
"""
import re
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from generate_ai_ide_tracker import (
    START, END, render_block, render_row, replace_block, current_block, stamp_dates,
    summary_of, displayable, safe_url, field,
    RESEARCH_START, RESEARCH_END, render_research, byline,
    sort_key, render_archive_row, render_archive_page, archive_changed,
    SCORE_CAVEAT, short_summary, SUMMARY_CHARS,
)


def _entry(**kw):
    base = {'id': 'CVE-2026-1', 'source': 'nvd', 'vendor': 'Cursor',
            'published': '2026-09-18', 'severity': '8.8', 'severity_label': 'High',
            'summary': 'A flaw in the agent.', 'url': 'https://nvd.nist.gov/vuln/detail/CVE-2026-1'}
    base.update(kw)
    return base


def _paper(**kw):
    base = {'id': '2509.08646v1', 'title': 'Architecting Resilient LLM Agents',
            'authors': ['Ron F. Del Rosario', 'Klaudia Krawiecka'],
            'published': '2025-09-10', 'summary': 'As LLM agents become capable...',
            'url': 'https://arxiv.org/abs/2509.08646v1'}
    base.update(kw)
    return base


PAGE = f"""<html><head>
<script type="application/ld+json">
{{"datePublished": "2026-03-16", "dateModified": "2026-03-16"}}
</script></head><body>
<p>Published: March 16, 2026 &middot; <span id="tracker-last-updated">Last updated: March 16, 2026</span></p>
{START}
{END}
{RESEARCH_START}
{RESEARCH_END}
<h2>Next section</h2>
</body></html>"""


class TestEscaping(unittest.TestCase):
    def test_escapes_script_tag_in_summary(self):
        row = render_row(_entry(summary='<script>alert(1)</script>'))
        self.assertNotIn('<script>', row)
        self.assertIn('&lt;script&gt;', row)

    def test_escapes_quote_breakout_in_url(self):
        """A crafted URL must not be able to close the href and add handlers."""
        row = render_row(_entry(url='https://x/" onmouseover="alert(1)'))
        self.assertNotIn('onmouseover="alert(1)"', row)
        self.assertIn('&quot;', row)

    def test_escapes_vendor_and_id(self):
        row = render_row(_entry(vendor='<img src=x onerror=alert(1)>', id='<b>CVE</b>'))
        self.assertNotIn('<img', row)
        self.assertNotIn('<b>', row)

    def test_escapes_hostile_text_through_the_whole_block(self):
        block = render_block([_entry(summary='"><script>alert(1)</script>')])
        self.assertNotIn('<script>', block)


class TestUrlScheme(unittest.TestCase):
    """Two of three sources build the URL from a fixed https prefix, but GHSA
    supplies its own and the review pass can write this field while reading
    attacker-authored CVE text."""

    def test_rejects_javascript_scheme(self):
        row = render_row(_entry(url='javascript:alert(document.domain)'))
        self.assertNotIn('javascript:', row)

    def test_rejects_data_and_vbscript_schemes(self):
        for bad in ('data:text/html;base64,PHNjcmlwdD4=', 'vbscript:msgbox(1)',
                    'JaVaScRiPt:alert(1)', ' javascript:alert(1)'):
            with self.subTest(url=bad):
                self.assertEqual(safe_url(bad), '')

    def test_keeps_http_and_https(self):
        self.assertEqual(safe_url('https://nvd.nist.gov/vuln/detail/CVE-1'),
                         'https://nvd.nist.gov/vuln/detail/CVE-1')
        self.assertEqual(safe_url('http://example.test/a'), 'http://example.test/a')

    def test_dropped_url_still_shows_the_cve_id(self):
        """Rejecting the link must not also lose the identifier."""
        row = render_row(_entry(url='javascript:alert(1)', id='CVE-2026-9'))
        self.assertIn('CVE-2026-9', row)
        self.assertNotIn('<a href', row)

    def test_handles_missing_url(self):
        self.assertEqual(safe_url(None), '')
        self.assertEqual(safe_url(''), '')


class TestFieldCoercion(unittest.TestCase):
    """data/ai-ide-vulns.json is edited by the review pass; a number where a
    string belongs must not crash the renderer mid-page."""

    def test_non_string_field_does_not_raise(self):
        row = render_row(_entry(published=20260101, severity=8.8, id=42))
        self.assertIn('20260101', row)

    def test_none_field_renders_empty(self):
        self.assertEqual(field({'vendor': None}, 'vendor'), '')
        self.assertEqual(field({}, 'vendor'), '')

    def test_non_string_is_still_escaped(self):
        class Evil:
            def __str__(self): return '<script>alert(1)</script>'
        self.assertNotIn('<script>', field({'vendor': Evil()}, 'vendor'))


class TestRenderBlock(unittest.TestCase):
    def test_respects_limit(self):
        entries = [_entry(id=f'CVE-2026-{i}') for i in range(20)]
        block = render_block(entries, limit=5)
        self.assertEqual(block.count('<tr>'), 5)

    def test_reports_total_not_just_shown(self):
        block = render_block([_entry(id=f'CVE-2026-{i}') for i in range(20)], limit=5)
        self.assertIn('lists 20 ', block)
        self.assertIn('5 most recent', block)

    def test_empty_data_renders_placeholder_not_a_crash(self):
        block = render_block([])
        self.assertIn('No disclosures', block)
        self.assertNotIn('<table', block)

    def test_rejected_entries_are_excluded_from_the_latest_teaser(self):
        """A CVE NVD has withdrawn has no business in a "latest disclosures"
        list -- the full tracker (not this teaser) is where it stays visible."""
        block = render_block([_entry(id='CVE-2026-1'),
                              _entry(id='CVE-2026-2', status='rejected')])
        self.assertIn('lists 1 ', block)
        self.assertNotIn('CVE-2026-2', block)

    def test_unrated_severity_when_score_missing(self):
        self.assertIn('Unrated', render_row(_entry(severity='', severity_label='')))

    def test_states_earliest_dated_entry_in_long_form(self):
        """"Earliest dated", not "published since": KEV rows carry no
        publication date and are skipped by the min(), so a claim about all N
        entries would be computed from fewer than N. Also not "recorded
        since", which would claim an observation history the site lacks."""
        block = render_block([_entry(published='2026-09-18'), _entry(published='2026-05-01')])
        self.assertIn('The earliest dated entry is from May 1, 2026', block)
        self.assertNotIn('recorded since', block)

    def test_undated_entry_does_not_skew_the_span_claim(self):
        block = render_block([_entry(published=''), _entry(published='2026-05-01')])
        self.assertIn('The earliest dated entry is from May 1, 2026', block)

    def test_states_mcp_share_of_the_total(self):
        """The article counts IDE vendors; most rows are MCP servers. Leaving
        that unsaid makes the page look self-contradictory."""
        block = render_block([_entry(vendor='MCP'), _entry(vendor='MCP'), _entry(vendor='Cursor')])
        self.assertIn('Most are MCP servers and SDKs: 2 of the 3.', block)
        # No complement: the vendor field is the heuristic that was pulled from
        # the table for being unreliable, so "the other N are IDE bugs" is not
        # a claim this data supports.
        self.assertNotIn('rather than the IDE vendors', block)

    def test_names_the_ghsa_scope_not_the_whole_database(self):
        block = render_block([_entry()])
        self.assertRegex(block, r'GitHub security advisories for \d+ MCP and AI-agent repositories')

    def test_caption_states_the_cvss_precedence(self):
        block = render_block([_entry()])
        self.assertIn('taking the rating NVD marks primary when one exists', block)

    def test_caption_does_not_claim_every_score_is_v31(self):
        """Verified against NVD 2026-09-19: CVE-2026-58201, CVE-2026-73218 and
        CVE-2026-48124 carry only a v4.0 metric, roughly a fifth of stored
        entries. v3.1 and v4.0 are different scales, so presenting both as one
        unlabelled "v3.1" number is wrong on a site that teaches CVSS."""
        block = render_block([_entry()])
        self.assertNotIn('CVSS v3.1 base scores where available', block)
        self.assertIn('v4.0 where that is the only rating published', block)

    def test_caption_does_not_promise_nvd_will_finish(self):
        """NVD marks a growing share of 2026 CVEs vulnStatus Deferred, meaning
        it has stopped enriching them. "until NVD completes its analysis"
        promises a correction that never arrives."""
        block = render_block([_entry()])
        self.assertNotIn('until NVD completes its analysis', block)
        self.assertIn('has deferred', block)

    def test_both_pages_share_one_score_caveat(self):
        """The teaser and the archive must not drift apart on this claim."""
        entries = [_entry()]
        self.assertIn(SCORE_CAVEAT, render_block(entries))
        self.assertIn(SCORE_CAVEAT, render_archive_page(entries, date(2026, 9, 19)))

    def test_caption_discloses_cna_scored_entries(self):
        """Verified against NVD: 11 of the 12 rows first published here had no
        Primary rating at all, only the reporting CNA's Secondary. Saying only
        "primary over secondary" implies an NVD adjudication that does not
        exist for entries this fresh."""
        block = render_block([_entry()])
        self.assertIn("the reporting CNA's own assessment", block)


class TestReviewerHooks(unittest.TestCase):
    """The daily Claude review edits the JSON; the renderer must honour it
    without needing to know whether a review has run."""

    def test_prefers_reviewed_summary(self):
        self.assertEqual(
            summary_of(_entry(summary='raw feed text', review_summary='edited text')),
            'edited text')

    def test_falls_back_to_raw_summary(self):
        self.assertEqual(summary_of(_entry(summary='raw feed text')), 'raw feed text')
        self.assertEqual(summary_of(_entry(summary='raw', review_summary='')), 'raw')

    def test_excluded_entries_are_not_rendered(self):
        block = render_block([_entry(id='CVE-KEEP'),
                              _entry(id='CVE-DROP', status='excluded')])
        self.assertIn('CVE-KEEP', block)
        self.assertNotIn('CVE-DROP', block)

    def test_excluded_entries_are_not_counted(self):
        block = render_block([_entry(id='CVE-KEEP'),
                              _entry(id='CVE-DROP', status='excluded')])
        self.assertIn('lists 1 ', block)

    def test_all_excluded_renders_placeholder(self):
        block = render_block([_entry(status='excluded')])
        self.assertIn('No disclosures', block)

    def test_reviewed_summary_is_still_escaped(self):
        """A reviewer's text is model output, not trusted markup."""
        block = render_block([_entry(review_summary='<script>alert(1)</script>')])
        self.assertNotIn('<script>', block)


class TestByline(unittest.TestCase):
    def test_lists_one_and_two_authors_in_full(self):
        self.assertEqual(byline(['A']), 'A')
        self.assertEqual(byline(['A', 'B']), 'A and B')

    def test_gives_the_honest_count_beyond_two(self):
        self.assertEqual(byline(['A', 'B', 'C']), 'A, B and 1 other')
        self.assertEqual(byline(['A', 'B', 'C', 'D', 'E', 'F']), 'A, B and 4 others')

    def test_handles_empty(self):
        self.assertEqual(byline([]), '')
        self.assertEqual(byline(None), '')


class TestRenderResearch(unittest.TestCase):
    def test_renders_title_and_link(self):
        block = render_research([_paper()])
        self.assertIn('Architecting Resilient LLM Agents', block)
        self.assertIn('https://arxiv.org/abs/2509.08646v1', block)

    def test_escapes_hostile_paper_fields(self):
        """arXiv metadata is third-party text like any other feed."""
        block = render_research([_paper(title='<script>alert(1)</script>',
                                        summary='<img src=x onerror=alert(1)>',
                                        authors=['<b>evil</b>'])])
        self.assertNotIn('<script>', block)
        self.assertNotIn('<img', block)
        self.assertNotIn('<b>evil', block)

    def test_rejects_non_http_paper_url(self):
        block = render_research([_paper(url='javascript:alert(1)')])
        self.assertNotIn('javascript:', block)

    def test_respects_limit(self):
        block = render_research([_paper(id=str(i)) for i in range(10)], limit=3)
        self.assertEqual(block.count('<li'), 3)

    def test_empty_renders_placeholder_not_a_crash(self):
        for empty in ([], None):
            with self.subTest(value=empty):
                self.assertIn('No papers', render_research(empty))

    def test_states_the_attribution_relationship(self):
        """The section names a real person next to a store CTA. It must say
        what the list is, link the work it credits, and disclaim involvement."""
        block = render_research([_paper()])
        self.assertIn('He is not involved with this site.', block)
        # He is 5th of 6 authors on one listed paper and 4th of 5 on another,
        # so "research by" would overstate his role.
        self.assertIn('co-authored by Ron F. del Rosario', block)
        self.assertIn('https://github.com/guerilla7/CyberMoE', block)
        self.assertIn('https://genai.owasp.org/contributors/', block)

    def test_does_not_claim_to_survey_the_field(self):
        """The list is filtered by author, not topic, so calling it "the
        research literature behind this class of attack" is falsifiable in one
        click."""
        block = render_research([_paper()])
        self.assertNotIn('the research literature behind', block)
        self.assertIn('adjacent to this attack class', block)

    def test_drops_the_anchor_on_a_rejected_url(self):
        """Matches the table path: no href="" pointing at the current page.
        Counted rather than asserted absent, because the intro paragraph
        carries its own attribution links."""
        good = render_research([_paper()])
        bad = render_research([_paper(url='javascript:alert(1)')])
        self.assertEqual(good.count('<a href'), bad.count('<a href') + 1)
        self.assertNotIn('javascript:', bad)
        self.assertNotIn('href=""', bad)
        self.assertIn('Architecting Resilient LLM Agents', bad)

    def test_non_string_published_does_not_raise(self):
        self.assertIn('<li', render_research([_paper(published=2026)]))

    def test_marker_text_in_a_title_cannot_break_out(self):
        block = render_research([_paper(title='<!-- AI-IDE-RESEARCH-END --> evil')])
        out = replace_block(PAGE, block, RESEARCH_START, RESEARCH_END)
        self.assertEqual(current_block(out, RESEARCH_START, RESEARCH_END), block)

    def test_formats_the_date_as_body_copy(self):
        self.assertIn('September 10, 2025', render_research([_paper()]))


class TestMarkers(unittest.TestCase):
    def test_replaces_between_markers_only(self):
        out = replace_block(PAGE, '<p>NEW</p>')
        self.assertIn('<p>NEW</p>', out)
        self.assertIn('<h2>Next section</h2>', out)
        self.assertIn('Published: March 16, 2026', out)

    def test_missing_markers_raise(self):
        with self.assertRaises(ValueError):
            replace_block('<html>no markers</html>', '<p>x</p>')

    def test_current_block_round_trips(self):
        """The idempotency check depends on reading back exactly what was
        written; if these two disagree the page rewrites itself every run."""
        block = render_block([_entry()])
        self.assertEqual(current_block(replace_block(PAGE, block)), block)

    def test_research_block_replaces_independently(self):
        """Two marker pairs on one page must not overwrite each other."""
        out = replace_block(PAGE, '<p>TABLE</p>')
        out = replace_block(out, '<p>PAPERS</p>', RESEARCH_START, RESEARCH_END)
        self.assertIn('<p>TABLE</p>', out)
        self.assertIn('<p>PAPERS</p>', out)
        self.assertEqual(current_block(out), '<p>TABLE</p>')
        self.assertEqual(current_block(out, RESEARCH_START, RESEARCH_END), '<p>PAPERS</p>')

    def test_missing_research_markers_raise(self):
        with self.assertRaises(ValueError):
            replace_block('<html>nope</html>', '<p>x</p>', RESEARCH_START, RESEARCH_END)

    def test_repeated_replace_is_stable(self):
        block = render_block([_entry()])
        once = replace_block(PAGE, block)
        self.assertEqual(once, replace_block(once, block))


class TestLongDate(unittest.TestCase):
    def test_formats_iso_as_body_copy_date(self):
        from generate_ai_ide_tracker import long_date
        self.assertEqual(long_date('2026-05-25'), 'May 25, 2026')

    def test_passes_through_unparseable(self):
        from generate_ai_ide_tracker import long_date
        self.assertEqual(long_date('not-a-date'), 'not-a-date')
        self.assertEqual(long_date(''), '')
        self.assertEqual(long_date(None), '')


class TestStampDates(unittest.TestCase):
    def test_updates_modified_and_visible_line(self):
        out = stamp_dates(PAGE, date(2026, 9, 19))
        self.assertIn('"dateModified": "2026-09-19"', out)
        self.assertIn('Last updated: September 19, 2026 (disclosure table)', out)

    def test_leaves_date_published_alone(self):
        out = stamp_dates(PAGE, date(2026, 9, 19))
        self.assertIn('"datePublished": "2026-03-16"', out)
        self.assertIn('Published: March 16, 2026', out)

    def test_visible_date_uses_audit_visible_format(self):
        """audit_pages.py's staleness regex requires a day number, so
        'September 2026' would be flagged as stale."""
        out = stamp_dates(PAGE, date(2026, 9, 5))
        self.assertRegex(out, r'Last updated: September 5, 2026')

    def test_scopes_the_claim_to_what_changed(self):
        """Only the table changed, not the March article body. The label keeps
        the audit's "Last updated" signal while saying what actually moved."""
        self.assertIn('(disclosure table)', stamp_dates(PAGE, date(2026, 9, 19)))

    def test_label_reflects_a_research_only_refresh(self):
        """On a day when only a paper lands, the page must not claim the
        disclosure table moved."""
        out = stamp_dates(PAGE, date(2026, 9, 19), 'research list')
        self.assertIn('(research list)', out)
        self.assertNotIn('(disclosure table)', out)

    def test_is_rerunnable(self):
        once = stamp_dates(PAGE, date(2026, 9, 19))
        self.assertEqual(once, stamp_dates(once, date(2026, 9, 19)))




class TestSortKey(unittest.TestCase):
    """The archive's severity column sorts on a precomputed number. The first
    version concatenated the score into a decimal position, which ranked CVSS
    10.0 ("4.100" -> 4.1) below 9.8 ("4.98") and buried the worst entry
    mid-table."""

    def test_ten_outranks_nine_point_eight(self):
        self.assertGreater(sort_key('Critical', '10.0'), sort_key('Critical', '9.8'))

    def test_band_beats_score(self):
        # A High 8.8 must never outrank a Critical 9.0, and a Critical with a
        # missing score must still outrank any High.
        self.assertGreater(sort_key('Critical', '9.0'), sort_key('High', '8.8'))
        self.assertGreater(sort_key('Critical', ''), sort_key('High', '8.8'))

    def test_unrated_sorts_last(self):
        self.assertLess(sort_key('', ''), sort_key('Low', '0.1'))

    def test_unparseable_score_does_not_raise(self):
        self.assertEqual(sort_key('High', 'not-a-number'), 300.0)


class TestArchiveRow(unittest.TestCase):
    """The archive row adds three attribute contexts the blog table does not
    have (data-search, data-date, data-score), each carrying feed text."""

    HOSTILE = {
        'id': 'CVE-2026-0001" onmouseover="alert(1)',
        'product': '<script>alert(1)</script>',
        'vendor': "'; alert(1); //",
        'published': '2026-09-19"><img src=x onerror=alert(1)>',
        'severity': '9.8', 'severity_label': 'Critical',
        'summary': 'Breakout: " data-x="y </td></tr><tr><td>injected',
        'url': 'javascript:alert(document.cookie)',
    }

    def _parse(self, html):
        from html.parser import HTMLParser

        class P(HTMLParser):
            def __init__(self):
                super().__init__()
                self.tags = []

            def handle_starttag(self, tag, attrs):
                self.tags.append((tag, dict(attrs)))

        p = P()
        p.feed(html)
        return p.tags

    def test_hostile_entry_yields_exactly_one_row(self):
        # A substring check is not enough here: "onmouseover=" legitimately
        # appears as text inside an escaped attribute value. What matters is
        # whether the parser sees it as an attribute.
        tags = self._parse(render_archive_row(self.HOSTILE))
        self.assertEqual(sum(1 for t, _ in tags if t == 'tr'), 1)
        self.assertEqual(sum(1 for t, _ in tags if t == 'td'), 5)

    def test_no_event_handlers_or_script_survive(self):
        tags = self._parse(render_archive_row(self.HOSTILE))
        self.assertFalse(any(t == 'script' for t, _ in tags))
        self.assertFalse(any(k.startswith('on') for _, a in tags for k in a))

    def test_rejected_scheme_drops_the_anchor_but_keeps_the_id(self):
        row = render_archive_row(self.HOSTILE)
        self.assertNotIn('<a href', row)
        self.assertIn('CVE-2026-0001', row)

    def test_search_haystack_is_lowercased(self):
        row = render_archive_row({'id': 'CVE-2026-1', 'product': 'RMCP',
                                  'severity_label': 'High', 'severity': '7.5',
                                  'published': '2026-09-01', 'summary': 'UPPER Text'})
        attrs = dict(self._parse(row)[0][1])
        self.assertIn('rmcp', attrs['data-search'])
        self.assertIn('upper text', attrs['data-search'])

    def test_rejected_entry_shows_its_successor_not_its_old_severity(self):
        """Hedged ("Possibly") and linked to the successor's own NVD record,
        not stated as settled fact -- content-editor review 2026-09-26: the
        successor is this pipeline's best-effort read of free text, not
        something NVD itself asserts."""
        row = render_archive_row(_entry(status='rejected', superseded_by='CVE-2026-9999',
                                        severity_label='Critical', severity='9.8'))
        self.assertIn('Possibly superseded by', row)
        self.assertIn('href="https://nvd.nist.gov/vuln/detail/CVE-2026-9999"', row)
        self.assertIn('>CVE-2026-9999</a>', row)
        self.assertNotIn('Critical', row)

    def test_rejected_entry_without_a_known_successor_says_so(self):
        row = render_archive_row(_entry(status='rejected', severity_label='Critical'))
        self.assertIn('Marked Rejected in NVD', row)

    def test_rejected_entry_does_not_match_any_severity_chip(self):
        row = render_archive_row(_entry(status='rejected', severity_label='Critical'))
        attrs = dict(self._parse(row)[0][1])
        self.assertEqual(attrs['data-severity'], 'Rejected')

    def test_rejected_entry_sorts_to_the_bottom_on_severity(self):
        row = render_archive_row(_entry(status='rejected', severity_label='Critical', severity='9.8'))
        attrs = dict(self._parse(row)[0][1])
        self.assertEqual(attrs['data-score'], '0.0')


class TestArchivePageSupersededCounts(unittest.TestCase):
    """A rejected CVE stays a row on the page (nothing tracked here just
    disappears) but must not read as a live disclosure in the headline count
    or the severity chips -- those numbers claim "confirmed", not "listed"."""

    def test_rejected_entry_is_excluded_from_the_headline_count(self):
        page = render_archive_page([_entry(id='CVE-2026-1'),
                                    _entry(id='CVE-2026-2', status='rejected')],
                                   date(2026, 9, 19))
        self.assertIn('the site tracks, 1 in total', page)

    def test_rejected_entry_is_still_a_row_on_the_page(self):
        page = render_archive_page([_entry(id='CVE-2026-1'),
                                    _entry(id='CVE-2026-2', status='rejected')],
                                   date(2026, 9, 19))
        self.assertIn('CVE-2026-2', page)

    def test_rejected_entry_is_excluded_from_severity_chip_counts(self):
        page = render_archive_page([_entry(id='CVE-2026-1', severity_label='Critical'),
                                    _entry(id='CVE-2026-2', severity_label='Critical',
                                           status='rejected')],
                                   date(2026, 9, 19))
        self.assertIn('Critical <span class="d-chip-n">1</span>', page)

    def test_footnote_appears_only_when_something_is_excluded(self):
        """"Rejected" stays framed as NVD's own claim; the successor guess
        stays framed as this site's read of the rejection notice, per
        content-editor review 2026-09-26 -- not attributed to NVD."""
        with_rejected = render_archive_page(
            [_entry(id='CVE-2026-1'), _entry(id='CVE-2026-2', status='rejected')],
            date(2026, 9, 19))
        without = render_archive_page([_entry(id='CVE-2026-1')], date(2026, 9, 19))
        self.assertIn('NVD has since rejected them', with_rejected)
        self.assertNotIn('NVD has since rejected them', without)


class TestArchiveIdempotence(unittest.TestCase):
    """The archive carries its own "Last updated" line. Rewriting it daily
    would commit a date change on days with no new disclosures, which is the
    freshness signal this whole design exists to avoid."""

    ENTRY = {'id': 'CVE-2026-1', 'product': 'RMCP', 'severity_label': 'High',
             'severity': '7.5', 'published': '2026-09-01', 'summary': 'x',
             'url': 'https://nvd.nist.gov/vuln/detail/CVE-2026-1'}

    def test_timestamp_only_difference_is_not_a_change(self):
        import tempfile
        old = render_archive_page([self.ENTRY], date(2026, 9, 1))
        new = render_archive_page([self.ENTRY], date(2026, 9, 19))
        self.assertNotEqual(old, new)  # the dates really do differ
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'archive.html'
            f.write_text(old, encoding='utf-8')
            self.assertFalse(archive_changed(new, f))

    def test_new_entry_is_a_change(self):
        import tempfile
        old = render_archive_page([self.ENTRY], date(2026, 9, 19))
        extra = dict(self.ENTRY, id='CVE-2026-2')
        new = render_archive_page([self.ENTRY, extra], date(2026, 9, 19))
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'archive.html'
            f.write_text(old, encoding='utf-8')
            self.assertTrue(archive_changed(new, f))

    def test_missing_file_counts_as_changed(self):
        self.assertTrue(archive_changed('<html></html>', Path('/nonexistent/x.html')))


class TestTeaserLinksToArchive(unittest.TestCase):
    def test_caption_links_the_full_tracker_with_the_real_total(self):
        entries = [dict(TestArchiveIdempotence.ENTRY, id=f'CVE-2026-{i}')
                   for i in range(25)]
        block = render_block(entries, limit=10)
        self.assertIn('/ai-ide-mcp-disclosures.html', block)
        self.assertIn('all 25', block)
        self.assertEqual(block.count('<tr>'), 10)


class TestArchiveDriftGuards(unittest.TestCase):
    """Each of these converts a silent drift into a failing test. All three
    were safe when written; none of them had anything asserting they stayed
    that way."""

    ENTRY = TestArchiveIdempotence.ENTRY

    def test_sort_key_always_returns_a_float(self):
        # data-score is interpolated with :.1f. A tie-breaker that made this
        # return a string would become stored XSS with no other code change,
        # and the ordering tests would not notice.
        for args in (('Critical', '10.0'), ('High', 'not-a-number'),
                     ('', ''), (None, None)):
            self.assertIsInstance(sort_key(*args), float)

    def test_css_version_matches_the_shared_constant(self):
        # Hardcoding the version means the next site-wide bump updates 740
        # pages and serves stale CSS to this one.
        from lib.constants import STYLE_CSS_VERSION
        page = render_archive_page([self.ENTRY], date(2026, 9, 19))
        self.assertIn(f'style.min.css?v={STYLE_CSS_VERSION}', page)

    def test_beacon_token_matches_the_shared_constant(self):
        from lib.constants import CF_ANALYTICS_TOKEN
        page = render_archive_page([self.ENTRY], date(2026, 9, 19))
        self.assertIn(CF_ANALYTICS_TOKEN, page)

    def test_summary_containing_the_timestamp_sentinel_still_counts_as_changed(self):
        """The strip in archive_changed() used to be unanchored, so a summary
        containing the literal "Last updated: " swallowed the rest of its cell
        and could mask a real delta, freezing the published archive."""
        import tempfile
        a = dict(self.ENTRY, summary='Last updated: ABC DEF')
        b = dict(self.ENTRY, summary='Last updated: abc def')
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'archive.html'
            f.write_text(render_archive_page([a], date(2026, 9, 19)), encoding='utf-8')
            self.assertTrue(
                archive_changed(render_archive_page([b], date(2026, 9, 19)), f))


class TestShortSummary(unittest.TestCase):
    """Presentation only. The stored summary stays long so the archive's search
    box keeps matching text the cell no longer displays."""

    REAL = ("RMCP is an official Rust SDK for the Model Context Protocol. Prior "
            "to 2.0.0, the rmcp crate's OAuth implementation in "
            "crates/rmcp/src/transport/auth.rs omits the RFC 9728 resource field.")

    def test_drops_the_definitional_opener(self):
        got = short_summary({'summary': self.REAL})
        self.assertNotIn('is an official Rust SDK', got)
        self.assertTrue(got.startswith('Prior to 2.0.0'))

    def test_keeps_the_version_clause(self):
        """The affected-version range is the one thing a reader acts on, and it
        survives truncation because it comes first."""
        self.assertIn('2.0.0', short_summary({'summary': self.REAL}))

    def test_reviewed_summary_is_never_chopped(self):
        """A reviewer wrote it to be read. summary_of() prefers it, and the
        shortener must not then truncate or strip it."""
        long_review = 'Unauthenticated SSE transport exposes every MCP tool. ' * 5
        entry = {'summary': self.REAL, 'review_summary': long_review}
        self.assertEqual(short_summary(entry), long_review)

    def test_respects_the_budget(self):
        self.assertLessEqual(len(short_summary({'summary': 'word ' * 200})),
                             SUMMARY_CHARS + 3)

    def test_short_text_is_returned_unchanged(self):
        self.assertEqual(short_summary({'summary': 'A brief note.'}), 'A brief note.')

    def test_strip_is_skipped_when_it_would_leave_nothing(self):
        # "X is a Y." with no second clause must not become an empty cell.
        text = 'Cline is an autonomous coding agent for the terminal.'
        self.assertEqual(short_summary({'summary': text}), text)

    def test_missing_summary_does_not_raise(self):
        for entry in ({}, {'summary': None}, {'summary': ''}):
            self.assertEqual(short_summary(entry), '')

    def test_stays_linear_on_adversarial_text(self):
        import time
        entry = {'summary': 'x ' + 'a-' * 3000 + ' is a thing. ' + 'b ' * 800}
        start = time.perf_counter()
        short_summary(entry)
        self.assertLess(time.perf_counter() - start, 0.1)

    def test_search_haystack_is_not_shortened(self):
        """The whole point of shortening at render time: the archive row's
        data-search attribute must still carry text the cell no longer shows."""
        # Long enough that truncation actually bites; REAL alone fits the budget.
        long_text = self.REAL + (' An unauthenticated client can then replay the '
                                 'token against any downstream resource server '
                                 'that trusts the issuer, including SENTINELWORD.')
        entry = {'id': 'CVE-2026-1', 'product': 'RMCP', 'severity_label': 'High',
                 'severity': '7.5', 'published': '2026-09-01', 'summary': long_text}
        row = render_archive_row(entry)
        self.assertIn('sentinelword', row.lower())            # in data-search
        self.assertNotIn('SENTINELWORD', short_summary(entry))  # cut from the cell


class TestShortSummaryEdges(unittest.TestCase):
    """Three defects a review caught after the first cut. Each was reachable
    from CNA-authored advisory text or from the LLM review pass's own output."""

    def test_non_string_review_summary_does_not_crash_the_render(self):
        """data/ai-ide-vulns.json is written by the daily review pass. The old
        call sites wrapped this in str(); the early return dropped that, so a
        reviewer emitting a bare number aborted the whole daily render."""
        for value in (123, 4.5, True):
            self.assertEqual(short_summary({'summary': 'x', 'review_summary': value}),
                             str(value))

    def test_strip_does_not_cross_a_sentence_boundary(self):
        """With '.' in the prefix class the strip spanned a sentence break and
        deleted a real impact sentence sitting before the definitional gloss."""
        text = ("Unauthenticated remote code execution is possible in the default "
                "config. Foo is a server for MCP. Prior to 1.2, the handler "
                "passes user input to a shell without quoting.")
        self.assertIn('remote code execution', short_summary({'summary': text}))

    def test_leading_short_word_does_not_collapse_the_cell(self):
        """rsplit on a string whose only space is near the start returned
        "A...", an effectively empty cell that feed text can force."""
        got = short_summary({'summary': 'A ' + 'x' * 300})
        self.assertGreater(len(got), 40)


if __name__ == '__main__':
    unittest.main()
