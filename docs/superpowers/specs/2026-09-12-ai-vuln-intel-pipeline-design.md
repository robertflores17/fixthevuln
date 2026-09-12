# AI Vulnerability Intelligence Pipeline — Design

Status: approved-pending-user-review
Date: 2026-09-12
Author: Claude (brainstorming session with Robert Flores)

## 1. Problem

FixTheVuln already runs a weekly AI-security *news* pipeline
(`scripts/aggregate_ai_security_news.py` → `ai-trend-roundup.yml`, Fridays) that
digests RSS/Atom signals into a blog roundup. That pipeline is out of scope here —
it works and isn't being touched.

Three real gaps exist around AI *vulnerability* content specifically:

1. **Staleness** — `owasp-llm-top10.html` is a static, hand-written page. Nothing
   detects when OWASP revises the LLM Top 10 (this happened during this design
   session: OWASP GenAI announced a 2026 revision on 2026-09-02, and the site had
   no mechanism to notice).
2. **No framework/vendor CVE tracking** — the news pipeline covers research and
   commentary (arXiv, blogs) but not security advisories for the LLM
   frameworks/vector stores FixTheVuln readers actually run.
3. **No structured technique library** — AI vulnerability content today is blog
   posts and one static Top-10 page, not a per-technique reference the way `cve/`
   gives every CVE its own page.

## 2. Goals / non-goals

**Goals:** detect + draft + verify + publish updates across all three gaps, on a
recurring schedule, reusing existing infrastructure and conventions wherever one
already fits.

**Non-goals:**
- Not touching `aggregate_ai_security_news.py` or the Friday blog roundup content
  itself — only chaining a new step onto the same workflow run.
- Not building a generic multi-project research pipeline (see below) — scoped
  to FixTheVuln only.
- Not replacing `content-editor` or `appsec` — the new agents run *before* that
  gate, not instead of it.

## 3. Architecture

One new state file, `data/ai-vuln-intel.json`, modeled on the existing
`data/pending_review.json` KEV-queue pattern. Each entry:

```json
{
  "id": "owasp-llm-2026-revision",
  "type": "owasp_top10_change | atlas_technique_change | framework_ghsa | missing_technique_page",
  "status": "new | drafted | in_review | needs_human_review | published",
  "source_url": "...",
  "detected_at": "...",
  "loop_rounds": 0,
  "notes": ""
}
```

One new script, `scripts/aggregate_ai_vuln_intel.py`, chained onto the existing
`ai-trend-roundup.yml` workflow (same Friday cadence, no new cron) as a step
after `aggregate_ai_security_news.py`. It populates `ai-vuln-intel.json` from
three signal sources:

- **OWASP Top 10 change detection** — reuses the `genai.owasp.org/feed/` RSS
  entry already fetched by the existing news script; a title match for
  "Top 10" + a version number is the signal. Does not scrape the taxonomy page.
- **MITRE ATLAS technique diff** — pulls structured YAML from
  `mitre-atlas/atlas-data` on GitHub (not the ATLAS website HTML) and diffs
  technique IDs/names against what's already published under `ai-vulnerabilities/`.
- **Framework/vector-DB GHSA advisories** — GitHub GraphQL Security Advisories
  API, authenticated with the Actions-provided `GITHUB_TOKEN` (no new secret),
  scoped to: `langchain`, `llama.cpp`, `vllm`, `ollama`, `transformers` (HF),
  `langgraph`, `autogen`, `openai-python`, `anthropic-sdk-python`, `chroma`,
  `weaviate`, `pinecone` client, `faiss`.

## 4. Page structure

`owasp-llm-top10.html` currently has all 10 items inline. To add per-technique
pages without duplicating content, it becomes a **hub page** (keeps its
intro/takeaways/quiz, drops the inline `<h2>LLM0X: ...</h2>` sections in favor
of summary + link), following the same hub-plus-subpages pattern this repo
already uses for `cve/` (index + per-CVE) and `practice-tests.html` (hub +
per-vendor). New directory `ai-vulnerabilities/` holds one page per OWASP LLM
item (`ai-vulnerabilities/llm01-prompt-injection.html`, etc.) and one per ATLAS
technique. A new `ai-vulnerabilities/index.html` or the existing
`owasp-llm-top10.html` serves as the hub — implementation plan should confirm
which, likely reusing `owasp-llm-top10.html` as the hub URL to preserve existing
SEO/backlinks.

Framework CVE writeups don't get new dedicated pages — they surface as entries
in the existing weekly news roundup blog post, same as today, just sourced
from GHSA instead of only RSS.

## 5. Draft → review-loop → publish flow

For every `status: new` entry in `ai-vuln-intel.json`:

1. `fixthevuln-lead` drafts the page (new/revised technique page, or a
   framework-CVE blurb for the roundup).
2. **Claim-verification loop** (new, scoped to this pipeline only — see §6):
   Marlowe (claim extraction) → Sable (evidence search) → Griggs (critic).
   Griggs's findings route back to `fixthevuln-lead` for revision; repeat.
3. **Loop cap: 3 rounds.** If Griggs hasn't passed clean after 3 rounds, the
   entry flips to `needs_human_review` and a GitHub issue is filed — same
   safety-net pattern as `friday-reminder.yml` / `audit-pages.yml`. No infinite
   loop, no force-publish.
4. Once Griggs passes clean, the draft goes through the **existing** mandatory
   `content-editor` + `appsec` pre-push gate, unchanged.
5. Auto-commit and push — same automation level as the existing daily
   `AppSec CVE Reviewer` trigger (which already auto-publishes once AI review
   passes, no human click required).

## 6. New agents (`FixTheVuln/.claude/agents/`)

Scoped to this pipeline's auto-drafted content only. Do not replace
`content-editor`, which still runs the standard pre-push gate on everything.

| Persona | File | Mandate |
|---|---|---|
| **Marlowe** | `claim-extractor.md` | Extracts every checkable claim from a draft (CVE ID, CVSS figure, "actively exploited" assertion, technique-to-incident attribution, framework/version reference) into a structured list. No verdicts — extraction only. |
| **Sable** | `evidence-searcher.md` | For each of Marlowe's claims, searches primary sources (NVD, CISA KEV, OWASP, MITRE ATLAS, GHSA, vendor advisories) and attaches supporting/contradicting evidence + citation. |
| **Griggs** | `critic.md` | Reviews each claim+evidence pair, flags unsupported/contradicted/overconfident claims using the same P0–P3 severity `content-editor` uses. Blocks on P0/P1. |

Tool access: Read/Grep/Glob/WebFetch for all three (research-only, no Write/Edit
— they report findings for `fixthevuln-lead` to act on, same separation as
`content-editor`/`appsec` today).

FixTheVuln's own `CLAUDE.md` Role System section gets a short addition
documenting these three, same style as the existing AppSec/Content Editor
entries.

## 7. Error handling

- Per-source try/except around every fetch (URLError/HTTPError/ParseError) —
  one bad source logs and is skipped, doesn't abort the run. Matches existing
  `aggregate_ai_security_news.py` behavior.
- All HTML-writing code paths use `lib/templates.esc()` like every other
  generator here.
- No new secrets — GHSA auth uses the Actions-provided `GITHUB_TOKEN`.

## 8. Testing

One `unittest` per script covering its riskiest logic, matching the existing
`tests/test_generate_threat_roundup.py` pattern (regression test for a specific
failure mode, not a full suite):
- OWASP version-diff comparator: must not false-positive on a reworded-but-not-
  renumbered item.
- GHSA dedup logic (mirrors `ai_news_seen.json`-style seen-tracking).

Standard `py_compile` syntax-check before commit, per the Execution Loop
convention already in `CLAUDE.md`.

## 9. Open questions for the implementation plan

- Exact hub URL (`owasp-llm-top10.html` reused vs. new `ai-vulnerabilities/index.html`).
- Whether ATLAS techniques get folded into the same hub page or a separate one.
- `generate_llms_txt.py` category updates for the new `ai-vulnerabilities/` pages.
- Sitemap/IndexNow submission for new pages (existing `propagate.py` likely reusable as-is).
