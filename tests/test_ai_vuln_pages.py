"""Covers the one thing that would silently create an XSS hole: any
attacker-influenced string (name, summary_html passed through unescaped
by mistake) must not appear un-escaped where esc() was supposed to run."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from lib.ai_vuln_pages import render_technique_page

SAMPLE = {
    "id": "llm01-prompt-injection",
    "framework": "owasp-llm-top10",
    "code": "LLM01",
    "name": "Prompt Injection",
    "risk_level": "Critical",
    "risk_color": "#ef4444",
    "summary_html": "<p>Test summary</p>",
    "sections": [{"heading": "Attack Example", "html": "<p>example</p>"}],
    "mitigations": ["Do the thing", "Do the other thing"],
    "related_links": [],
}


class TestRenderTechniquePage(unittest.TestCase):
    def test_includes_code_and_name_in_title(self):
        html = render_technique_page(SAMPLE, hub_url="/owasp-llm-top10.html", hub_name="OWASP LLM Top 10")
        self.assertIn("LLM01: Prompt Injection", html)

    def test_includes_all_mitigations(self):
        html = render_technique_page(SAMPLE, hub_url="/owasp-llm-top10.html", hub_name="OWASP LLM Top 10")
        self.assertIn("Do the thing", html)
        self.assertIn("Do the other thing", html)

    def test_escapes_name_field(self):
        entry = dict(SAMPLE, name='Prompt Injection<script>alert(1)</script>')
        html = render_technique_page(entry, hub_url="/owasp-llm-top10.html", hub_name="OWASP LLM Top 10")
        self.assertNotIn('<script>alert(1)</script>', html)

    def test_links_back_to_hub(self):
        html = render_technique_page(SAMPLE, hub_url="/owasp-llm-top10.html", hub_name="OWASP LLM Top 10")
        self.assertIn('href="../owasp-llm-top10.html"', html)


if __name__ == '__main__':
    unittest.main()
