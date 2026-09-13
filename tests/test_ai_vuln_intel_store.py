"""Tests for scripts/lib/ai_vuln_intel_store.py.

Covers the two behaviors every downstream aggregator task depends on:
id-based dedup (add_entry) and the 3-round loop cap (record_loop_round).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from lib.ai_vuln_intel_store import add_entry, record_loop_round, get_entries, load_state, set_status


def _fresh_state():
    return {"last_updated": None, "entries": []}


class TestAddEntry(unittest.TestCase):
    def test_adds_new_entry(self):
        state = _fresh_state()
        added = add_entry(state, {"id": "owasp-top10-2026", "type": "owasp_top10_change",
                                   "status": "new", "source_url": "https://x", "detected_at": "2026-09-12"})
        self.assertTrue(added)
        self.assertEqual(len(state["entries"]), 1)

    def test_dedups_by_id(self):
        state = _fresh_state()
        entry = {"id": "ghsa-abc", "type": "framework_ghsa", "status": "new",
                  "source_url": "https://x", "detected_at": "2026-09-12"}
        add_entry(state, entry)
        added_again = add_entry(state, dict(entry))
        self.assertFalse(added_again)
        self.assertEqual(len(state["entries"]), 1)

    def test_new_entry_defaults_loop_rounds_to_zero(self):
        state = _fresh_state()
        add_entry(state, {"id": "x", "type": "framework_ghsa", "status": "new",
                           "source_url": "https://x", "detected_at": "2026-09-12"})
        self.assertEqual(state["entries"][0]["loop_rounds"], 0)


class TestRecordLoopRound(unittest.TestCase):
    def _state_with_entry(self):
        state = _fresh_state()
        add_entry(state, {"id": "e1", "type": "missing_technique_page", "status": "drafted",
                           "source_url": "https://x", "detected_at": "2026-09-12"})
        return state

    def test_stays_in_review_under_cap(self):
        state = self._state_with_entry()
        for _ in range(3):
            status = record_loop_round(state, "e1")
        self.assertEqual(status, "in_review")
        self.assertEqual(get_entries(state)[0]["loop_rounds"], 3)

    def test_flips_to_needs_human_review_past_cap(self):
        state = self._state_with_entry()
        for _ in range(4):
            status = record_loop_round(state, "e1")
        self.assertEqual(status, "needs_human_review")


class TestGetEntries(unittest.TestCase):
    def test_filters_by_status(self):
        state = _fresh_state()
        add_entry(state, {"id": "a", "type": "framework_ghsa", "status": "new",
                           "source_url": "https://x", "detected_at": "2026-09-12"})
        add_entry(state, {"id": "b", "type": "framework_ghsa", "status": "published",
                           "source_url": "https://x", "detected_at": "2026-09-12"})
        self.assertEqual(len(get_entries(state, status="new")), 1)
        self.assertEqual(len(get_entries(state)), 2)


class TestSetStatus(unittest.TestCase):
    def _state_with_entry(self):
        state = _fresh_state()
        add_entry(state, {"id": "e1", "type": "framework_ghsa", "status": "new",
                           "source_url": "https://x", "detected_at": "2026-09-12"})
        return state

    def test_set_status_on_existing_entry(self):
        state = self._state_with_entry()
        result = set_status(state, "e1", "drafted")
        self.assertTrue(result)
        self.assertEqual(get_entries(state)[0]["status"], "drafted")

    def test_set_status_on_nonexistent_entry(self):
        state = _fresh_state()
        result = set_status(state, "nonexistent", "drafted")
        self.assertFalse(result)

    def test_set_status_with_notes(self):
        state = self._state_with_entry()
        result = set_status(state, "e1", "in_review", notes="Verified claim")
        self.assertTrue(result)
        self.assertEqual(get_entries(state)[0]["status"], "in_review")
        self.assertEqual(get_entries(state)[0]["notes"], "Verified claim")


if __name__ == '__main__':
    unittest.main()
