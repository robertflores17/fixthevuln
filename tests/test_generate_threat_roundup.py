#!/usr/bin/env python3
"""Regression tests for scripts/generate_threat_roundup.py.

Run: python3 -m unittest tests.test_generate_threat_roundup
  or python3 tests/test_generate_threat_roundup.py

Guards the cvss_score() helper against the June 2026 crash where a newly-added
KEV entry stored cvss=None (key present, value None). float(v.get('cvss', 0))
returned None and float(None) raised TypeError, aborting the weekly
blog-publish job. cvss_score() must coerce any non-numeric input to 0.0.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from generate_threat_roundup import cvss_score


class TestCvssScore(unittest.TestCase):
    def test_none_value_does_not_crash(self):
        # The exact case that broke the June 16 publish job.
        self.assertEqual(cvss_score({'cvss': None}), 0.0)

    def test_missing_key(self):
        self.assertEqual(cvss_score({}), 0.0)

    def test_empty_string(self):
        self.assertEqual(cvss_score({'cvss': ''}), 0.0)

    def test_non_numeric_string(self):
        self.assertEqual(cvss_score({'cvss': 'N/A'}), 0.0)

    def test_numeric_string(self):
        self.assertEqual(cvss_score({'cvss': '9.8'}), 9.8)

    def test_numeric_float(self):
        self.assertEqual(cvss_score({'cvss': 7.5}), 7.5)

    def test_zero_and_unscored_both_floor_to_zero(self):
        # A real 0.0 and an unscored null both sort/bucket as 0.0 (intended:
        # unscored CVEs deprioritize to the bottom of the roundup).
        self.assertEqual(cvss_score({'cvss': 0}), 0.0)
        self.assertEqual(cvss_score({'cvss': None}), cvss_score({'cvss': 0}))


if __name__ == '__main__':
    unittest.main()
