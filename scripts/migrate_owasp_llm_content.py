#!/usr/bin/env python3
"""
One-time migration: extract the 10 OWASP LLM Top 10 sections currently
inline in owasp-llm-top10.html into data/ai-vuln-content.json, verbatim.
Run once as part of the ai-vulnerabilities/ rollout (Task 2). Not part of
the recurring pipeline — safe to delete after a successful run, kept here
for reference/re-run if the migration needs to be redone.

Usage: python3 scripts/migrate_owasp_llm_content.py
"""
import json
import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "owasp-llm-top10.html"
OUTPUT = REPO_ROOT / "data" / "ai-vuln-content.json"

CODE_TO_SLUG = {
    "LLM01": "llm01-prompt-injection",
    "LLM02": "llm02-sensitive-information-disclosure",
    "LLM03": "llm03-supply-chain-vulnerabilities",
    "LLM04": "llm04-data-and-model-poisoning",
    "LLM05": "llm05-improper-output-handling",
    "LLM06": "llm06-excessive-agency",
    "LLM07": "llm07-system-prompt-leakage",
    "LLM08": "llm08-vector-and-embedding-weaknesses",
    "LLM09": "llm09-misinformation",
    "LLM10": "llm10-unbounded-consumption",
}

RISK_COLOR_TO_LABEL = {
    "#ef4444": "Critical",
    "#fd7e14": "High",
    "#ffc107": "Medium",
}


def split_sections(html):
    """Split the file into the 10 <!-- LLM0X --> ... blocks, each running
    until the next <!-- LLM0X --> marker or <!-- Summary Table -->."""
    marker_positions = [m.start() for m in re.finditer(r'<!-- LLM\d\d -->', html)]
    end_marker = html.index('<!-- Summary Table -->')
    blocks = []
    for i, start in enumerate(marker_positions):
        end = marker_positions[i + 1] if i + 1 < len(marker_positions) else end_marker
        blocks.append(html[start:end])
    return blocks


def parse_block(block):
    code = re.search(r'<!-- (LLM\d\d) -->', block).group(1)
    name = re.search(rf'<h2>{code}: (.+?)</h2>', block).group(1)
    risk_color = re.search(r'color:\s*(#[0-9a-fA-F]{6})', block).group(1)
    risk_level = RISK_COLOR_TO_LABEL.get(risk_color.lower(), "Unknown")

    # Summary paragraph: the <p> immediately after the Risk Level line, before the first <h3>
    after_risk = block.split('</p>', 1)[1]  # drop the "Risk Level:" line itself
    first_h3_idx = after_risk.find('<h3>')
    summary_html = after_risk[:first_h3_idx].strip()
    if not summary_html.startswith('<p>'):
        summary_html = ''  # no separate summary paragraph in this block

    # h3 subsections (Attack Example, Real-World Example, etc.) up to <h3>Mitigations</h3>
    sections = []
    h3_matches = list(re.finditer(r'<h3>(.+?)</h3>', block))
    for i, m in enumerate(h3_matches):
        heading = m.group(1)
        if heading == 'Mitigations':
            continue
        content_start = m.end()
        content_end = h3_matches[i + 1].start() if i + 1 < len(h3_matches) else block.index('<div class="remediation">')
        sections.append({"heading": heading, "html": block[content_start:content_end].strip()})

    # Mitigations: every <li> inside <div class="remediation">
    remediation_block = block.split('<div class="remediation">', 1)[1].split('</div>', 1)[0]
    mitigations = [
        re.sub(r'<input[^>]*>\s*', '', li).strip()
        for li in re.findall(r'<li>(.*?)</li>', remediation_block, re.S)
    ]

    # Related links already embedded as <a href="...">...</a> inside summary/sections text
    # are left in place (not extracted separately) — they render correctly wherever they land.

    return {
        "id": CODE_TO_SLUG[code],
        "framework": "owasp-llm-top10",
        "code": code,
        "name": name,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "summary_html": summary_html,
        "sections": sections,
        "mitigations": mitigations,
        "related_links": [],
    }


def main():
    html = SOURCE.read_text()
    blocks = split_sections(html)
    assert len(blocks) == 10, f"Expected 10 LLM sections, found {len(blocks)}"
    techniques = [parse_block(b) for b in blocks]
    OUTPUT.write_text(json.dumps({
        "lastUpdated": date.today().isoformat(),
        "techniques": techniques,
    }, indent=2))
    print(f"Wrote {len(techniques)} techniques to {OUTPUT}")


if __name__ == "__main__":
    main()
