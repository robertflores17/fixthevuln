"""Covers the OWASP version-change detector's riskiest case: it must fire on
a genuine new-version announcement but NOT false-positive on a post that
merely mentions the Top 10 in passing (e.g. a "how we use the OWASP Top 10"
commentary post) or re-fire on a title it's already queued."""
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from aggregate_ai_vuln_intel import (
    check_atlas_techniques, check_owasp_top10_change, check_framework_ghsa,
    resolve_atlas_signals,
)
from lib.ai_vuln_intel_store import add_entry, get_atlas_known_ids, set_atlas_known_ids

# Fixed cutoff for GHSA recency tests: a 7-day window ending 2026-09-03,
# matching the fixture advisories' 2026-09-01 published_at dates.
_CUTOFF_7D = datetime(2026, 8, 27, tzinfo=timezone.utc)


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


class TestCheckAtlasTechniques(unittest.TestCase):
    def test_flags_new_remote_technique(self):
        entries = check_atlas_techniques(
            remote_technique_ids=["AML.T0051", "AML.T0043"],
            known_ids={"AML.T0051"},
        )
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "atlas_technique_change")
        self.assertIn("AML.T0043", entries[0]["id"])

    def test_no_entries_when_nothing_new(self):
        entries = check_atlas_techniques(
            remote_technique_ids=["AML.T0051"],
            known_ids={"AML.T0051"},
        )
        self.assertEqual(entries, [])

    def test_empty_remote_list_produces_no_entries(self):
        # A failed fetch (Step 1's endpoint 404s or times out) must degrade
        # to "nothing new" rather than flagging every known technique as missing.
        entries = check_atlas_techniques(remote_technique_ids=[], known_ids={"AML.T0051"})
        self.assertEqual(entries, [])


class TestCheckFrameworkGhsa(unittest.TestCase):
    def test_creates_one_entry_per_advisory(self):
        advisories_by_repo = {
            "langchain-ai/langchain": [
                {"ghsa_id": "GHSA-aaaa-bbbb-cccc", "summary": "SSRF in loader",
                 "html_url": "https://github.com/advisories/GHSA-aaaa-bbbb-cccc",
                 "published_at": "2026-09-01T00:00:00Z"},
            ]
        }
        entries = check_framework_ghsa(advisories_by_repo, _CUTOFF_7D)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "framework_ghsa")
        self.assertIn("GHSA-aaaa-bbbb-cccc", entries[0]["id"])

    def test_no_advisories_produces_no_entries(self):
        self.assertEqual(check_framework_ghsa({"vllm-project/vllm": []}, _CUTOFF_7D), [])

    def test_multiple_repos_each_contribute(self):
        advisories_by_repo = {
            "ollama/ollama": [{"ghsa_id": "GHSA-1111-2222-3333", "summary": "x",
                                "html_url": "https://x", "published_at": "2026-09-01T00:00:00Z"}],
            "huggingface/transformers": [{"ghsa_id": "GHSA-4444-5555-6666", "summary": "y",
                                           "html_url": "https://x", "published_at": "2026-09-01T00:00:00Z"}],
        }
        entries = check_framework_ghsa(advisories_by_repo, _CUTOFF_7D)
        self.assertEqual(len(entries), 2)

    def test_advisory_outside_recency_window_excluded(self):
        # Published 2023-01-01, well before the 7-day cutoff off _NOW.
        advisories_by_repo = {
            "vllm-project/vllm": [{"ghsa_id": "GHSA-old-old-oldd", "summary": "stale",
                                    "html_url": "https://x", "published_at": "2023-01-01T00:00:00Z"}],
        }
        self.assertEqual(check_framework_ghsa(advisories_by_repo, _CUTOFF_7D), [])

    def test_advisory_inside_recency_window_included(self):
        advisories_by_repo = {
            "vllm-project/vllm": [{"ghsa_id": "GHSA-new-new-newd", "summary": "fresh",
                                    "html_url": "https://x", "published_at": "2026-09-01T00:00:00Z"}],
        }
        entries = check_framework_ghsa(advisories_by_repo, _CUTOFF_7D)
        self.assertEqual(len(entries), 1)


class TestAtlasBaseline(unittest.TestCase):
    """Fix 2a: first run must baseline (queue nothing); only later runs
    diff against that baseline, so the real ~197-technique ATLAS repo
    doesn't flood the queue on day one."""

    def test_first_run_queues_nothing_but_writes_baseline(self):
        state = _state()
        self.assertIsNone(get_atlas_known_ids(state))
        entries, new_baseline = resolve_atlas_signals(
            remote_ids=["AML.T0051", "AML.T0043"], known_ids=get_atlas_known_ids(state))
        self.assertEqual(entries, [])
        self.assertEqual(new_baseline, {"AML.T0051", "AML.T0043"})

    def test_second_run_queues_only_genuinely_new_ids(self):
        state = _state()
        set_atlas_known_ids(state, {"AML.T0051", "AML.T0043"})
        entries, new_baseline = resolve_atlas_signals(
            remote_ids=["AML.T0051", "AML.T0043", "AML.T0099"],
            known_ids=get_atlas_known_ids(state))
        self.assertEqual(len(entries), 1)
        self.assertIn("AML.T0099", entries[0]["id"])
        self.assertEqual(new_baseline, {"AML.T0051", "AML.T0043", "AML.T0099"})

    def test_failed_fetch_does_not_touch_baseline(self):
        entries, new_baseline = resolve_atlas_signals(remote_ids=[], known_ids={"AML.T0051"})
        self.assertEqual(entries, [])
        self.assertIsNone(new_baseline)


if __name__ == '__main__':
    unittest.main()
