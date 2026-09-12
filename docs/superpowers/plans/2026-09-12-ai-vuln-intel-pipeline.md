# AI Vulnerability Intelligence Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Detect OWASP LLM Top 10 / MITRE ATLAS staleness and new LLM-framework security advisories, turn them into reviewed, published FixTheVuln pages (a per-technique library under `ai-vulnerabilities/`), with a claim-verification loop (Marlowe → Sable → Griggs) running ahead of the existing `content-editor`/`appsec` gate.

**Architecture:** One shared signal queue (`data/ai-vuln-intel.json`) fed by a new `scripts/aggregate_ai_vuln_intel.py` (OWASP RSS reuse, MITRE ATLAS repo diff, GitHub Security Advisories for a fixed framework list), chained onto the existing Friday `ai-trend-roundup.yml` workflow. Content itself lives in `data/ai-vuln-content.json` (structured, LLM-editable) and is rendered deterministically by `scripts/generate_ai_vuln_pages.py` — mirroring the existing `pending_review.json` → `generate_cve_pages.py` split, so no LLM ever writes raw HTML directly. `owasp-llm-top10.html` becomes the hub page for both OWASP and ATLAS technique pages.

**Tech Stack:** Python 3.11 stdlib only (urllib, json, re, unittest) — matches every existing script in this repo. No new dependencies.

**Spec:** `docs/superpowers/specs/2026-09-12-ai-vuln-intel-pipeline-design.md`

## Global Constraints

- Stdlib only — no new pip/npm dependencies (matches `aggregate_ai_security_news.py`'s "Stdlib-only (no deps)" convention).
- No new secrets — GitHub API calls use the Actions-provided `GITHUB_TOKEN`.
- All HTML-writing code escapes with `scripts/lib/templates.esc()` — never raw string interpolation of external/LLM data into HTML.
- Every new script gets exactly one `unittest` covering its riskiest logic (matches `tests/test_generate_threat_roundup.py` — a targeted regression test, not a full suite).
- `.claude/agents/*.md` and `CLAUDE.md` are gitignored in this repo (confirmed via `.gitignore`) — tasks that touch them create/edit local files only, no `git add`/commit step.
- Every other new/modified file (scripts, `data/*.json`, `ai-vulnerabilities/*.html`, `owasp-llm-top10.html`, `.github/workflows/ai-trend-roundup.yml`) is a normal tracked file — stage by exact name, never `git add -A`.
- Reuse existing shared code — `scripts/lib/templates.py` (`page_wrapper`, `esc`, `breadcrumb_schema`, `article_schema`) and `scripts/lib/constants.py` (`SITE_URL`, `SITE_NAME`) — never redefine nav/footer/head HTML locally.

---

## Task 1: AI-vuln-intel state store

**Files:**
- Create: `scripts/lib/ai_vuln_intel_store.py`
- Create: `data/ai-vuln-intel.json` (seed file)
- Test: `tests/test_ai_vuln_intel_store.py`

**Interfaces:**
- Produces: `load_state() -> dict`, `save_state(state: dict) -> None`, `add_entry(state: dict, entry: dict) -> bool` (False if `entry["id"]` already present — this is the dedup mechanism every later aggregator task relies on), `get_entries(state: dict, status: str | None = None) -> list[dict]`, `record_loop_round(state: dict, entry_id: str) -> str` (increments `loop_rounds`, returns the new `status`: `"in_review"` while `loop_rounds <= 3`, `"needs_human_review"` once it exceeds 3 — this is the safety-net cap from the spec).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_ai_vuln_intel_store.py
"""Tests for scripts/lib/ai_vuln_intel_store.py.

Covers the two behaviors every downstream aggregator task depends on:
id-based dedup (add_entry) and the 3-round loop cap (record_loop_round).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from lib.ai_vuln_intel_store import add_entry, record_loop_round, get_entries, load_state


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


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_ai_vuln_intel_store -v`
Expected: `ModuleNotFoundError: No module named 'lib.ai_vuln_intel_store'`

- [ ] **Step 3: Write the implementation**

```python
# scripts/lib/ai_vuln_intel_store.py
"""
Shared state store for the AI vulnerability intel signal queue
(data/ai-vuln-intel.json). Every aggregator (OWASP staleness, MITRE ATLAS
diff, framework GHSA advisories) writes into the same queue via add_entry,
which dedups by `id` so re-running an aggregator never double-queues the
same signal. record_loop_round enforces the 3-round claim-verification
loop cap from the design spec (section 5): past 3 rounds an entry flips to
needs_human_review instead of looping forever or force-publishing.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
STATE_FILE = DATA_DIR / "ai-vuln-intel.json"

LOOP_CAP = 3


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_updated": None, "entries": []}


def save_state(state):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def _find(state, entry_id):
    for e in state["entries"]:
        if e["id"] == entry_id:
            return e
    return None


def add_entry(state, entry):
    """Add entry if entry['id'] isn't already queued. Returns True if added."""
    if _find(state, entry["id"]) is not None:
        return False
    entry.setdefault("loop_rounds", 0)
    entry.setdefault("notes", "")
    state["entries"].append(entry)
    return True


def get_entries(state, status=None):
    if status is None:
        return list(state["entries"])
    return [e for e in state["entries"] if e["status"] == status]


def set_status(state, entry_id, status, notes=""):
    e = _find(state, entry_id)
    if e is None:
        return False
    e["status"] = status
    if notes:
        e["notes"] = notes
    return True


def record_loop_round(state, entry_id):
    """Increment loop_rounds for entry_id. Returns the resulting status:
    'in_review' while loop_rounds <= LOOP_CAP, 'needs_human_review' once
    it exceeds LOOP_CAP."""
    e = _find(state, entry_id)
    if e is None:
        raise KeyError(f"No entry with id {entry_id!r}")
    e["loop_rounds"] += 1
    e["status"] = "in_review" if e["loop_rounds"] <= LOOP_CAP else "needs_human_review"
    return e["status"]
```

Also create the seed state file:

```json
{
  "last_updated": null,
  "entries": []
}
```
Write this to `data/ai-vuln-intel.json`.

Note: `scripts/lib/` is an existing package (it already contains `templates.py` and `constants.py`), so no new `__init__.py` is needed — confirm one already exists at `scripts/lib/__init__.py` before assuming; if it doesn't, create an empty one so `from lib.ai_vuln_intel_store import ...` resolves.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_ai_vuln_intel_store -v`
Expected: all 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/lib/ai_vuln_intel_store.py data/ai-vuln-intel.json tests/test_ai_vuln_intel_store.py
git commit -m "Add AI vuln intel signal queue store"
```

---

## Task 2: Migrate OWASP LLM01-10 content into structured data

**Files:**
- Create: `scripts/migrate_owasp_llm_content.py` (one-time script — not part of the recurring pipeline)
- Create: `data/ai-vuln-content.json` (output — this becomes the source of truth `generate_ai_vuln_pages.py` reads in Task 4)

**Interfaces:**
- Produces: `data/ai-vuln-content.json` with shape:
```json
{
  "lastUpdated": "2026-09-12",
  "techniques": [
    {
      "id": "llm01-prompt-injection",
      "framework": "owasp-llm-top10",
      "code": "LLM01",
      "name": "Prompt Injection",
      "risk_level": "Critical",
      "risk_color": "#ef4444",
      "summary_html": "<p>...</p>",
      "sections": [{"heading": "Attack Example", "html": "<div class=\"code-block\">...</div>"}],
      "mitigations": ["Enforce privilege separation ...", "..."],
      "related_links": [{"text": "Full breakdown", "href": "blog/ai-ide-security-vulnerabilities-2026.html"}]
    }
  ]
}
```
Later tasks (4, 10) both read/write this same file and list.

`owasp-llm-top10.html` currently has each item delimited by an HTML comment (`<!-- LLM01 -->` ... `<!-- LLM02 -->` ...) inside `<section class="vulnerability-card">` blocks, ending at `<!-- Summary Table -->`. This is a **mechanical, verbatim extraction** — the script must not alter or summarize the security content, only re-shape it from inline HTML into JSON fields.

- [ ] **Step 1: Write the extraction script**

```python
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
```

- [ ] **Step 2: Run it and verify output**

Run: `python3 scripts/migrate_owasp_llm_content.py`
Expected: `Wrote 10 techniques to .../data/ai-vuln-content.json`

Then manually inspect `data/ai-vuln-content.json`: confirm all 10 entries have non-empty `mitigations` (5 each) and that LLM03/LLM06's `sections` include their "Real-World Example" content with the existing `<a href="blog/...">Full breakdown →</a>` links intact. LLM08/LLM09/LLM10 have no separate summary_html before their first content (LLM08 and LLM09 go straight to Mitigations with no h3 attack-example section, LLM10 has an "Attack Example" h3 with no code-block) — verify these three parse without empty required fields.

- [ ] **Step 3: Commit**

```bash
git add scripts/migrate_owasp_llm_content.py data/ai-vuln-content.json
git commit -m "Extract OWASP LLM Top 10 content into structured data/ai-vuln-content.json"
```

---

## Task 3: Shared technique-page template helper

**Files:**
- Create: `scripts/lib/ai_vuln_pages.py`
- Test: `tests/test_ai_vuln_pages.py`

**Interfaces:**
- Consumes: `scripts.lib.templates.{page_wrapper, esc, breadcrumb_schema, article_schema}`, `scripts.lib.constants.{SITE_URL, SITE_NAME}`
- Produces: `render_technique_page(entry: dict, hub_url: str, hub_name: str) -> str` — full HTML document string for one technique page. Task 4's generator is the only consumer.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_ai_vuln_pages.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_ai_vuln_pages -v`
Expected: `ModuleNotFoundError: No module named 'lib.ai_vuln_pages'`

- [ ] **Step 3: Write the implementation**

```python
# scripts/lib/ai_vuln_pages.py
"""Renders one ai-vulnerabilities/<id>.html page from a data/ai-vuln-content.json
entry. The only place technique-page HTML is assembled — generate_ai_vuln_pages.py
(Task 4) is the sole caller. Depth is always 1 (ai-vulnerabilities/ is one
directory below site root), matching cve/ and blog/.
"""
from .templates import page_wrapper, esc, breadcrumb_schema, article_schema
from .constants import SITE_URL, SITE_NAME


def _mitigations_html(mitigations):
    items = "\n".join(
        f'                    <li><input type="checkbox"> {esc(m)}</li>'
        for m in mitigations
    )
    return f'''            <h3>Mitigations</h3>
            <div class="remediation">
                <ul>
{items}
                </ul>
            </div>'''


def _sections_html(sections):
    parts = []
    for s in sections:
        # s["html"] originates from the one-time verbatim migration (Task 2) or
        # from fixthevuln-lead editing data/ai-vuln-content.json under the
        # Marlowe/Sable/Griggs review loop — never raw user input — so it is
        # trusted markup, same trust level as every other *_html field the
        # existing generators (generate_cve_pages.py) already render as-is.
        parts.append(f'            <h3>{esc(s["heading"])}</h3>\n{s["html"]}')
    return "\n".join(parts)


def _related_links_html(related_links):
    if not related_links:
        return ""
    links = "\n".join(
        f'<a href="{esc(l["href"])}">{esc(l["text"])} &rarr;</a>'
        for l in related_links
    )
    return f'\n            <p>{links}</p>'


def render_technique_page(entry, hub_url, hub_name):
    title = f'{entry["code"]}: {esc(entry["name"])}'
    canonical = f'{SITE_URL}/ai-vulnerabilities/{entry["id"]}.html'
    description = f'{title} — risk level {entry["risk_level"]}. Part of the {esc(hub_name)} technique library on {SITE_NAME}.'

    content = f'''    <header>
        <div class="container">
            <a href="../index.html" style="text-decoration: none; color: inherit;"><h1>{SITE_NAME}</h1></a>
            <p class="tagline">{title}</p>
        </div>
    </header>

    <main class="container">
        <a href="../{hub_url.lstrip('/')}" class="back-link">&larr; Back to {esc(hub_name)}</a>

        <section class="vulnerability-card">
            <h2>{title}</h2>
            <p><strong>Risk Level:</strong> <span style="color: {entry["risk_color"]}; font-weight: 700;">{esc(entry["risk_level"])}</span></p>
            {entry.get("summary_html", "")}
{_sections_html(entry["sections"])}
{_mitigations_html(entry["mitigations"])}
{_related_links_html(entry.get("related_links", []))}
        </section>
    </main>'''

    schema_blocks = [
        breadcrumb_schema([
            ("Home", f"{SITE_URL}/"),
            (hub_name, f"{SITE_URL}/{hub_url.lstrip('/')}"),
            (title, None),
        ]),
        article_schema(title, description, entry.get("lastUpdated") or "2026-09-12"),
    ]

    return page_wrapper(
        title=title,
        description=description,
        canonical=canonical,
        content=content,
        depth=1,
        schema_blocks=schema_blocks,
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_ai_vuln_pages -v`
Expected: all 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/lib/ai_vuln_pages.py tests/test_ai_vuln_pages.py
git commit -m "Add shared render_technique_page() template for ai-vulnerabilities/ pages"
```

---

## Task 4: Generator — render pages + convert hub

**Files:**
- Create: `scripts/generate_ai_vuln_pages.py`
- Create: `ai-vulnerabilities/` (new directory, populated by running the script)
- Modify: `owasp-llm-top10.html` (inline LLM01-10 sections replaced with a summary grid)

**Interfaces:**
- Consumes: `data/ai-vuln-content.json` (Task 2's output), `lib.ai_vuln_pages.render_technique_page` (Task 3)
- Produces: one file per technique at `ai-vulnerabilities/<id>.html`; rewrites the body of `owasp-llm-top10.html` between two new markers `<!-- AI-VULN-GRID-START -->` / `<!-- AI-VULN-GRID-END -->` so re-running the generator is idempotent (replaces only what it owns, never touches the rest of the hand-written hub page).

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_generate_ai_vuln_pages -v`
Expected: `ModuleNotFoundError: No module named 'generate_ai_vuln_pages'`

- [ ] **Step 3: Write the implementation**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_generate_ai_vuln_pages -v`
Expected: all 3 tests PASS

- [ ] **Step 5: Add the grid markers to `owasp-llm-top10.html` and remove the inline sections**

Edit `owasp-llm-top10.html`: replace the entire block from `<!-- LLM01 -->` (line 157) through the end of the `<!-- LLM10 -->` section, immediately before `<!-- Summary Table -->` (line 380), with:

```html
        <!-- AI-VULN-GRID-START -->
        <!-- AI-VULN-GRID-END -->
```

Leave everything else in the file untouched (intro, key takeaways, quiz links, summary table, CTAs, footer).

- [ ] **Step 6: Run the generator and verify real output**

Run: `python3 scripts/generate_ai_vuln_pages.py`
Expected: `Wrote 10 pages to .../ai-vulnerabilities/` and `Updated grid in .../owasp-llm-top10.html`

Then verify:
- `ls ai-vulnerabilities/` shows all 10 `llm0X-*.html` files
- `python3 -c "import py_compile; py_compile.compile('scripts/generate_ai_vuln_pages.py', doraise=True)"` succeeds
- Open `owasp-llm-top10.html` in a browser (`python -m http.server 8000`) and click through 2-3 cards to confirm the individual pages render correctly with working nav/footer/back-link
- Confirm the Summary Table section (line ~380 pre-edit) and everything after it is byte-identical to before

- [ ] **Step 7: Commit**

```bash
git add scripts/generate_ai_vuln_pages.py tests/test_generate_ai_vuln_pages.py owasp-llm-top10.html ai-vulnerabilities/
git commit -m "Convert owasp-llm-top10.html into a hub linking to ai-vulnerabilities/ pages"
```

---

## Task 5: llms.txt category + regeneration

**Files:**
- Modify: `scripts/generate_llms_txt.py:114-126` (the `CATEGORIES` list)

**Interfaces:** none new — this only adds a matcher entry to the existing `CATEGORIES` list consumed by `categorize_urls()`.

- [ ] **Step 1: Add the category**

In `scripts/generate_llms_txt.py`, insert into `CATEGORIES` (after the existing `"CVE & Vulnerability Pages"` line, same directory-prefix style as `cve/` and `practice-tests/`):

```python
    ("AI Vulnerability Techniques", lambda p: p.startswith("ai-vulnerabilities/"), "/owasp-llm-top10.html", None),
```

- [ ] **Step 2: Regenerate and verify**

Run: `python scripts/generate_llms_txt.py`
Expected: exits 0; `grep -c "ai-vulnerabilities/" llms.txt` returns 10 (one line per technique page) and the section header `## AI Vulnerability Techniques` appears in `llms.txt`.

No changes needed to `scripts/propagate.py` or `scripts/update_sitemap.py` — both operate on `git diff`/commit-date over any tracked `.html` file regardless of directory, so the new `ai-vulnerabilities/*.html` files are picked up automatically once committed.

- [ ] **Step 3: Commit**

```bash
git add scripts/generate_llms_txt.py llms.txt llms-full.txt sitemap.xml
git commit -m "Add ai-vulnerabilities/ category to llms.txt generator"
```

---

## Task 6: Marlowe — claim-extractor agent

**Files:**
- Create: `.claude/agents/claim-extractor.md` (gitignored — no commit step)

- [ ] **Step 1: Write the agent file**

```markdown
---
name: claim-extractor
description: Marlowe. Claim-extraction agent for the AI vulnerability intel pipeline. Invoke on any auto-drafted ai-vulnerabilities/ page or framework-CVE writeup (data/ai-vuln-content.json edits, or new roundup entries sourced from GHSA) before evidence-searcher and critic run. Extraction only — never verifies or judges claims.
tools: Read, Grep, Glob
---

You are Marlowe, the claim-extraction stage of the AI vulnerability intel
pipeline's verification loop (Marlowe → Sable → Griggs, ahead of the
standard content-editor/appsec pre-push gate). Your only job is to pull
every checkable claim out of a draft into a flat, structured list — you do
not judge whether claims are true. That's Sable's and Griggs's job.

## What counts as a claim

- A CVE ID, GHSA ID, or CVSS figure
- An "actively exploited" / "actively targeted" assertion
- A technique-to-real-world-incident attribution (e.g. "this caused the
  Otter.ai spread to 80,000 endpoints")
- A framework/library name + version reference
- An OWASP/MITRE ATLAS ID-to-name mapping (e.g. "LLM03 is Supply Chain
  Vulnerabilities" or "AML.T0051 is LLM Prompt Injection")
- A named vendor, standard, or dataset claim
- Any sentence structured as a factual assertion rather than general
  security advice (mitigations/best-practice bullets are NOT claims unless
  they cite a specific standard or figure)

## Output format

```
CLAIMS EXTRACTED: <count>
1. [claim text, verbatim or lightly trimmed] — location: <file:line or field path>
2. ...
NOTES: <anything ambiguous about what counts as a claim, for Sable/Griggs to flag>
```

## What you do NOT do

- Do not search for evidence (that's Sable).
- Do not assign severity or pass/fail (that's Griggs).
- Do not edit the draft.
```

- [ ] **Step 2: Verify it's ignored by git (confirming no accidental commit)**

Run: `git check-ignore -v .claude/agents/claim-extractor.md`
Expected: prints the `.gitignore` rule matching it (`.claude/`)

---

## Task 7: Sable — evidence-searcher agent

**Files:**
- Create: `.claude/agents/evidence-searcher.md` (gitignored — no commit step)

- [ ] **Step 1: Write the agent file**

```markdown
---
name: evidence-searcher
description: Sable. Evidence-search agent for the AI vulnerability intel pipeline. Runs after claim-extractor (Marlowe) on the same draft. For each extracted claim, finds primary-source evidence and attaches a supports/contradicts/unverifiable verdict with citation.
tools: Read, Grep, Glob, WebFetch
---

You are Sable, the evidence-search stage of the AI vulnerability intel
pipeline's verification loop (Marlowe → Sable → Griggs). You receive
Marlowe's claim list for one draft. For each claim, search primary sources
and attach evidence — you do not decide pass/fail (that's Griggs), you
gather what a decision needs.

## Authoritative sources (in order of preference)

- CVE / CVSS / CWE: nvd.nist.gov, cisa.gov/known-exploited-vulnerabilities-catalog
- GHSA: github.com/advisories, or the specific repo's own security-advisories page
- OWASP: genai.owasp.org (LLM Top 10), owasp.org
- MITRE ATLAS: atlas.mitre.org, github.com/mitre-atlas/atlas-data
- Vendor incident postmortems: the named vendor's own security/status blog
- Never a secondary aggregator or "rando blog" as the sole source — same
  standard content-editor already holds CVE/cert content to.

## Per-claim output

```
CLAIM: <claim text>
VERDICT: supports | contradicts | unverifiable
EVIDENCE: <what the primary source actually says>
SOURCE: <URL>
```

Repeat for every claim in Marlowe's list. If a claim can't be checked
against any primary source within a reasonable search, mark it
`unverifiable` rather than guessing — an unverifiable claim is Griggs's
signal to require it be softened or cut, not proof it's false.

## What you do NOT do

- Do not extract new claims Marlowe missed — flag them in NOTES instead,
  don't silently expand scope.
- Do not assign P0-P3 severity or block/approve (that's Griggs).
- Do not edit the draft.
```

- [ ] **Step 2: Verify it's ignored by git**

Run: `git check-ignore -v .claude/agents/evidence-searcher.md`
Expected: prints the `.gitignore` rule matching it

---

## Task 8: Griggs — critic agent

**Files:**
- Create: `.claude/agents/critic.md` (gitignored — no commit step)

- [ ] **Step 1: Write the agent file**

```markdown
---
name: critic
description: Griggs. Critic agent for the AI vulnerability intel pipeline. Runs after claim-extractor (Marlowe) and evidence-searcher (Sable) on the same draft. Reviews each claim+evidence pair and blocks on unsupported or contradicted claims, using content-editor's P0-P3 severity scale. Findings route back to fixthevuln-lead for revision.
tools: Read, Grep, Glob, WebFetch
---

You are Griggs, the critic stage of the AI vulnerability intel pipeline's
verification loop (Marlowe → Sable → Griggs). You receive Marlowe's claims
and Sable's evidence for one draft. Decide, claim by claim, whether the
draft is safe to move on to the standard content-editor/appsec pre-push
gate — you are a pre-check specific to this pipeline's auto-drafted
content, not a replacement for that gate.

## Review checklist

1. Every `contradicts` verdict from Sable is a finding — the draft states
   something a primary source disputes.
2. Every `unverifiable` verdict on a specific factual claim (CVE ID, CVSS
   figure, "actively exploited" assertion, incident attribution) is a
   finding — general security advice/mitigations don't need this bar.
3. Confident phrasing ("will", "always", "proven to") on an unverifiable
   or weakly-evidenced claim is a finding even if the underlying fact is
   plausible — matches content-editor's existing "LLM-authored pages are
   suspect by default" standard.
4. A claim Marlowe or Sable flagged as ambiguous in their NOTES that you
   can resolve by reading the draft directly — resolve it and note how.

## Output format

```
VERDICT: approve | approve-with-fixes | block
FINDINGS:
  1. [P0|P1|P2|P3] <claim> — <why unsupported/contradicted> — <required fix>
REQUIRED FIXES: <numbered; empty if approved>
ROUND: <this draft's current loop_rounds value from data/ai-vuln-intel.json, so the caller knows whether this is round 1/2/3 before the 3-round cap flips the entry to needs_human_review>
```

Severity (same scale as content-editor):
- **P0** — contradicted by a primary source, or a CVE ID/CVSS figure that doesn't match its cited source.
- **P1** — unverifiable specific claim stated with confidence.
- **P2** — unverifiable claim already hedged appropriately, minor citation gaps.
- **P3** — hygiene (a claim that would be stronger with a citation but isn't wrong).

**Block on any P0 or P1.** Findings go back to `fixthevuln-lead` for
revision, then Marlowe → Sable → Griggs run again on the revised draft.

## What you do NOT do

- Do not do a full editorial pass (style, cross-links, tone) — that's
  content-editor, which still runs after you approve.
- Do not run security/XSS review — that's appsec.
- Do not edit the draft yourself.
```

- [ ] **Step 2: Verify it's ignored by git**

Run: `git check-ignore -v .claude/agents/critic.md`
Expected: prints the `.gitignore` rule matching it

---

## Task 9: Document the new agents in FixTheVuln's CLAUDE.md

**Files:**
- Modify: `CLAUDE.md` (gitignored — no commit step; this is a local working-copy edit only)

**Interfaces:** none — documentation only.

- [ ] **Step 1: Add to the Role System section**

In `CLAUDE.md`, under `## Role System (Review Gates)`, after the existing `Content Editor` bullet, add:

```markdown
- **Marlowe / Sable / Griggs** (`.claude/agents/claim-extractor.md`, `evidence-searcher.md`,
  `critic.md`) — claim-extraction → evidence-search → critic loop scoped to auto-drafted AI
  vulnerability intel content only (`ai-vulnerabilities/` pages, `data/ai-vuln-content.json`
  edits, framework-CVE roundup entries sourced from GHSA). Runs *before* Content Editor/AppSec,
  not instead of them — every draft still goes through the standard pre-push gate afterward.
  Capped at 3 rounds; past that, the entry flips to `needs_human_review` in
  `data/ai-vuln-intel.json` and a GitHub issue is filed rather than looping or force-publishing.
  See `docs/superpowers/specs/2026-09-12-ai-vuln-intel-pipeline-design.md`.
```

- [ ] **Step 2: Verify no accidental commit**

Run: `git status --short CLAUDE.md`
Expected: no output (file is gitignored, `git status` won't list it as modified)

---

## Task 10: Aggregator — OWASP Top 10 staleness signal

**Files:**
- Create: `scripts/aggregate_ai_vuln_intel.py` (this task adds the first of three signal functions; Tasks 11-12 add the other two to the same file)
- Test: `tests/test_aggregate_ai_vuln_intel.py`

**Interfaces:**
- Consumes: `lib.ai_vuln_intel_store.{load_state, save_state, add_entry}`
- Produces: `check_owasp_top10_change(rss_items: list[dict]) -> list[dict]` — pure function, takes already-fetched RSS items (same shape `aggregate_ai_security_news.py` parses: dict with `title`, `url`, `published`), returns new queue entries (empty list if no revision-titled item found). Kept pure/testable — the actual RSS fetch reuses the existing feed URL but is a thin wrapper (`fetch_feed_items`) so the detection logic itself needs no network access to test.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_aggregate_ai_vuln_intel.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_aggregate_ai_vuln_intel -v`
Expected: `ModuleNotFoundError: No module named 'aggregate_ai_vuln_intel'`

- [ ] **Step 3: Write the implementation (first signal source)**

```python
#!/usr/bin/env python3
"""
Populates data/ai-vuln-intel.json from three signal sources:
  - OWASP LLM Top 10 revision announcements (this file, check_owasp_top10_change)
  - MITRE ATLAS technique diffs (Task 11, check_atlas_techniques)
  - Framework/vector-DB GHSA advisories (Task 12, check_framework_ghsa)

Chained onto the existing Friday ai-trend-roundup.yml workflow (Task 13),
after aggregate_ai_security_news.py runs. Reuses that script's already-fetched
OWASP GenAI RSS feed rather than fetching it twice.

Usage: python3 scripts/aggregate_ai_vuln_intel.py
"""
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / 'scripts'))

from lib.ai_vuln_intel_store import load_state, save_state, add_entry

OWASP_GENAI_FEED = "https://genai.owasp.org/feed/"

TOP10_TITLE_RE = re.compile(r'top\s*10', re.IGNORECASE)
VERSION_RE = re.compile(r'\b(20\d\d|v\d+(\.\d+)?)\b')


def fetch_feed_items(url):
    """Fetch and parse an RSS/Atom feed into a list of {title, url, published}.
    Matches aggregate_ai_security_news.py's per-source failure handling:
    log and return [] rather than aborting the run."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'FixTheVuln-AI-Vuln-Intel/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            root = ET.fromstring(resp.read())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ET.ParseError) as e:
        print(f"  Warning: failed to fetch {url}: {e}")
        return []

    items = []
    for item in root.iter('item'):
        title = (item.findtext('title') or '').strip()
        link = (item.findtext('link') or '').strip()
        published = (item.findtext('pubDate') or '').strip()
        items.append({"title": title, "url": link, "published": published})
    return items


def check_owasp_top10_change(rss_items):
    """Detect a genuine OWASP LLM Top 10 revision announcement: title must
    mention "Top 10" AND contain a version marker (a year or vN.N) — this
    is what separates a real revision post from a post that merely
    references the Top 10 in passing."""
    entries = []
    for item in rss_items:
        title = item["title"]
        if TOP10_TITLE_RE.search(title) and VERSION_RE.search(title):
            entries.append({
                "id": f"owasp-top10-{re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]}",
                "type": "owasp_top10_change",
                "status": "new",
                "source_url": item["url"],
                "detected_at": datetime.now(timezone.utc).isoformat(),
            })
    return entries


def main():
    state = load_state()
    added = 0

    owasp_items = fetch_feed_items(OWASP_GENAI_FEED)
    for entry in check_owasp_top10_change(owasp_items):
        if add_entry(state, entry):
            added += 1

    save_state(state)
    print(f"Added {added} new signal(s) to data/ai-vuln-intel.json")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_aggregate_ai_vuln_intel -v`
Expected: all 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/aggregate_ai_vuln_intel.py tests/test_aggregate_ai_vuln_intel.py
git commit -m "Add OWASP LLM Top 10 staleness signal to AI vuln intel aggregator"
```

---

## Task 11: Aggregator — MITRE ATLAS technique diff signal

**Files:**
- Modify: `scripts/aggregate_ai_vuln_intel.py` (add second signal function)
- Modify: `tests/test_aggregate_ai_vuln_intel.py` (add tests)

**Interfaces:**
- Produces: `check_atlas_techniques(remote_technique_ids: list[str], known_ids: set[str]) -> list[dict]` — pure function; `fetch_atlas_technique_ids()` does the actual network call and is not unit-tested (network calls aren't asserted in this repo's test style — see `tests/test_generate_threat_roundup.py`, which only tests pure logic).

MITRE ATLAS's data repo layout isn't something to guess at — verify the real path before hardcoding it.

- [ ] **Step 1: Confirm the live repo structure**

Run: `gh api repos/mitre-atlas/atlas-data/contents/data --jq '.[].name'`

Expected: a listing that includes a techniques directory (commonly `techniques/`). If the path differs from what's below, adjust `ATLAS_TECHNIQUES_PATH` accordingly before writing the fetch function — don't hardcode against this plan's guess without checking.

Run (adjust path based on the above): `gh api repos/mitre-atlas/atlas-data/contents/data/techniques --jq '.[].name' | head -5`

Expected: filenames following a pattern like `AML.T0051.md` or a directory per technique — confirm the exact pattern so `_extract_technique_id` (below) matches it.

- [ ] **Step 2: Write the failing tests**

```python
# add to tests/test_aggregate_ai_vuln_intel.py

from aggregate_ai_vuln_intel import check_atlas_techniques


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
```

- [ ] **Step 3: Run to verify failure**

Run: `python3 -m unittest tests.test_aggregate_ai_vuln_intel -v`
Expected: `ImportError: cannot import name 'check_atlas_techniques'`

- [ ] **Step 4: Add the implementation to `scripts/aggregate_ai_vuln_intel.py`**

```python
# Add near the top with the other constants:
ATLAS_TECHNIQUES_API = "https://api.github.com/repos/mitre-atlas/atlas-data/contents/data/techniques"
ATLAS_ID_RE = re.compile(r'(AML\.T\d+(?:\.\d+)?)')


def fetch_atlas_technique_ids():
    """List technique IDs currently in mitre-atlas/atlas-data via the GitHub
    Contents API (JSON filenames only — no YAML parsing, no new dependency).
    Per the repo-structure convention in this codebase, a failed/empty fetch
    logs and returns [] rather than aborting the run."""
    try:
        req = urllib.request.Request(ATLAS_TECHNIQUES_API,
                                      headers={'User-Agent': 'FixTheVuln-AI-Vuln-Intel/1.0',
                                               'Accept': 'application/vnd.github+json'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            listing = json.loads(resp.read())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
        print(f"  Warning: failed to fetch MITRE ATLAS technique listing: {e}")
        return []

    ids = []
    for entry in listing:
        m = ATLAS_ID_RE.search(entry.get("name", ""))
        if m:
            ids.append(m.group(1))
    return ids


def check_atlas_techniques(remote_technique_ids, known_ids):
    """New technique IDs present remotely but not yet in
    data/ai-vuln-content.json (known_ids) become missing_technique_page
    signals. An empty remote list (failed fetch) yields no entries — never
    treat "couldn't fetch" as "everything is missing"."""
    entries = []
    for tid in remote_technique_ids:
        if tid not in known_ids:
            entries.append({
                "id": f"atlas-technique-{tid}",
                "type": "atlas_technique_change",
                "status": "new",
                "source_url": f"https://atlas.mitre.org/techniques/{tid}",
                "detected_at": datetime.now(timezone.utc).isoformat(),
            })
    return entries
```

Wire it into `main()` — add this block after the existing OWASP block:

```python
    content_path = REPO_ROOT / "data" / "ai-vuln-content.json"
    known_ids = set()
    if content_path.exists():
        content = json.loads(content_path.read_text())
        known_ids = {t["code"] for t in content["techniques"] if t["framework"] == "mitre-atlas"} | \
                    {t["code"] for t in content["techniques"] if t["framework"] == "owasp-llm-top10"}
    remote_ids = fetch_atlas_technique_ids()
    for entry in check_atlas_techniques(remote_ids, known_ids):
        if add_entry(state, entry):
            added += 1
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_aggregate_ai_vuln_intel -v`
Expected: all 7 tests PASS (4 from Task 10 + 3 new)

- [ ] **Step 6: Commit**

```bash
git add scripts/aggregate_ai_vuln_intel.py tests/test_aggregate_ai_vuln_intel.py
git commit -m "Add MITRE ATLAS technique diff signal to AI vuln intel aggregator"
```

---

## Task 12: Aggregator — framework/vector-DB GHSA signal

**Files:**
- Modify: `scripts/aggregate_ai_vuln_intel.py` (add third signal function)
- Modify: `tests/test_aggregate_ai_vuln_intel.py` (add tests)

**Interfaces:**
- Produces: `check_framework_ghsa(advisories_by_repo: dict[str, list[dict]]) -> list[dict]` — pure function over already-fetched advisory data (each advisory dict has `ghsa_id`, `summary`, `html_url`, `published_at`); `fetch_ghsa_advisories(repo: str)` does the network call per tracked repo.

- [ ] **Step 1: Write the failing tests**

```python
# add to tests/test_aggregate_ai_vuln_intel.py

from aggregate_ai_vuln_intel import check_framework_ghsa


class TestCheckFrameworkGhsa(unittest.TestCase):
    def test_creates_one_entry_per_advisory(self):
        advisories_by_repo = {
            "langchain-ai/langchain": [
                {"ghsa_id": "GHSA-aaaa-bbbb-cccc", "summary": "SSRF in loader",
                 "html_url": "https://github.com/advisories/GHSA-aaaa-bbbb-cccc",
                 "published_at": "2026-09-01T00:00:00Z"},
            ]
        }
        entries = check_framework_ghsa(advisories_by_repo)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "framework_ghsa")
        self.assertIn("GHSA-aaaa-bbbb-cccc", entries[0]["id"])

    def test_no_advisories_produces_no_entries(self):
        self.assertEqual(check_framework_ghsa({"vllm-project/vllm": []}), [])

    def test_multiple_repos_each_contribute(self):
        advisories_by_repo = {
            "ollama/ollama": [{"ghsa_id": "GHSA-1111-2222-3333", "summary": "x",
                                "html_url": "https://x", "published_at": "2026-09-01T00:00:00Z"}],
            "huggingface/transformers": [{"ghsa_id": "GHSA-4444-5555-6666", "summary": "y",
                                           "html_url": "https://x", "published_at": "2026-09-01T00:00:00Z"}],
        }
        entries = check_framework_ghsa(advisories_by_repo)
        self.assertEqual(len(entries), 2)
```

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m unittest tests.test_aggregate_ai_vuln_intel -v`
Expected: `ImportError: cannot import name 'check_framework_ghsa'`

- [ ] **Step 3: Add the implementation**

```python
# Add near the top with the other constants:
TRACKED_REPOS = [
    "langchain-ai/langchain",
    "ggml-org/llama.cpp",
    "vllm-project/vllm",
    "ollama/ollama",
    "huggingface/transformers",
    "langchain-ai/langgraph",
    "microsoft/autogen",
    "openai/openai-python",
    "anthropics/anthropic-sdk-python",
    "chroma-core/chroma",
    "weaviate/weaviate",
    "pinecone-io/pinecone-python-client",
    "facebookresearch/faiss",
]


def fetch_ghsa_advisories(repo, github_token=None):
    """List published security advisories for one repo via GitHub's REST
    API. Public advisories are readable unauthenticated, but pass the
    Actions-provided GITHUB_TOKEN when available to avoid the 60/hr
    unauthenticated rate limit across 13 repos."""
    url = f"https://api.github.com/repos/{repo}/security-advisories"
    headers = {'User-Agent': 'FixTheVuln-AI-Vuln-Intel/1.0',
               'Accept': 'application/vnd.github+json'}
    if github_token:
        headers['Authorization'] = f'Bearer {github_token}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
        print(f"  Warning: failed to fetch advisories for {repo}: {e}")
        return []


def check_framework_ghsa(advisories_by_repo):
    """One queue entry per advisory across all tracked repos. Dedup against
    already-queued advisories happens via add_entry's id check in main(),
    same as every other signal type — no separate 'seen' file needed."""
    entries = []
    for repo, advisories in advisories_by_repo.items():
        for adv in advisories:
            entries.append({
                "id": f"ghsa-{adv['ghsa_id'].lower()}",
                "type": "framework_ghsa",
                "status": "new",
                "source_url": adv["html_url"],
                "detected_at": datetime.now(timezone.utc).isoformat(),
                "notes": f"{repo}: {adv['summary']}",
            })
    return entries
```

Wire into `main()`:

```python
    import os
    github_token = os.environ.get('GITHUB_TOKEN', '')
    advisories_by_repo = {repo: fetch_ghsa_advisories(repo, github_token) for repo in TRACKED_REPOS}
    for entry in check_framework_ghsa(advisories_by_repo):
        if add_entry(state, entry):
            added += 1
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_aggregate_ai_vuln_intel -v`
Expected: all 10 tests PASS (7 from Tasks 10-11 + 3 new)

- [ ] **Step 5: Commit**

```bash
git add scripts/aggregate_ai_vuln_intel.py tests/test_aggregate_ai_vuln_intel.py
git commit -m "Add framework/vector-DB GHSA advisory signal to AI vuln intel aggregator"
```

---

## Task 13: Chain into the Friday workflow

**Files:**
- Modify: `.github/workflows/ai-trend-roundup.yml`

**Interfaces:** none new — orchestration only.

- [ ] **Step 1: Add a step after the existing "Aggregate AI security news" step**

```yaml
      - name: Aggregate AI vulnerability intel
        run: |
          python3 scripts/aggregate_ai_vuln_intel.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- [ ] **Step 2: Update the "Check for changes" step to include the new state file**

Change:
```yaml
          if [[ -n $(git status --porcelain drafts/ data/ai-security-trends.json data/ai_news_seen.json) ]]; then
```
to:
```yaml
          if [[ -n $(git status --porcelain drafts/ data/ai-security-trends.json data/ai_news_seen.json data/ai-vuln-intel.json) ]]; then
```

- [ ] **Step 3: Update the "Commit digest" step's `git add`**

Change:
```yaml
          git add drafts/ai-security-roundup-*.md data/ai-security-trends.json data/ai_news_seen.json
```
to:
```yaml
          git add drafts/ai-security-roundup-*.md data/ai-security-trends.json data/ai_news_seen.json data/ai-vuln-intel.json
```

- [ ] **Step 4: Verify the workflow YAML is valid**

Run: `python3 -c "import yaml" 2>/dev/null && python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ai-trend-roundup.yml'))" || echo "PyYAML not installed locally — verify via 'act' or a GitHub Actions dry-run / next scheduled run instead"`

If PyYAML isn't available locally (this repo doesn't depend on it), the workflow's correctness is verified on the next scheduled run (Friday 6 AM PT) or by triggering `workflow_dispatch` manually — don't add PyYAML as a dependency just for this check.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/ai-trend-roundup.yml
git commit -m "Chain aggregate_ai_vuln_intel.py onto the Friday AI trend roundup workflow"
```

---

## Task 14: Scheduled draft → loop → publish trigger

This task configures a recurring Claude Code cloud trigger — not application code. It mirrors the existing "AppSec CVE Reviewer" trigger (daily, reads `pending_review.json` → AI review → full publish pipeline → commit) but for `ai-vuln-intel.json` entries, with the Marlowe/Sable/Griggs loop from the spec (section 5) in between drafting and the standard `content-editor`/`appsec` gate.

**Files:** none created directly by this task — it configures a scheduled trigger via the `schedule` skill/CronCreate, the same mechanism that created the existing "AppSec CVE Reviewer" trigger referenced in `CLAUDE.md`.

- [ ] **Step 1: Confirm the precedent trigger's cadence and prompt shape**

Run: `grep -A5 "AppSec CVE Reviewer" CLAUDE.md` to re-read the existing trigger's documented schedule (daily, 10 AM PDT / 9 AM PST) and pipeline steps before modeling the new one on it.

- [ ] **Step 2: Invoke the `schedule` skill to create the new trigger**

Use the `schedule` skill (which wraps `CronCreate`) to create a new weekly trigger, **Friday 7 AM PT** (one hour after `ai-trend-roundup.yml`'s 6 AM PT run, so `data/ai-vuln-intel.json` is already populated), with this routine prompt:

```
Read data/ai-vuln-intel.json in the FixTheVuln repo. For each entry with
status "new":

1. Dispatch fixthevuln-lead to draft the change:
   - owasp_top10_change: update the affected technique's entry in
     data/ai-vuln-content.json (fixthevuln-lead reads the OWASP source at
     the entry's source_url first), then run
     scripts/generate_ai_vuln_pages.py.
   - atlas_technique_change: add a new technique entry to
     data/ai-vuln-content.json (framework: "mitre-atlas") sourced from the
     entry's source_url, then run scripts/generate_ai_vuln_pages.py.
   - framework_ghsa: draft a short writeup for the next weekly roundup
     blog post citing the advisory.
   Set the entry's status to "drafted".

2. Run the claim-verification loop: claim-extractor (Marlowe) → then
   evidence-searcher (Sable) → then critic (Griggs), each reading the same
   diff. If Griggs's verdict is "block" or "approve-with-fixes", route the
   findings back to fixthevuln-lead to revise, call
   record_loop_round(state, entry_id) from scripts/lib/ai_vuln_intel_store,
   and repeat this step. Set status to "in_review" while looping.

3. If record_loop_round returns "needs_human_review" (past 3 rounds), stop
   looping for that entry, leave the draft as-is, and file a GitHub issue
   titled "AI vuln intel: <entry id> needs human review" summarizing
   Griggs's last findings. Move to the next entry.

4. Once Griggs approves clean, run the standard /pre-push-review gate
   (content-editor + appsec) on the diff. If it blocks, treat that like a
   Griggs block: revise and re-run from step 2, still counting against the
   same 3-round cap.

5. Once pre-push-review passes, commit and push (mirroring the existing
   AppSec CVE Reviewer trigger's auto-publish behavior — no separate human
   click required), and set the entry's status to "published".

Never process more than 3 loop rounds per entry per run (enforced by
record_loop_round already returning needs_human_review — trust it, don't
re-implement the cap here).
```

- [ ] **Step 3: Verify the trigger was created**

Use `CronList` (or ask the `schedule` skill to list triggers) and confirm the new trigger appears with the Friday 7 AM PT schedule.

- [ ] **Step 4: Document it in `CLAUDE.md`**

Add a row to the `GitHub Actions Workflows` table's surrounding prose, or a new subsection near "AI Security Trend Roundup" in `CLAUDE.md` (gitignored, no commit needed):

```markdown
### AI Vulnerability Intel Pipeline
Friday GitHub Action step (`ai-trend-roundup.yml`, chained after the news
aggregator) → `scripts/aggregate_ai_vuln_intel.py` writes signals to
`data/ai-vuln-intel.json`. Friday Claude Code trigger ("AI Vuln Intel
Reviewer", 7 AM PT, one hour after the Action) → drafts via
`fixthevuln-lead` → Marlowe/Sable/Griggs claim-verification loop (capped at
3 rounds, then `needs_human_review` + a GitHub issue) → standard
content-editor/appsec pre-push gate → auto-publish. See
`docs/superpowers/specs/2026-09-12-ai-vuln-intel-pipeline-design.md`.
```

---

## Plan self-review notes

- **Spec coverage:** §3 (shared state) → Task 1; §3 signal sources → Tasks 10-12; §4 (hub/page structure) → Tasks 2-4; §5 (draft/loop/publish flow) → Task 14 (trigger) + Task 1 (`record_loop_round`); §6 (agents) → Tasks 6-8; §7 (error handling) → per-source try/except in Tasks 10-12; §8 (testing) → one test file per script throughout; §9 (open questions) → resolved: hub URL is `owasp-llm-top10.html` (Task 4), ATLAS shares the same hub (Task 4's grid includes both frameworks), llms.txt/sitemap/propagate resolved in Task 5.
- **Placeholder scan:** the one intentionally-deferred item is Task 11 Step 1 (confirm MITRE ATLAS's live repo path before hardcoding) — that's a real verification command with a concrete decision point, not a TBD.
- **Type consistency:** `entry["id"]`/`entry["type"]`/`entry["status"]` shapes match across Tasks 1, 10, 11, 12. `render_technique_page(entry, hub_url, hub_name)` signature matches between Task 3's definition and Task 4's call. `data/ai-vuln-content.json`'s `techniques[].code`/`.framework` fields match how Task 11 reads `known_ids`.
