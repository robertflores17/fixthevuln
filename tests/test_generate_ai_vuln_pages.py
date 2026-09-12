# tests/test_generate_ai_vuln_pages.py
"""Guards the hub-grid regeneration boundary: re-running the generator must
replace only the content between the AI-VULN-GRID markers and leave every
other line of owasp-llm-top10.html byte-identical, so hand-edits to the
intro/quiz/takeaways/summary-table sections survive regeneration."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from generate_ai_vuln_pages import replace_grid_section

BEFORE = "before-marker\n<!-- AI-VULN-GRID-START -->\nold grid\n<!-- AI-VULN-GRID-END -->\nafter-marker"


class TestReplaceGridSection(unittest.TestCase):
    def test_replaces_only_between_markers(self):
        result = replace_grid_section(BEFORE, "new grid")
        self.assertIn("before-marker", result)
        self.assertIn("after-marker", result)
        self.assertIn("new grid", result)
        self.assertNotIn("old grid", result)

    def test_idempotent_on_second_run(self):
        once = replace_grid_section(BEFORE, "new grid")
        twice = replace_grid_section(once, "new grid")
        self.assertEqual(once, twice)

    def test_missing_markers_raises(self):
        with self.assertRaises(ValueError):
            replace_grid_section("no markers here", "new grid")


if __name__ == '__main__':
    unittest.main()
