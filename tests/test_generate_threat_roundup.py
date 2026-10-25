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
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from datetime import datetime

from generate_threat_roundup import covered_ids, cvss_score, recent_vulns


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


class TestRecentWindow(unittest.TestCase):
    """KEV entries reach kev-data.json 1-3 days after CISA's dateAdded, so a 7-day window lost CVEs
    (8 between Aug and Oct 2026). Look back 14 days and de-duplicate against earlier roundups."""

    TODAY = datetime(2026, 10, 27)  # a Tuesday

    def _v(self, date, id=None, **kw):
        return {'id': id or f'CVE-{date}', 'dateAdded': date, **kw}

    def test_late_published_monday_item_is_still_picked_up(self):
        late = self._v('2026-10-19', id='CVE-2026-1')  # CISA Monday, published after last Tuesday's run
        self.assertEqual(recent_vulns([late], self.TODAY), [late])

    def test_window_boundary_is_14_days_inclusive(self):
        vulns = [self._v('2026-10-13'), self._v('2026-10-12')]
        self.assertEqual([v['dateAdded'] for v in recent_vulns(vulns, self.TODAY)], ['2026-10-13'])

    def test_already_covered_cves_are_not_repeated(self):
        vulns = [self._v('2026-10-20', id='CVE-2026-1'), self._v('2026-10-20', id='CVE-2026-2')]
        got = recent_vulns(vulns, self.TODAY, covered={'CVE-2026-1'})
        self.assertEqual([v['id'] for v in got], ['CVE-2026-2'])

    def test_covered_ids_reads_published_and_unpublished_drafts(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, 'weekly-threat-roundup-2026-10-13.md.published').write_text(
                '### CVE-2026-1: x\nSee also CVE-2025-22 mentioned in prose.')
            Path(d, 'weekly-threat-roundup-2026-10-20.md').write_text('### CVE-2026-3: y')
            Path(d, 'ai-security-roundup-2026-10-25.md').write_text('### CVE-2026-999: z')
            # Only item headings of weekly roundups count; prose mentions must not suppress a CVE.
            self.assertEqual(covered_ids(d), {'CVE-2026-1', 'CVE-2026-3'})

    def test_missing_or_null_date_does_not_crash(self):
        vulns = [self._v(None), {'id': 'CVE-x'}, self._v('2026-10-25')]
        self.assertEqual([v['dateAdded'] for v in recent_vulns(vulns, self.TODAY)], ['2026-10-25'])

    def test_malformed_date_is_skipped_not_fatal(self):
        vulns = [self._v('Oct 25'), self._v('2026-13-45'), self._v(20261025), self._v('2026-10-25')]
        got = recent_vulns(vulns, self.TODAY)
        self.assertEqual([v['dateAdded'] for v in got if v['dateAdded'] == '2026-10-25'], ['2026-10-25'])

    def test_archived_entries_excluded(self):
        vulns = [self._v('2026-10-25', archived=True), self._v('2026-10-25')]
        self.assertEqual(len(recent_vulns(vulns, self.TODAY)), 1)

if __name__ == '__main__':
    unittest.main()
