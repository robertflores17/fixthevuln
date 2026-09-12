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
HUB_PATH = REPO_ROOT / "owasp-llm-top10.html"
HUB_URL = "owasp-llm-top10.html"
HUB_NAME = "OWASP LLM Top 10"

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
                    <strong style="display:block;margin-bottom:0.4rem;color:var(--text-primary,#333);">{t["code"]}: {esc(t["name"])}</strong>
                    <span style="font-size:0.85rem;font-weight:700;color:{t["risk_color"]};">{esc(t["risk_level"])}</span>
                </a>''')
    return f'''            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;">
{chr(10).join(cards)}
            </div>'''


def main():
    data = json.loads(CONTENT_PATH.read_text())
    techniques = data["techniques"]

    OUTPUT_DIR.mkdir(exist_ok=True)
    for t in techniques:
        html = render_technique_page(t, hub_url=HUB_URL, hub_name=HUB_NAME)
        (OUTPUT_DIR / f'{t["id"]}.html').write_text(html)
    print(f"Wrote {len(techniques)} pages to {OUTPUT_DIR}/")

    hub_html = HUB_PATH.read_text()
    grid_html = render_grid(techniques)
    HUB_PATH.write_text(replace_grid_section(hub_html, grid_html))
    print(f"Updated grid in {HUB_PATH}")


if __name__ == "__main__":
    main()
