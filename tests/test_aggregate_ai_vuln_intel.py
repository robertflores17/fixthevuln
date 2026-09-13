"""Covers the OWASP version-change detector's riskiest case: it must fire on
a genuine new-version announcement but NOT false-positive on a post that
merely mentions the Top 10 in passing (e.g. a "how we use the OWASP Top 10"
commentary post) or re-fire on a title it's already queued."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from aggregate_ai_vuln_intel import check_owasp_top10_change
from lib.ai_vuln_intel_store import add_entry


def _state():
    return {"last_updated": None, "entries": []}


class TestCheckOwaspTop10Change(unittest.TestCase):
    def test_fires_on_version_announcement(self):
        items = [{"title": "OWASP GenAI Security Project Unveils 2026 Top 10 for LLM Applications",
                   "url": "https://genai.owasp.org/x", "published": "2026-09-02"}]
        entries = check_owasp_top10_change(items)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "owasp_top10_change")

    def test_does_not_fire_on_unrelated_post(self):
        items = [{"title": "How we use the OWASP Top 10 in our SOC", "url": "https://x", "published": "2026-09-02"}]
        entries = check_owasp_top10_change(items)
        self.assertEqual(entries, [])

    def test_does_not_fire_without_version_number(self):
        items = [{"title": "OWASP Top 10 for LLM Applications: a refresher", "url": "https://x", "published": "2026-09-02"}]
        entries = check_owasp_top10_change(items)
        self.assertEqual(entries, [])

    def test_dedups_when_already_queued(self):
        items = [{"title": "OWASP GenAI Security Project Unveils 2026 Top 10 for LLM Applications",
                   "url": "https://genai.owasp.org/x", "published": "2026-09-02"}]
        state = _state()
        for e in check_owasp_top10_change(items):
            add_entry(state, e)
        # Running detection again on the same feed item must not add a duplicate.
        added_second_time = [add_entry(state, e) for e in check_owasp_top10_change(items)]
        self.assertEqual(added_second_time, [False])


if __name__ == '__main__':
    unittest.main()
