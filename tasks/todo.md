# FixTheVuln — Task Tracker

## Next Up

- [ ] **AI vuln-intel draft/publish pipeline** — `data/ai-vuln-intel.json` (fed by
  `scripts/aggregate_ai_vuln_intel.py`: OWASP Top 10 change, MITRE ATLAS diff,
  framework GHSA advisories, AI Incident Database) is currently a manual-review
  queue only — nothing drafts, verifies, or publishes from it yet. Spec + plan
  already written: `docs/superpowers/specs/2026-09-12-ai-vuln-intel-pipeline-design.md`
  and matching plan in `docs/superpowers/plans/`. Needs: `fixthevuln-lead` drafting
  step, new Marlowe/Sable/Griggs claim-verification agents (§5-6 of spec), then
  the existing `content-editor`/`appsec` gate. Deliberately deferred — decided
  2026-09-14 to leave the queue manual-only for now.

## Current Sprint — AI Security Content (from [un]prompted 2026)

Source: theweatherreport.ai/posts/unprompted-2026-top-insights-day-one

### Blog Posts
- [x] **"How AI Is Changing Vulnerability Discovery"** — `blog/ai-vulnerability-discovery-2026.html` (2026-03-16)
- [x] **"Zero-Click RCE in AI IDEs"** — `blog/ai-ide-security-vulnerabilities-2026.html` (2026-03-16)
- [x] **"AI Notetakers — Security Risk"** — `blog/ai-notetaker-security-risk.html` (2026-03-16)
- [x] **"AI Incident Response Revolution"** — `blog/ai-incident-response-revolution.html` (2026-03-16)

### Guide Updates
- [x] **Updated `prompt-injection.html`** — Added AI IDE & MCP Attack Surface section (2026-03-16)
- [x] **Updated `owasp-llm-top10.html`** — Added real-world examples to LLM03 + LLM06 (2026-03-16)
- [x] **New guide: "AI Security Careers"** — `ai-security-careers.html`, 5 roles with skills/certs/salary (2026-03-16)

### LinkedIn Posts (FixTheVuln TTHS)
- [x] **"AI finds vulnerabilities for 61 cents each"** — Post 13 in captions (2026-03-16)
- [x] **"37 zero-click vulnerabilities in AI coding tools"** — Post 14 in captions (2026-03-16)
- [x] **"Your AI notetaker is a security risk"** — Post 15 in captions (2026-03-16)
- [x] **"AI incident response: 12x more findings"** — Post 16 in captions (2026-03-16)

## Backlog

### SEO & Distribution (from 2026-03-16 growth plan)
- [x] Sitemap expanded to 454 URLs (4 new blog posts added)
- [x] IndexNow propagation (450 URLs submitted)
- [x] Quiz analytics endpoint + client wiring deployed
- [x] 12 LinkedIn hero PNGs + captions created
- [x] Submit sitemap in Google Search Console — already submitted, GSC "Verify fix" triggered on 331 pages (2026-03-16)
- [x] Start LinkedIn cadence — first post published (2026-03-16)
- [ ] Monitor GSC validation on 331 "discovered not indexed" pages (check in 1-2 weeks)

## Completed

- [x] Sitemap: 381 → 450 URLs (2026-03-16)
- [x] Quiz analytics: POST /quiz/submit endpoint + sendBeacon client (2026-03-16)
- [x] generate_sitemap.py script (2026-03-16)
- [x] 12 LinkedIn hero marketing PNGs + captions (2026-03-16)
- [x] Merged 4 planner skills from Etsy-Claude (2026-03-16)
- [x] Created deploy + linkedin-content skills (2026-03-16)

## Review Notes

_Add post-implementation review notes here._

---

## 2026-09-17 — OWASP LLM Top 10 (2026) refresh + Agentic Skills Top 10 (AST10)

Verified against 3 sources (genai.owasp.org press release 2026-09-01, Superblocks, Check Point).
Note: genai.owasp.org/llm-top-10/ still serves the 2025 edition — the 2026 doc lives at
/resource/owasp-genai-llm-top-10-2026/. Confirm before publishing.

### 2025 -> 2026 mapping (8 of 10 move, 1 renamed)

| 2026 | Title | was 2025 | slug change |
|---|---|---|---|
| LLM01 | Prompt Injection | LLM01 | none |
| LLM02 | Sensitive Information Disclosure | LLM02 | none |
| LLM03 | Excessive Agency | LLM06 | yes |
| LLM04 | Supply Chain | LLM03 (Supply Chain Vulnerabilities) | yes + retitle |
| LLM05 | Data and Model Poisoning | LLM04 | yes |
| LLM06 | Unbounded Consumption | LLM10 | yes |
| LLM07 | Misinformation | LLM09 | yes |
| LLM08 | Hidden Context Exposure | LLM07 (System Prompt Leakage) | yes + rewrite (broadened: RAG content, memory, tool schemas, app state) |
| LLM09 | Vector and Embedding Weaknesses | LLM08 | yes |
| LLM10 | Improper Output Handling | LLM05 | yes |

### Phase 1 — LLM Top 10 2026 refresh

- [x] Rewrite `data/ai-vuln-content.json`: renumber codes/ids, retitle LLM04, rewrite LLM08 entry for broadened scope, re-rank risk_level where the edition moved it
- [x] Update `scripts/generate_guides.py` owasp-llm-top10 config: description, FAQ, key takeaways, intro, and all 10 `<h2>LLMxx:</h2>` sections -> 2026 numbering + a "what changed from 2025" block
- [x] Regenerate in order: `generate_guides.py` THEN `generate_ai_vuln_pages.py` (the second re-injects the AI-VULN-GRID into the hub the first overwrites)
- [x] 8 redirect stubs at the old `ai-vulnerabilities/<old-slug>.html` paths (meta refresh + rel=canonical to new URL). Excluded from sitemap. Upgrade path: Cloudflare Bulk Redirects for real 301s.
- [x] Update `ai-security.html` technique-library list (10 refs)
- [x] Update `ai-agent-security.html`, `ai-agent-security-threats.html`, `prompt-injection.html`, `model-poisoning.html` LLM-code cross-refs
- [x] Verify: `python3 -m unittest tests.test_ai_vuln_pages`

### Phase 2 — Quiz bank correction (currently on the 2023 edition, 2 versions stale)

- [x] `data/ai-security-questions.json` (21 refs) and `data/secai-questions.json` (22 refs): "LLM02: Insecure Output Handling", "LLM09: Overreliance", "LLM03: Training Data Poisoning", "LLM08/LLM06: Excessive Agency", "LLM05: Supply Chain Vulnerabilities" -> 2026 codes/titles. Fix distractors that only work under the old numbering.
- [x] Verify: JSON valid, answer indices still point at the right option after any reordering

### Phase 3 — AST10 (hub + 10 subpages)

- [x] Generalize `generate_ai_vuln_pages.py`: FRAMEWORKS dict keyed on the existing `framework` field in each entry -> (hub_url, hub_name). Group techniques by framework, render each framework's own grid. ~20 lines; reuses templates, tests, sitemap, breadcrumbs unchanged.
- [x] Add 10 AST entries to `data/ai-vuln-content.json` (framework `owasp-agentic-skills-top10`, ids `ast01-malicious-skills` ... `ast10-cross-platform-reuse`), same output dir
- [x] New hub `agentic-skills-top-10.html` via a PAGE_CONFIGS entry in `generate_guides.py` (+ AI-VULN-GRID markers)
- [x] Link from `ai-security.html`, `ai-agent-security-threats.html` ("The Agent Skill Supply Chain" section maps to AST01/02/03/05/08), `guides.html`, `tools.html` if it fits
- [x] Add AST pages to `GUIDE_PAGES` in `generate_llms_txt.py`

### Phase 4 — Propagation + gates

- [x] `python scripts/generate_llms_txt.py`, `python scripts/update_sitemap.py`
- [x] `/self-qa` full pass
- [x] `/pre-push-review` (security-review + appsec + content-editor — content-editor is blocking here, every factual claim is new)
- [x] `scripts/propagate.py` IndexNow for new + changed URLs

### Not doing (say so if wanted)

- No 2025 archive pages — refresh in place, stubs redirect.
- Cloudflare Bulk Redirects left as a manual follow-up; static stubs ship today.

### Review — completed 2026-09-17

**Deviations from plan:**
- Did NOT regenerate the hub via `generate_guides.py`. Running it regressed 11 live pages by -634 lines (see `lessons.md`). Hub was edited surgically instead; the generator config was still corrected so a future run is not wrong, and its 6-month-old `_esc` crash bug was fixed.
- Did NOT re-rank `risk_level` labels to follow OWASP position. Those labels describe severity of the vulnerability class, not rank order; Improper Output Handling still causes RCE at #10. Position alone conveys the OWASP ranking.
- Quiz banks were on the **2023** edition, not 2025 as first assessed. 14 questions corrected across both files.

**Unplanned fixes found en route:**
- `scripts/generate_guides.py`: `_esc` undefined since 2026-03-06, crashed on import. Fixed.
- `scripts/generate_llms_txt.py`: `category_order` silently drops any category missing from it. "AI Security Guides" was never listed, so 9 AI pages had been absent from `llms.txt` and `llms-full.txt` entirely. Fixed, plus a guard that now raises instead of dropping.
- `scripts/generate_sitemap.py`: added generic meta-refresh detection so redirect stubs never enter the sitemap.

**Verification:** 4/4 unit tests pass; 3 JSON files valid; 4 scripts compile; 457 internal links across 35 touched files resolve; `audit_pages.py` reports 0 broken links and 0 errors; sitemap 692 -> 703 URLs with all 8 stubs excluded.

**Still open:**
- Cloudflare Bulk Redirects for real 301s on the 8 renumbered URLs (static stubs ship today, dashboard task for Robert).
- `scripts/migrate_owasp_llm_content.py` is a spent one-time migration whose slug map now points at redirect stubs. Harmless, referenced by nothing, left in place — delete when convenient.
- `generate_guides.py` remains unsafe to run for the other 10 pages it owns (it reverts injector output). Now carries a loud docstring warning and chains the grid regeneration, but the page-drift problem itself is untouched. Not in scope here.
- **`js/quiz-engine.js:138` only renders a "Learn more" link when `q.link` matches `^https?://`.** Every `link` value in both quiz banks is relative, so no question has ever rendered one. Pre-existing, not a regression (the old values were equally relative), but the improved link targets in this change set have no user-visible effect until the engine accepts relative paths. Deliberately not changed here: relaxing that regex would surface links on all 300 questions at once, which is a product decision, not a fix.

### Content Editor BLOCK — resolved 2026-09-17

Gate returned `block` with 5 P0 and 6 P1 on the AST10 half. Root cause: sourced the framework from a
LinkedIn post, a personal fork, and a blog instead of `OWASP/www-project-agentic-skills-top-10`.
Verified every blocking claim myself against the OWASP org repo and the NVD API before rewriting.

Fixed (all 17 findings):
- P0 AST05 was the wrong risk. "Unsafe Deserialization" does not exist in AST10; AST05 is **Untrusted
  External Instructions**. Page rewritten from `ast05.md`; the deserialization material moved into
  AST04 where OWASP maps it (CWE-502, ASVS V5.5). Old page deleted rather than redirected: it was
  never deployed, so there are no inbound links to carry.
- P0 Dropped "published August 17, 2026" and "standard" everywhere. AST10 is an OWASP **Incubator**
  project, "New Project Proposal — active development", v1 whitepaper in public review, v1.0 Q4 2026.
- P0 13.4% restated: critical issues in 13.4% of 3,984 scanned skills (534), most missed by pattern
  matching. It was never an "escape rate".
- P0 ClawJacked/CVE-2026-28363 mapping removed (NVD: that ID is a `sort` allowlist bypass, unrelated).
- P0 All three CVSS scores replaced with NVD primary, dual-cited against the CNA: 8.8 (not 8.7),
  7.5 (not 5.3 — Medium vs High, the worst of the three), and the third dropped with its CVE.
- P1 Severity disclaimer deleted; all ten severities now match the project's published ratings
  (AST06 Critical→High, AST07 High→Medium).
- P1 OpenClaw CVE counts date-qualified to SecurityScorecard's March 2026 analysis.
- P1 LLM 2026 date → "published August 2026 and announced September 1, 2026" (true against the
  resource page, the PDF cover, and the press release, which disagree with each other).
- P1 LLM04 movement cell → "Down 1". "Supply Chain" was already the 2025 title; "Supply Chain
  Vulnerabilities" was 2023.
- P1 Cisco 34% re-attributed through the AST10 project (the Cisco report is registration-gated).
- P1/P2 Cut the PraisonAI citation (appears in no AST10 source — likely fabricated upstream or by me).
- P2 toxicskills-goof re-attributed: Snyk's suite, SpecWeave's scanner.
- P2 Framework mapping corrected: AISVS v1.0 + MAESTRO direct, NIST AI RMF indirect, MCP dropped.
- P2 ClawHavoc split: campaign began Jan 27 2026 (341 skills in 3 days); 1,184 across 12 accounts is
  Antiy CERT's February tally.
- P3 Store/CyberFolio footer line added to the new hub.
- P3 "tool poisoning" re-mapped off AST04 in ai-agent-security-threats.html.

Content Editor verified clean and unchanged: all 14 quiz corrections, the entire LLM 2026 renumbering,
the redirect stubs, sitemap/llms hygiene, and the LLM08 Hidden Context Exposure rewrite.

Open question it raised: if CompTIA SecAI+ objectives still reference the 2025 LLM edition, the
`secai-questions.json` items may now diverge from the exam blueprint. Worth checking against CompTIA's
current objectives PDF before the next quiz regeneration.
