"""Pins the Secondary-over-Primary defect in fetch_kev's CVSS selection.

fetch_cvss_from_nvd sets the score on every published CVE page. NVD does not
order its metric list, so taking the first entry meant a reporting CNA's
Secondary rating could outrank NVD's own Primary. Real case, verified live:
CVE-2026-13323 lists Eclipse's Secondary 4.1 MEDIUM before NVD's Primary
8.7 HIGH. The same defect was found and fixed in aggregate_ai_ide_vulns.py.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from fetch_kev import _best_score


class TestBestScore(unittest.TestCase):
    def test_primary_wins_when_listed_after_secondary(self):
        self.assertEqual(_best_score([
            {'type': 'Secondary', 'cvssData': {'baseScore': 4.1}},
            {'type': 'Primary', 'cvssData': {'baseScore': 8.7}}]), '8.7')

    def test_primary_wins_when_listed_first(self):
        self.assertEqual(_best_score([
            {'type': 'Primary', 'cvssData': {'baseScore': 8.2}},
            {'type': 'Secondary', 'cvssData': {'baseScore': 5.0}}]), '8.2')

    def test_secondary_used_when_no_primary_exists(self):
        """Most CVEs carry only a CNA score; those must still publish."""
        self.assertEqual(_best_score([
            {'type': 'Secondary', 'cvssData': {'baseScore': 8.8}}]), '8.8')

    def test_untyped_metric_still_yields_a_score(self):
        self.assertEqual(_best_score([{'cvssData': {'baseScore': 7.5}}]), '7.5')

    def test_empty_and_scoreless_lists_return_blank(self):
        self.assertEqual(_best_score([]), '')
        self.assertEqual(_best_score([{'type': 'Primary', 'cvssData': {}}]), '')

    def test_skips_a_primary_with_no_score(self):
        self.assertEqual(_best_score([
            {'type': 'Primary', 'cvssData': {}},
            {'type': 'Secondary', 'cvssData': {'baseScore': 6.1}}]), '6.1')

    def test_zero_score_is_preserved_not_treated_as_missing(self):
        self.assertEqual(_best_score([{'type': 'Primary', 'cvssData': {'baseScore': 0.0}}]), '0.0')


if __name__ == '__main__':
    unittest.main()
