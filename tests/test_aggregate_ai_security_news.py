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

import re
import time

from aggregate_ai_security_news import CATEGORY_ORDER, SOURCES, _clean_html, build_digest, parse_feed
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


if __name__ == '__main__':
    unittest.main()
