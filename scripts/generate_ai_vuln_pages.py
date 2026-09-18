#!/usr/bin/env python3
"""
Reads data/ai-vuln-content.json, writes one ai-vulnerabilities/<id>.html per
technique, and regenerates the summary-card grid inside owasp-llm-top10.html
between the AI-VULN-GRID markers. Run whenever data/ai-vuln-content.json
changes (manually, or by the aggregate_ai_vuln_intel.py pipeline in Task 12).

Usage: python3 scripts/generate_ai_vuln_pages.py
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / 'scripts'))

from lib.ai_vuln_pages import render_technique_page
from lib.templates import esc

CONTENT_PATH = REPO_ROOT / "data" / "ai-vuln-content.json"
OUTPUT_DIR = REPO_ROOT / "ai-vulnerabilities"
# Each entry's "framework" field selects its hub. Adding a framework here plus
# entries in data/ai-vuln-content.json is all a new technique library needs;
# the hub page itself must carry the AI-VULN-GRID markers.
FRAMEWORKS = {
    "owasp-llm-top10": ("owasp-llm-top10.html", "OWASP LLM Top 10"),
    "owasp-agentic-skills-top10": ("agentic-skills-top-10.html", "OWASP Agentic Skills Top 10"),
}

# Matches every id currently in data/ai-vuln-content.json (e.g.
# "llm01-prompt-injection"); guards against a malformed id building a write
# path that escapes OUTPUT_DIR.
VALID_ID_RE = re.compile(r'^[a-z0-9.-]+$')

GRID_START = "<!-- AI-VULN-GRID-START -->"
GRID_END = "<!-- AI-VULN-GRID-END -->"


def replace_grid_section(hub_html, grid_html):
    pattern = re.compile(re.escape(GRID_START) + r".*?" + re.escape(GRID_END), re.S)
    if not pattern.search(hub_html):
        raise ValueError(f"{GRID_START} / {GRID_END} markers not found in hub page")
    return pattern.sub(f"{GRID_START}\n{grid_html}\n{GRID_END}", hub_html)


def render_grid(techniques):
    cards = []
    for t in techniques:
        cards.append(f'''                <a href="ai-vulnerabilities/{t["id"]}.html" style="display:block;padding:1.25rem;background:var(--bg-tertiary,#f8f9fa);border-radius:8px;text-decoration:none;border:2px solid var(--border-color,#e0e0e0);">
                    <strong style="display:block;margin-bottom:0.4rem;color:var(--text-primary,#333);">{esc(t["code"])}: {esc(t["name"])}</strong>
                    <span style="font-size:0.85rem;font-weight:700;color:{esc(t["risk_color"])};">{esc(t["risk_level"])}</span>
                </a>''')
    return f'''            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;">
{chr(10).join(cards)}
            </div>'''


def main():
    data = json.loads(CONTENT_PATH.read_text(encoding='utf-8'))
    techniques = data["techniques"]
    last_updated = data["lastUpdated"]

    for t in techniques:
        if not VALID_ID_RE.fullmatch(t["id"]):
            raise ValueError(f'Invalid technique id {t["id"]!r} — must match {VALID_ID_RE.pattern}')
        if t.get("framework") not in FRAMEWORKS:
            raise ValueError(f'Unknown framework {t.get("framework")!r} on {t["id"]} — add it to FRAMEWORKS')

    OUTPUT_DIR.mkdir(exist_ok=True)
    for t in techniques:
        hub_url, hub_name = FRAMEWORKS[t["framework"]]
        html = render_technique_page(t, hub_url=hub_url, hub_name=hub_name, last_updated=last_updated)
        (OUTPUT_DIR / f'{t["id"]}.html').write_text(html, encoding='utf-8')
    print(f"Wrote {len(techniques)} pages to {OUTPUT_DIR}/")

    for framework, (hub_url, _) in FRAMEWORKS.items():
        members = [t for t in techniques if t["framework"] == framework]
        hub_path = REPO_ROOT / hub_url
        hub_html = hub_path.read_text(encoding='utf-8')
        hub_path.write_text(replace_grid_section(hub_html, render_grid(members)), encoding='utf-8')
        print(f"Updated grid in {hub_path}")


if __name__ == "__main__":
    main()
