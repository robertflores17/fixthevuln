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

from aggregate_ai_security_news import build_digest
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


if __name__ == '__main__':
    unittest.main()
