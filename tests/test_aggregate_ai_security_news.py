#!/usr/bin/env python3
"""Regression test for scripts/aggregate_ai_security_news.py.

Run: python3 -m unittest tests.test_aggregate_ai_security_news
  or python3 tests/test_aggregate_ai_security_news.py

Guards the 2026-09-29 fix for a 4-day date mismatch: build_digest() used to
write a `date:` frontmatter field stamped with the Friday aggregation date.
publish_editorial.py's _parse_frontmatter() only defaults `date` to "today"
when the field is absent, so that Friday date rode straight through into
datePublished / the visible "Last updated" line -- even though the digest
isn't published to the live site until the following Tuesday's
publish-blog.yml run, up to 4 days later. build_digest() must leave `date`
unset so the actual publish run stamps the real go-live date.
"""

import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

import io
import re
import time
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock
from html.parser import HTMLParser

import aggregate_ai_security_news as agg
from aggregate_ai_security_news import CATEGORY_ORDER, SOURCES, _clean_html, _item_matches_filter, build_digest, carry_framework_advisories, parse_feed, report_source_health
from publish_editorial import MarkdownConverter
from publish_editorial import BlogPublisher


class TestDigestDateFrontmatter(unittest.TestCase):
    def test_no_date_field_in_frontmatter(self):
        aggregation_day = datetime(2026, 9, 18)  # a Friday
        digest = build_digest({}, aggregation_day, aggregation_day)
        fm_text = digest.split('---')[1]
        self.assertNotIn('date:', fm_text)

    def test_publisher_stamps_actual_publish_date_not_aggregation_date(self):
        aggregation_day = datetime(2026, 9, 18)  # written Friday
        digest = build_digest({}, aggregation_day, aggregation_day)
        publisher = BlogPublisher.__new__(BlogPublisher)  # skip __init__'s disk I/O
        fm, _ = publisher._parse_frontmatter(digest)
        # _parse_frontmatter defaults `date` to datetime.now() -- i.e. whenever
        # publish_editorial.py actually runs (the next Tuesday), not the
        # Friday the digest was written.
        self.assertEqual(fm['date'], datetime.now().strftime('%Y-%m-%d'))
        self.assertNotEqual(fm['date'], aggregation_day.strftime('%Y-%m-%d'))


class TestCleanHtmlEmDash(unittest.TestCase):
    def test_mdash_entity_and_literal_become_commas(self):
        self.assertEqual(_clean_html('price &mdash; Hacker News.'), 'price, Hacker News.')
        self.assertEqual(_clean_html('price — Hacker News.'), 'price, Hacker News.')
        self.assertEqual(_clean_html('News.I\'m here'), 'News. I\'m here')


class TestFeedTextEscaping(unittest.TestCase):
    def _digest_with(self, title, link, summary):
        item = {'title': title, 'link': link, 'summary': _clean_html(summary),
                'published': '', 'published_dt': None}
        grouped = {CATEGORY_ORDER[0][0]: [{'source': SOURCES[0], 'item': item}]}
        return build_digest(grouped, datetime(2026, 10, 2), datetime(2026, 10, 2))

    def test_encoded_markup_in_summary_stays_text(self):
        digest = self._digest_with('T', 'https://example.com/a', '&lt;img src=x onerror=alert(1)&gt;')
        self.assertNotIn('<img', digest)
        self.assertIn('&lt;img', digest)

    def test_markup_in_title_is_escaped(self):
        digest = self._digest_with('T <i>x</i>', 'https://example.com/a', 'ok')
        self.assertNotIn('<i>', digest)
        self.assertIn('&lt;i&gt;', digest)

    def test_non_http_links_are_dropped(self):
        rss = (b'<rss><channel><item><title>T</title><link>javascript:alert(1)</link>'
               b'<description>x</description></item></channel></rss>')
        self.assertEqual(parse_feed(rss, SOURCES[0]), [])

    def test_markdown_link_payloads_stay_text(self):
        digest = self._digest_with('P](javascript:void(1)', 'https://example.com/a',
                                   '[x](https://a.example/" data-probe="1)')
        body = digest.split('\n---\n', 1)[1]  # publisher converts the body only
        out = MarkdownConverter().convert(body)
        hrefs = re.findall(r'href="([^"]*)"', out)
        self.assertTrue(hrefs)
        self.assertTrue(all(h.startswith('https://') for h in hrefs), hrefs)
        self.assertNotIn('data-probe="1"', out)

    def test_long_angle_bracket_run_is_fast(self):
        start = time.monotonic()
        _clean_html('<' * 100000)
        self.assertLess(time.monotonic() - start, 2.0)

    def test_long_whitespace_run_is_fast(self):
        start = time.monotonic()
        _clean_html(' ' * 50000 + 'x')
        self.assertLess(time.monotonic() - start, 2.0)

    def test_hostile_item_renders_no_executable_markup(self):
        """Friday publishes with no human step: escaping is the only control, so pin it end to end."""
        hostile = ('"><script>alert(1)</script><img src=x onerror=alert(1)> '
                   '&lt;script&gt;alert(2)&lt;/script&gt; [x](javascript:alert(3)) &#x3c;svg onload=alert(4)&#x3e;')
        digest = self._digest_with(hostile, 'https://example.com/a?q="><x', hostile)
        out = MarkdownConverter().convert(digest.split('\n---\n', 1)[1])
        tags = []

        class Collect(HTMLParser):
            def handle_starttag(self, tag, attrs):
                tags.append((tag, [k for k, _ in attrs]))

        Collect().feed(out)
        for tag, attr_names in tags:
            self.assertNotIn(tag, ('script', 'img', 'svg', 'iframe'), out)
            self.assertFalse([a for a in attr_names if a.startswith('on')], (tag, attr_names))
        hrefs = re.findall(r'href="([^"]*)"', out)
        self.assertTrue(all(h.startswith('http') for h in hrefs), hrefs)


class TestUnparseablePublishedDate(unittest.TestCase):
    def test_raw_date_text_cannot_inject_markdown_formatting(self):
        item = {'title': 'T', 'link': 'https://example.com/a', 'summary': '',
                'published': '*x*_y_`z`<b>', 'published_dt': None}
        grouped = {CATEGORY_ORDER[0][0]: [{'source': SOURCES[0], 'item': item}]}
        digest = build_digest(grouped, datetime(2026, 10, 2), datetime(2026, 10, 2))
        out = MarkdownConverter().convert(digest.split('\n---\n', 1)[1])
        credit = re.search(r'<p>Source:.*?</p>', out, re.S).group(0)
        self.assertNotRegex(credit, r'<(em|code|b)>')


class TestFeedTextCleanup(unittest.TestCase):
    def test_arxiv_announce_prefix_is_stripped(self):
        self.assertEqual(_clean_html('arXiv:2610.30184v1 Announce Type: new Abstract: Static analysis misses bugs.'),
                         'Static analysis misses bugs.')

    def test_numeric_hex_apostrophe_decodes_once(self):
        self.assertEqual(_clean_html('Today&#x27;s release'), "Today's release")
        digest = TestFeedTextEscaping()._digest_with('T', 'https://example.com/a', 'Today&#x27;s release')
        self.assertNotIn('&amp;#x27;', digest)

    def test_numeric_em_dash_becomes_comma(self):
        self.assertEqual(_clean_html('a &#8212; b'), 'a, b')

    def test_em_dash_in_item_title_becomes_comma(self):
        digest = TestFeedTextEscaping()._digest_with('Alpha \u2014 Beta', 'https://example.com/a', 'x')
        self.assertNotIn('\u2014', digest)
        self.assertIn('Alpha, Beta', digest)

    def test_single_source_is_singular(self):
        digest = TestFeedTextEscaping()._digest_with('T', 'https://example.com/a', 'x')
        self.assertIn('1 new item from 1 source.', digest)
        self.assertNotIn('1 sources', digest)


class TestWillisonRelevanceFilter(unittest.TestCase):
    KW = next(s for s in SOURCES if s['name'] == 'Simon Willison')['filter_keywords']

    def test_off_topic_posts_are_dropped(self):
        for title in ('Battle Drones - a vibe coded RTS', 'My obituary for programming', 'llm-echo 0.5',
                      'Inline rendering with document.currentScript', 'web-edit 0.1a2'):
            self.assertFalse(_item_matches_filter({'title': title, 'summary': ''}, self.KW), title)
        # 'Hacker News' links in a summary must not rescue an off-topic post.
        for title in ('DE STAAT - FREEDOM (Official Music Video)',):
            self.assertFalse(_item_matches_filter({'title': title, 'summary': 'via Hacker News'}, self.KW), title)

    def test_ai_security_posts_are_kept(self):
        """Real Willison security titles that an earlier, tighter list dropped (inflected forms)."""
        for title in ('Self-generated prompt injections in compaction summaries',
                      'Microsoft Copilot Cowork Exfiltrates Files',
                      'Clinejection - Compromising Cline\'s Production Releases',
                      'OpenAI agents attacked RubyGems',
                      'How I tricked Claude into leaking your deepest, darkest secrets',
                      'AI Worming through Word',
                      'OpenAI Help: Lockdown Mode', "OpenAI's accidental cyberattack against Hugging Face",
                      'Stealing Reasoning Traces from Proprietary LLM APIs',
                      'MCP Colors: Systematically deal with prompt injection risk',
                      'eMudhra Intermediate CA Compromise', "Today's PHP Security Release"):
            self.assertTrue(_item_matches_filter({'title': title, 'summary': ''}, self.KW), title)


class FakeResp:
    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self, n=-1):
        return self.body if n < 0 else self.body[:n]


class TestFeedSizeCap(unittest.TestCase):
    """2026-10: read(MAX_FEED_BYTES) cut Project Zero (11 MB) and CISA (5.7 MB) off mid-XML, so they
    parsed to 0 items with no alert. Over-cap must be a loud fetch error, never a silent truncation."""

    def test_feed_over_cap_is_rejected_not_truncated(self):
        big = b'<rss><channel>' + b'x' * (agg.MAX_FEED_BYTES + 10)
        with mock.patch.object(agg.urllib.request, 'urlopen', return_value=FakeResp(big)), redirect_stderr(io.StringIO()) as err:
            self.assertIsNone(agg.fetch_feed('https://example.com/f.xml'))
        self.assertIn('over', err.getvalue())

    def test_feed_at_cap_boundary_is_kept(self):
        ok = b'<rss/>' + b' ' * (agg.MAX_FEED_BYTES - 6)
        with mock.patch.object(agg.urllib.request, 'urlopen', return_value=FakeResp(ok)):
            self.assertEqual(len(agg.fetch_feed('https://example.com/f.xml')), agg.MAX_FEED_BYTES)

    def test_parse_error_is_reported_to_the_caller(self):
        errors = []
        self.assertEqual(parse_feed(b'<rss><channel><item>', SOURCES[0], errors), [])
        self.assertEqual(len(errors), 1)

    def test_no_known_oversize_or_dead_feed_urls(self):
        feeds = [s['feed'] for s in SOURCES]
        self.assertNotIn('https://www.cisa.gov/cybersecurity-advisories/all.xml', feeds)  # 5.7 MB
        self.assertNotIn('https://googleprojectzero.blogspot.com/feeds/posts/default', feeds)  # 11 MB
        self.assertFalse([f for f in feeds if 'protectai.com' in f])  # 404


class TestSourceHealthReport(unittest.TestCase):
    def test_reports_live_broken_and_empty_sources(self):
        stats = [{'source': 'A', 'status': 'ok', 'parsed': 5, 'count': 1},
                 {'source': 'B', 'status': 'parse-failed', 'parsed': 0, 'count': 0},
                 {'source': 'C', 'status': 'fetch-failed', 'parsed': 0, 'count': 0},
                 {'source': 'D', 'status': 'ok', 'parsed': 0, 'count': 0}]
        out = io.StringIO()
        with redirect_stdout(out):
            live = report_source_health(stats)
        text = out.getvalue()
        self.assertEqual(live, 1)
        self.assertIn('sources_with_items=1/4', text)
        self.assertIn('B (parse-failed)', text)
        self.assertIn('C (fetch-failed)', text)
        self.assertIn('empty', text)


if __name__ == '__main__':
    unittest.main()


class CarryFrameworkAdvisoriesTest(unittest.TestCase):
    """Regenerating a week's draft must not drop the reviewer's advisories."""

    NEW = "# Roundup\n\n## Research\n\n- item\n\n## Source List\n\n- src\n"
    EXISTING = ("# Roundup\n\n## Research\n\n- old\n\n## Framework Advisories\n\n"
                "- **GHSA-aaaa-bbbb-cccc** one\n\n### Earlier\n\n- **GHSA-dddd-eeee-ffff** two\n\n"
                "## Source List\n\n- src\n")

    def test_section_carried_into_regenerated_digest(self):
        out = carry_framework_advisories(self.EXISTING, self.NEW)
        self.assertIn("GHSA-aaaa-bbbb-cccc", out)
        self.assertIn("GHSA-dddd-eeee-ffff", out)
        self.assertLess(out.index("## Framework Advisories"), out.index("## Source List"))
        self.assertEqual(out.count("## Source List"), 1)

    def test_no_section_leaves_digest_unchanged(self):
        self.assertEqual(carry_framework_advisories(self.NEW, self.NEW), self.NEW)

    def test_not_duplicated_when_digest_already_has_it(self):
        out = carry_framework_advisories(self.EXISTING, self.EXISTING)
        self.assertEqual(out.count("## Framework Advisories"), 1)
