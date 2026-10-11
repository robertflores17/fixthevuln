#!/usr/bin/env python3
"""Regression tests for the Patch Tuesday window in scripts/generate_sprint_kit.py.

Run: python3 -m unittest tests.test_sprint_kit_cycle  (needs reportlab installed)

Guards the October 2026 fix: the kit ships the day after Patch Tuesday, so its
data window must be KEVs added after the previous Patch Tuesday through this
one (inclusive, so Patch Tuesday zero-days land in it). The old window ran
forward from this Patch Tuesday, so every kit was built from data that
didn't exist yet.
"""

import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from generate_sprint_kit import get_patch_cycle_range, latest_patch_month


class TestPatchCycleRange(unittest.TestCase):
    def test_window_ends_on_this_patch_tuesday(self):
        # Sep 2026 PT = Sep 8, Oct 2026 PT = Oct 13
        self.assertEqual(get_patch_cycle_range(2026, 10),
                         (datetime(2026, 9, 9), datetime(2026, 10, 13)))

    def test_january_wraps_to_previous_december(self):
        # Dec 2026 PT = Dec 8, Jan 2027 PT = Jan 12
        self.assertEqual(get_patch_cycle_range(2027, 1),
                         (datetime(2026, 12, 9), datetime(2027, 1, 12)))

    def test_consecutive_windows_have_no_gap_or_overlap(self):
        _, sep_end = get_patch_cycle_range(2026, 9)
        oct_start, _ = get_patch_cycle_range(2026, 10)
        self.assertEqual((oct_start - sep_end).days, 1)


class TestLatestPatchMonth(unittest.TestCase):
    def test_before_patch_tuesday_uses_previous_month(self):
        self.assertEqual(latest_patch_month(datetime(2026, 10, 11)), (2026, 9))

    def test_on_and_after_patch_tuesday_uses_this_month(self):
        self.assertEqual(latest_patch_month(datetime(2026, 10, 13)), (2026, 10))
        self.assertEqual(latest_patch_month(datetime(2026, 10, 14)), (2026, 10))

    def test_early_january_uses_previous_december(self):
        self.assertEqual(latest_patch_month(datetime(2027, 1, 5)), (2026, 12))


if __name__ == '__main__':
    unittest.main()
