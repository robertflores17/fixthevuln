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

    def test_unrated_severity_when_score_missing(self):
        self.assertIn('Unrated', render_row(_entry(severity='', severity_label='')))

    def test_states_earliest_published_date_in_long_form(self):
        """"Published since", not "recorded since": the first collection ran
        long after the earliest entry was disclosed, so "recorded" would claim
        an observation history the site does not have."""
        block = render_block([_entry(published='2026-09-18'), _entry(published='2026-05-01')])
        self.assertIn('published since May 1, 2026', block)
        self.assertNotIn('recorded since', block)

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
        self.assertIn('CVSS v3.1 base scores where available', block)

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


if __name__ == '__main__':
    unittest.main()
