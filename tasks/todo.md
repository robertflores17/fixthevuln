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

---

## Daily AI IDE / MCP vulnerability tracker (2026-09-19)

**Goal:** `blog/ai-ide-security-vulnerabilities-2026.html` currently reads as 6 months stale
(Published: March 16, 2026, no later signal). Give it a live tracker section refreshed daily,
without churning the narrative or faking freshness on days with no new disclosures.

**Shape:** narrative stays frozen. One marker-delimited tracker block appended to the post.
"Last updated" bumps only when the rendered block actually changes.

### Phase 1 — collector
- [x] `scripts/aggregate_ai_ide_vulns.py` → `data/ai-ide-vulns.json`
  - [x] NVD `keywordSearch` + **`pubStartDate`** (not lastMod: NVD re-enriches ancient CVEs,
        so a lastMod window returned 2002-era ncurses bugs for "cursor")
        (Cursor, Copilot, Windsurf, Continue, Zed, Cline, Aider, Roo); reuse the
        `NVD_API_KEY` header + timeout pattern from `fetch_kev.py`
  - [x] GHSA: import `fetch_ghsa_advisories` from `aggregate_ai_vuln_intel.py`,
        new repo list scoped to MCP servers + IDE extension ecosystem
  - [x] KEV: filter already-on-disk `data/kev-data.json` for AI tooling vendors (cheap, low yield)
  - [x] Dedup via a plain id set, not `lib/ai_vuln_intel_store.add_entry` (that store is bound
        to ai-vuln-intel.json and stamps loop_rounds/notes for a review loop this doesn't run)
  - [x] Verify: `py_compile` + one live run, confirm non-empty and no dupes on second run

**Phase 1 result (done 2026-09-19):** 88 entries collected; 58 MCP, 8 Claude Code, 7 Cursor,
5 Aider, 5 Zed, 3 Cline, 1 Windsurf, 1 GitHub Copilot. Re-run added 0 (dedup verified).
`tests/test_aggregate_ai_ide_vulns.py`, 19 tests; full suite 67 tests green.

Four bugs found and fixed by running against live data, none visible from reading the code:
1. **NVD_API_KEY is rejected** and NVD answers a bad key with **404, not 401** — every query
   silently returned nothing. Now reuses `fetch_kev._validate_nvd_key()` and omits the header
   when the key fails. See "Open item" below.
2. `lastModStartDate` surfaced pre-2025 noise; `pubStartDate` collapsed "zed" from 28 hits to 6.
3. Matching a product name anywhere in the text filed Semantic MediaWiki, node-tar, Ruby JSON
   and async-tar under "Cursor" (database cursors). Ambiguous names now count only in the
   subject window; unambiguous ones still match anywhere.
4. `roo\s?code` could not match "Roo-Code", so Roo Code and Kilo Code would never have matched
   despite Roo-Code carrying 11 advisories. Separator class now allows a hyphen.

Also: `sourcegraph/cody` 404s (repo moved) and was dropped; the other 9 GHSA repos are live with
42 advisories between them. GHSA's 3 relevant hits were all already in NVD — kept anyway because
GHSA publishes before NVD indexes.

### Phase 2 — renderer
- [x] `scripts/generate_ai_ide_tracker.py`
  - [x] Insert `<!-- AI-IDE-TRACKER-START/END -->` markers into the post
  - [x] Regex marker replace (same pattern as `generate_ai_vuln_pages.replace_grid_section`)
  - [x] All feed-sourced text through `lib.templates.esc` — NVD/GHSA descriptions are
        untrusted external input written straight into HTML
  - [x] No-op + exit 0 when rendered block is byte-identical to what's on disk
  - [x] Bump `Last updated: <Month D, YYYY>` in static HTML only on change
        (not in `<script>` — invisible to `audit_pages.py`)
  - [x] Add `dateModified` to the post's JSON-LD schema
  - [x] Verify: `tests/test_generate_ai_ide_tracker.py` — marker replace, XSS escape on
        hostile feed text, no-op on unchanged data, date bump only on change

### Phase 3 — schedule
- [x] `.github/workflows/ai-ide-tracker.yml`, daily, collector → renderer → commit if changed
- [x] Commit with **no** `[skip ci]` — corrected during build. `propagate-index.yml` triggers on
      pushes touching `**.html`, so `[skip ci]` would have silently killed IndexNow submission
      on exactly the days the page changed. Verified `auto-publish-cve.yml` only watches
      `data/pending_review.json`, which this job never writes.
- [x] Added to `notify-on-failure.yml` watch list
- [ ] Verify: `workflow_dispatch` manual run, check `gh run list` (needs push first)

### Phase 4 — Claude-reviewed digest (optional, ships after 1-3)
- [ ] Claude Code scheduled trigger (subscription, no API cost) mirroring `AppSec CVE Reviewer`:
      reads new raw items, judges AI-IDE relevance, writes summary prose into the JSON
- [x] Phases 1-3 work standalone with raw NVD/GHSA descriptions if this is deferred

**Phase 2-3 result (done 2026-09-19):** tracker renders 12 of 88 rows; second run is a clean
no-op ("page not touched"), so the date only moves when data does. `tests/test_generate_ai_ide_tracker.py`,
23 tests. Two caption bugs caught before shipping: it named only the sources present in the data
(GHSA vanishes whenever NVD publishes the same CVE first, which is most days), and it claimed a
fixed "last 120 days" window that would go false as entries accumulate past it. Now uses a fixed
source sentence and states the earliest date actually recorded.

**Phase 4 (partial):** the renderer already honours a review pass — `review_summary` overrides the
raw feed text and `status: "excluded"` drops a row from both the table and the count, with model
output still escaped. So the review layer is a JSON edit, no renderer change needed. The scheduled
Claude trigger itself is NOT created; it is recurring and billable, so it needs Robert's sign-off.
Draft trigger prompt, to run daily after the 20:00 UTC tracker job:

> Read `data/ai-ide-vulns.json`. For each entry with `status: "new"`: decide whether it is really an
> AI IDE or MCP component (not a generic library that happens to mention one). If it is not, set
> `status: "excluded"`. If it is, set `status: "reviewed"` and write a one-sentence `review_summary`
> in FixTheVuln's voice, following the anti-AI-tell rules (no em-dashes, no banned vocabulary, name
> the affected version and the impact). Never edit any other field. Then run
> `python3 scripts/generate_ai_ide_tracker.py`, and commit only if it reports a change.

### Gates
- [x] `/self-qa` full pass
- [x] `appsec` subagent — **approve-with-fixes, no P0/P1**. Verified clean: all five rendered
      fields escaped, attribute breakout impossible (esc covers both quote types), ReDoS linear
      (700 KB adversarial inputs, <=0.021s), feed text cannot forge the markers or a
      `dateModified` target, all three `re.sub` calls use lambdas so `\g<0>` in feed data is
      inert, secrets travel as headers and never reach logs/JSON/HTML, commit path list is
      hardcoded. Four findings taken:
  - [x] P2 `href` had no scheme allowlist — a `javascript:` URL from GHSA's `html_url` or from
        the review pass would render as a live one-click XSS link. Now `safe_url()` allowlists
        http(s) at render time (the chokepoint all three sources funnel through), and a rejected
        URL still shows the CVE id as plain text. Regression tests added.
  - [x] P3 no type validation on JSON read from disk — a number where a string belongs crashed
        `esc()` mid-render. Now coerced via `field()`.
  - [x] P3 write-scoped `GITHUB_TOKEN` was passed to the GHSA call; urllib forwards headers
        across cross-host redirects. These are public advisories, so the token is simply no
        longer passed or set in the workflow. Left `aggregate_ai_vuln_intel.py` untouched.
  - [x] P3 `git pull --rebase` could not find a merge base in a depth-1 clone; `fetch-depth: 0`
        added to checkout.
  - [ ] P3 deferred: no CSP on the page (pre-existing, site-wide). Would have made the P2 inert.
        Not this diff's scope.
  - [x] P3 entry retention capped at 500 (newest first), well outside the 120-day collection
        window so a pruned entry can never be re-collected. The file commits daily.
- [x] `content-editor` subagent (round 1) — **blocked on one P0**, all findings addressed:
  - [x] **P0** `_cvss_from_metrics` took the first metric regardless of `type`, so a CNA's
        Secondary score beat NVD's Primary. Real case: CVE-2026-13323 shipped as "Medium 4.1"
        (Eclipse Secondary) when NVD's Primary is **8.7 High**. Verified against the NVD API
        before fixing. Now prefers `type == 'Primary'` within each version tier; data
        re-collected from scratch.
  - [x] P1 vendor misattribution (6 of 30 non-MCP rows wrong: an Open VSX marketplace bug filed
        under "Windsurf", a 10.0 on third-party "Ruflo" filed under "Claude Code"). Root cause:
        a name reached through a "for X" clause was treated as the affected product. New
        `affected_product()` extracts the advisory's grammatical subject; column renamed to
        "Affected product"; fills 79/88 and leaves 9 blank rather than guess.
  - [x] P1 "recorded since" claimed a four-month observation history that did not exist (first
        collection ran today). Now "published since", formatted `Month D, YYYY`.
  - [x] P2 "GitHub Security Advisories" read as the whole database; it is 9 hand-listed repos.
        Scope now named, count derived from `len(GHSA_REPOS)`.
  - [x] P2 37-vs-88 contradiction: caption now states the MCP share, computed not hardcoded.
  - [x] P2 timestamp scoped to "Last updated: <date> (disclosure table)" — keeps the audit's
        `Last updated` regex match while saying what actually changed.
  - [x] P2 GHSA severity said "Moderate" where CVSS says "Medium"; now derived from the score.
  - [x] P3 ISO date in prose, define-by-negation phrasing, CVSS provenance caveat, column name.
  - [ ] Deferred: `review_vendor` override. `affected_product()` made it unnecessary for now;
        revisit when the review pass lands.

### Phase 5 — related research section (added 2026-09-19 at Robert's request)

Robert asked to track Ron F. del Rosario's research as a tracker source. Google Scholar was
rejected as a source: no public API, actively blocks automated access, and a paper has no CVE id
or CVSS score, which is three of the table's five columns. Routed through arXiv instead.

- [x] `fetch_arxiv_author()` / `parse_arxiv_atom()` — `au:"Del Rosario" AND cat:cs.CR`, author
      re-verified locally against each entry's author list because arXiv's `au:` match is fuzzy
- [x] `render_research()` into a second marker pair, as its own section, not rows in the CVE table
- [x] Attribution framing states the existing CyberMoE relationship rather than implying endorsement
- [x] Hardening: https (arXiv serves it natively), 1 MB response cap, doctype refused.
      Verified empirically on this interpreter that ElementTree **blocks** external entities but
      **expands** internal ones, so a DTD is the live vector, not XXE.
- [x] 135 tests green
- [x] `appsec` re-review — its one blocking P1 (`http://` arXiv endpoint) was already fixed
      while the review was running; confirmed https at the file. It verified clean: `safe_url`
      fails closed on uppercase/whitespace-prefixed schemes, the MAX_STORED cap sorts before
      truncating, no token reaches the GHSA call, no secret leakage path, the two marker pairs
      cannot nest or clobber, and an empty arXiv result correctly keeps the last known-good list.
      New findings applied:
  - [x] **P2 author filter could not tell two people apart.** `surname in author` would let
        anyone publishing in cs.CR under "Del Rosario" onto a page that vouches for him by name,
        with an attacker-chosen title, abstract and outbound link. Now matches full-name variants
        (`ron f. del rosario` / `ronald f. del rosario`); all 6 real papers still pass and a
        "Maria Del Rosario" fixture is rejected. Test added.
  - [x] P3 `long_date()` returned its input unchanged on TypeError, propagating a non-string into
        `esc()` — the same class of bug `field()` was added to prevent, on the one path that
        bypassed it.
  - [x] P3 a rejected paper URL still emitted `href=""`; now drops the anchor like the table path.
  - [x] P3 `except` tuples missed `ConnectionResetError` / `IncompleteRead`, raised during
        `read()` and not `URLError` subclasses, so a mid-transfer reset crashed the job.
  - [x] P3 `sub()` without `count=1`; P3 comment corrected re: withdrawn papers; expat-version
        caveat recorded at the parse site.
- [x] `content-editor` re-review — **approve-with-fixes, no P0**. It re-verified the P0 fix live
      against NVD (CVE-2026-13323 now High 8.7), confirmed all six vendor misattributions
      corrected, and verified all five rendered papers against the arXiv API: titles, IDs
      (including v-suffixes), dates, full author lists, author order and every "and N others"
      count match exactly. Findings applied:
  - [x] **P1 overclaim, my error.** "The papers below are the research literature behind this
        class of attack" was false: the list is filtered by author, not topic, and two of the
        five papers (COALESCE, MAIF) are not about MCP or IDE attacks at all. Rewritten to say
        they sit adjacent to the attack class rather than surveying it.
  - [x] P2 three product-extraction defects: `"Spring AI. Prior to"` (captured across a sentence
        break; the product is mcp-security, now blank), `"IBM Langflow OSS 1.0.0"` (advisory
        covers 1.0.0 **through 1.10.3**, so naming one version is a patching-decision error),
        and `"WebSocket endpoint of gpt-researcher"` (component, not product). All three pinned
        by tests. Coverage is now 78/88, one lower and correct.
  - [x] P2 caption's "rather than the IDE vendors named above" implied the other 31 rows are IDE
        bugs, derived from the same `vendor_of()` heuristic pulled from the table for being
        unreliable. Seven third-party tools sat in that complement. Complement dropped.
  - [x] P2 attribution: added the CyberMoE repo link (the blog was the only one of four
        attribution sites without it), the OWASP contributors link as a source for the
        affiliation claim (verified independently), and "He has no involvement with this site
        beyond that." Verb corrected: `analytics.html` says the quiz feedback system was
        "inspired by" CyberMoE, not "adapted from".
  - [x] P3 `stamp_dates` claimed "(disclosure table)" even on a research-only refresh; the label
        is now derived from which block actually changed.
  - [x] P3 two docstrings had gone stale and understated the guards that exist.
- [x] 145 tests green; idempotent re-run; HTML structure, JSON-LD, JSON and em-dash checks clean

### Cross-file findings

1. **[DONE 2026-09-19] `scripts/fetch_kev.py` Secondary-over-Primary CVSS defect fixed.** Robert
   approved fixing it with the tracker work. Added `_best_score()` preferring `type == 'Primary'`
   and routed all three call sites (v3.1/v3.0, v2, v4.0) through it. Version ordering deliberately
   left unchanged; only the choice within a version list moved. Verified live through the real
   function: CVE-2026-13323 now returns 8.7 (was 4.1), CVE-2021-44228 still 10.0 (no regression).
   `tests/test_fetch_kev_cvss.py`, 7 tests. NOT done: the sweep of `data/kev-data.json` against
   NVD primaries to correct already-published CVE pages. Robert chose fix-only, no sweep.
   Original finding text follows.

   **`scripts/fetch_kev.py:96-102` carried the same Secondary-over-Primary CVSS defect** that was
   the P0 here. It takes `metric_list[0]` with no `type == 'Primary'` preference, and it sets the
   CVSS score on **every published CVE page on the site**. content-editor sampled CVE-2026-58704,
   CVE-2026-42018 and CVE-2026-67277 against NVD and found no divergence today, but CVE-2026-13323
   proves NVD does not order these, so that is luck rather than correctness. Same one-line sort key
   as the fix in `_cvss_from_metrics`. Also warrants a sweep of `data/kev-data.json` against NVD
   primaries. Left alone because it is a live daily pipeline outside this change's scope.
2. `scripts/aggregate_ai_security_news.py:57` fetches `http://export.arxiv.org/rss/cs.CR` in plain
   text. One character.
3. `scripts/entity_extractor.py:9-10` names the author and MIT licence but carries no
   `Copyright (c)` line; MIT section 1 asks for the copyright notice specifically.

### Open items for Robert

- **`NVD_API_KEY` is rejected by NVD** for every endpoint, not just keyword search. NVD answers a
  bad key with 404, not 401. `fetch_kev.py` already degrades to the 6s anonymous rate limit, so
  nothing is broken, but the daily KEV enrichment has been running 10x slower than it should. The
  key needs reissuing (NVD requires an email activation click that is easy to miss). I tested the
  local env var; I cannot read the GitHub secret, so confirm they are the same value.
- **`scripts/aggregate_ai_security_news.py:57` uses `http://export.arxiv.org/rss/cs.CR`** — same
  plaintext-fetch weakness appsec flagged on the tracker, in the Friday roundup pipeline. One
  character fixes it. Left alone deliberately: different pipeline, outside this change's scope.
- **No CSP on the site.** Would have made the `javascript:`-href finding inert rather than merely
  blocked. Pre-existing and site-wide; its own project.
- **95 stale pages** in `audit_pages.py`, all pre-existing and unrelated to this work.
- **Phase 4 scheduled Claude trigger not created** — recurring and billable, needs your sign-off.
  Draft prompt is above.
- [ ] `/pre-push-review`, blocks on any P0/P1

### Notes / decisions
- H1 "37 Vulnerabilities" stays frozen — it is the historical [un]prompted 2026 research count.
  A headline figure that drifts daily reads as unreliable. Live count lives in the tracker block.
- Daily *run*, conditional *publish*. Real AI-IDE disclosures land ~weekly; a daily date bump with
  no new substance is freshness spam and Google discounts it.
- No new pages → no `llms.txt` / `sitemap.xml` regeneration needed.
- No CSS/JS touched → no cache-bust bump needed.
- Blog cross-link block is `inject_blog_links.py`-managed — do not hand-edit.


---

## RESUME POINT (session paused 2026-09-19)

Nothing is committed. Working tree holds all of it. 152 tests pass.

**State:** phases 1-3 complete and gated; phase 5 (research section) complete and gated;
`fetch_kev.py` P0-class fix complete. Pipeline is idempotent: a re-run with no new data prints
"page not touched" and writes nothing.

**Next step Robert asked for:** he chose "show me the diff first", so the diff was printed for
review. Nothing was committed or pushed pending his read.

**Remaining work, in order:**
1. Robert reviews the diff.
2. Run `/pre-push-review` (mandatory gate: security-review + appsec + content-editor on the full
   diff, blocks on P0/P1). Not yet run on the combined final state.
3. Commit. Suggested split: (a) the AI IDE tracker pipeline, (b) the `fetch_kev.py` CVSS fix as
   its own commit so it can be reverted independently.
4. After push, verify the workflow with a manual `workflow_dispatch` run and `gh run list`.
5. Phase 4 scheduled Claude trigger: still NOT created. Recurring and billable, needs sign-off.
   Draft prompt is in the Phase 4 section above. Phases 1-3 work standalone without it.

**Still open, not started:**
- `scripts/aggregate_ai_security_news.py:57` plaintext `http://` arXiv fetch (one character).
- `scripts/entity_extractor.py:9-10` missing MIT `Copyright (c)` line.
- `NVD_API_KEY` is rejected by NVD; reissue and confirm the GitHub secret matches the local value.
- Sweep of `data/kev-data.json` against NVD primary scores (Robert declined for now).
- 95 pre-existing stale pages; no CSP site-wide.

## Pre-push review — 2026-09-19

Three reviewers run on the combined working tree: native `security-review`, `appsec`, `content-editor`.

| Reviewer | Verdict | Findings |
|---|---|---|
| security-review | no findings | traced untrusted feed text into published HTML; executed renderer against hostile payloads |
| appsec | **block** | 1 P0 (ReDoS), 3 P3 |
| content-editor | approve-with-fixes | 2 P1, 1 P2, 6 P3 |

### Fixed this pass (all independently verified before accepting)

- **P0 ReDoS** `aggregate_ai_ide_vulns.py` `_SUBJ`. `-` sat in both `_NAME`'s body
  class and the separator class, so a hyphen run had O(n^6) partitions.
  Reproduced: 144-char chain 0.529s, ~1.75x per 4 tokens, ~300 bytes would hang
  the daily job past the 6h Actions ceiling. Separator narrowed to a space
  (`_NAME` already carries `-`, so hyphenated npm names still match as one
  token) plus a 400-char input bound. After: 0.0000s at 10KB input, and
  **0 of 88 stored product extractions changed**. Pinned by
  `TestAffectedProductRuntime`.
- **P1 CVSS provenance.** Caption said "taking the rating NVD marks primary over
  a secondary one", which reads as NVD-adjudicated. Verified against the NVD API:
  11 of 12 displayed CVEs have no Primary at all (`vulnStatus: Received`, only
  the GitHub CNA's Secondary); CVE-2026-93982's Primary is VulnCheck's, not
  nvd@nist.gov. Caption now discloses the CNA assessment. No displayed number
  was ever wrong.
- **P1 KEV date.** `collect_kev` wrote CISA `dateAdded` into `published`.
  Verified on CVE-2026-59822: recorded 2026-09-02, NVD published 2026-07-08, an
  8-week error under a "Published" header. `kev-data.json` has no publication
  date, so `published` is now blank and the catalog date is kept as `kev_added`.
  Blank sorts last, which is right for an unknown disclosure date. The one
  stored entry was corrected in place (merge is additive by id).
- **P2 attribution.** "research by Ron F. del Rosario" over papers where he is
  5th of 6 and 4th of 5 author. Now "co-authored by".
- **P3** "He has no involvement with this site beyond that." implied the credits
  were involvement by him. Now "He is not involved with this site."
- **P3** research section had no truncation disclosure (table had one). Added.
- **P3** a short arXiv response replaced a good list wholesale. Now treated as a
  failed fetch unless the new list is at least as long.

### Open follow-ups (none blocking)

- [ ] `aggregate_ai_ide_vulns.py` DOCTYPE guard only scans `body[:2048]`; a
      DOCTYPE is legal anywhere in the prolog. Needs upstream TLS control to hit
      and libexpat caps the damage. Fix: `defusedxml`, or scan the whole prolog.
- [ ] `resp.read()` on the NVD response is unbounded (the arXiv path caps
      correctly); arXiv `title` is the one field that skips `_trim()`.
- [ ] `severity_label()` applies CVSS v3.1 bands to a v2 fallback score. v2 has
      no Critical band. No current row affected (all v3.1).
- [ ] Aggregator tries v3.1, v3.0, v4.0, v2; `fetch_kev.fetch_cvss_from_nvd`
      tries v3.1, v3.0, v2, v4.0. Same CVE could show two scores site-wide.
- [ ] Table cells render bare ISO dates while the caption uses house-style long
      dates, contradicting `long_date`'s own docstring rationale.
- [ ] GHSA has contributed 0 of 88 rows (NVD dedup wins). Deliberate, documented
      at `generate_ai_ide_tracker.py`. Do not "fix" the caption the wrong way.
- [ ] GHSA runs unauthenticated on purpose (urllib replays headers across
      redirects, and Actions' `GITHUB_TOKEN` is write-scoped). 60 req/hr per IP
      and runners share IPs, so a 403 is possible. Degrades to "no GHSA rows".
- [ ] Site ships no CSP, so escaping is the only XSS control on this page.
      Pre-existing, out of scope here.
- [x] **`NVD_API_KEY` added as a repo secret 2026-09-19 16:43Z and verified
      working.** It had never existed, so `fetch-vulnerabilities.yml` had been
      running anonymous too. Confirmed authenticating rather than silently
      falling back: collect went 60s -> 9s (0.6s pacing vs 6.0s) with zero NVD
      warnings. Duration is the only tell available, because NVD answers a
      rejected key with 404 and `_validate_nvd_key()` falls back to anonymous,
      so a bad key and a good one produce the same job conclusion. Stripe
      secrets are correctly absent: those live in the Worker via wrangler.
- [ ] `SKILLS.md` is untracked and has never been committed, though `CLAUDE.md`
      references it. Not part of this change set.

## Plan: scale the AI IDE tracker section (2026-09-19)

Decided with Robert: full archive moves to its own page, the blog post keeps a
short teaser, and the summary column gets shortened. Not started.

**Why:** 12 of 88 shown, 76 already invisible, `MAX_STORED` is 500 (roughly a
year at 5-9 disclosures/week). The section is already the longest thing in the
post and the 200-char summary column is what makes it tall.

### Phase A — new page `/ai-ide-mcp-disclosures.html`

- [ ] Renderer writes a standalone page from the same `data/ai-ide-vulns.json`.
      Extend `generate_ai_ide_tracker.py` rather than adding a second script:
      it already owns `render_row`, `safe_url`, `esc`, `severity` colours.
- [ ] Full table, all stored entries, not a 12-row window.
- [ ] Client-side severity filter chips + product/text search + sortable date
      and severity columns. Vanilla JS, no framework, no backend. All data is
      already in the DOM, so filtering is a class toggle.
- [ ] Follow the standard page pattern: OG + Twitter Card meta, canonical,
      Cloudflare Analytics before `</body>`, social share bar.
- [ ] Auto-generated page, so it KEEPS a "Last updated" timestamp in
      `Month Day, Year` format (`strftime('%B %-d, %Y')`) per the timestamp rules.
- [ ] Move the table CSS out of inline `style=` attributes into `style.css`,
      since it will now be used on two pages. Re-minify and bump `?v=`.
- [ ] Register: add to `sitemap.xml`, add to `TOOL_PAGES` in
      `generate_llms_txt.py`, re-run it, then `propagate.py`.

### Phase B — blog post becomes a teaser

- [ ] Drop `DEFAULT_LIMIT` 12 -> 10 and tighten columns.
- [ ] Add "View all N disclosures" linking to the new page. N must come from
      the data, not a literal.
- [ ] Caption stays accurate about what the *table* shows vs what the archive
      holds. The CNA-score caveat and the earliest-published span stay.

### Phase C — summary column

- [ ] Strip the leading definitional sentence ("X is a Model Context Protocol
      server for Y.") before truncating. Verified against real data: fires on
      66 of 88 entries (75%), cuts roughly 40% of row height.
- [ ] Truncate to ~110 chars rather than 200.
- [ ] **Known ceiling:** the result reads as a mid-sentence fragment and is
      heavy with file paths (`crates/rmcp/src/transport/common/reqwest/...`).
      True 90-char impact clauses need semantic rewriting, not truncation.
      `summary_of()` already prefers `review_summary`, so the Phase 4 Claude
      trigger is the real fix. Do not build a second extraction heuristic to
      fake it: `affected_product()` took several iterations and shipped a P0.

### Gates

- [ ] `appsec` on the new page's client-side filter/sort JS (DOM injection,
      and the search box is user input rendered back to the page).
- [ ] `content-editor` on the new page's copy and any caption changes.
- [ ] `/pre-push-review` before push. Blocks on any P0/P1.

## Open: gitleaks pre-commit hook (2026-09-19, paused)

gitleaks 8.30.1 installed via brew. `core.hooksPath` still unset, no hook written.

Baseline scan: **773 findings in the working tree, all false positives.** This
site teaches secret handling, so the default ruleset fires on its own lesson
content: 766 `generic-api-key` across quiz/guide pages, 4 `curl-auth-header` in
`api-security.html`, 2 `jwt` in `jwt-decoder.html`, 1 `stripe-access-token` in
`secrets-management.html` (verified a placeholder: 13 chars, 1 distinct char).
History scan finds 794 across 918 commits.

- [ ] Write `.gitleaks.toml` with an allowlist for the teaching paths, or
      generate a baseline file and scan against it.
- [ ] Only then add `.githooks/pre-commit` + `git config core.hooksPath`, so
      the hook is tracked rather than living in `.git/hooks`.
- [ ] Hook must use `--redact` (printing the secret defeats the purpose and
      breaks the project's "never display secret values" rule) and `--staged`.
      Note `gitleaks protect` is gone in 8.x; it is `gitleaks git --staged`.
- [ ] A gate that fires 773 times gets bypassed on day one. Tune before arming.

## Phase A + B shipped — pre-push review 2026-09-19 (second pass)

| Reviewer | Verdict | Findings |
|---|---|---|
| appsec | approve | 0 P0/P1, 7 P3 |
| content-editor | approve-with-fixes | 1 P1, 6 P2, 3 P3 |

### Fixed (all verified independently before accepting)

- **P1 CVSS version.** Both pages claimed "CVSS v3.1 base scores". Confirmed
  against NVD: CVE-2026-58201 (8.7), CVE-2026-73218 (7.7) and CVE-2026-48124
  (8.5) carry **only** a v4.0 metric, roughly a fifth of stored entries. v3.1
  and v4.0 are different scales. Now one `SCORE_CAVEAT` constant shared by the
  teaser and the archive so they cannot drift.
- **P2** "until NVD completes its analysis" promised a correction that never
  arrives: NVD marks a growing share of 2026 CVEs `vulnStatus: Deferred`
  (confirmed on CVE-2026-48124). Reworded.
- **P2** "published since May 25, 2026" was computed from 87 of 88 entries,
  because the KEV row's `published` is deliberately blank. True only by luck;
  the next KEV entry with an older real date would have falsified it silently.
  Now "The earliest dated entry is from ...", which is true regardless.
- **P2** meta description said "updated daily" (the page is *checked* daily and
  rewritten only on change, which `archive_changed()` exists to guarantee) and
  said "GitHub security advisories" unscoped, which reads as the whole GHSA
  database rather than 9 repos.
- **P3 (appsec)** `data-score` was the only attribute not escaped. Safe today
  because `sort_key()` provably returns a float; now interpolated `:.1f` so a
  future string return cannot become stored XSS.
- **P3 (appsec)** `archive_changed()`'s strip was unanchored, so a summary
  containing the literal "Last updated: " could mask a real delta and freeze
  the published archive. Anchored to `<p id="d-updated">`.
- **P3 (appsec)** the page hand-pasted nav, footer, favicon, beacon token and
  `style.min.css?v=11` instead of using `lib.templates`/`lib.constants`, which
  already export all of it. The next CSS bump would have updated 740 pages and
  served stale CSS to this one. Now generated from the helpers, with tests
  asserting the CSS version and beacon token match the constants.
- **Accessibility.** Sortable headers were click-only: no `tabindex`, no
  keyboard handler, no `aria-sort`, and no `aria-live` on the result count, so
  keyboard and screen-reader users could not sort at all.
- **P2** missing theme toggle (dark-mode visitors got a light page) and missing
  JSON-LD. Added the same toggle markup and storage key as
  `exploit-tracker.html`, plus a breadcrumb schema via `breadcrumb_schema()`.
- **P3** "filterable by severity and product" — product is a search box, not a
  filter. Now "filterable by severity and searchable by product".
- **P3** verbless opening sentence and noun rotation between meta and body.

### Open follow-ups from this pass

- [ ] **10 of 88 rows have a blank "Affected product" cell** on a page whose
      description promises "search by product": CVE-2026-85674 (aider),
      CVE-2026-53965, CVE-2026-49986, CVE-2026-44192, CVE-2026-57495,
      CVE-2026-15643, CVE-2026-13341, CVE-2026-11624, CVE-2026-45609,
      CVE-2026-59822. All ten name the product in their own first clause, and
      search still finds them because the haystack covers the summary. This is
      a data/extraction gap, not a renderer bug. Belongs with Phase C.
- [ ] **Per-row CVSS version labels.** The caveat now states the v3.1/v4.0 mix
      in prose. Showing the version per row needs the collector to store a
      `score_version` field and a backfill for the 88 existing entries.
- [ ] **Cross-links.** The archive's only inbound link is the blog teaser.
      `ai-security.html` is the natural second entry point; `tools.html`,
      `resources.html` and `blog/index.html` also do not link it.
- [ ] Page weight at `MAX_STORED = 500` is roughly 500 KB uncompressed, marked
      with a `ponytail:` comment naming the ceiling. Revisit only if it nears
      the cap.

## Phase C (partial) — review 2026-09-19 (third pass)

| Reviewer | Verdict | Findings |
|---|---|---|
| appsec | approve-with-fixes | 0 P0/P1, 2 P2, 2 P3 |
| content-editor | approve-with-fixes | **3 P1**, 6 P2, 3 P3 |

### The summary shortening was reverted to a boilerplate strip only

Shipping a 130-char budget cost meaning. Measured, counting cells that retain
any impact language (allows/exposes/bypass/unauthenticated/traversal/...):

| variant | cells with no impact language | avg len |
|---|---|---|
| 260, no strip (original) | 48 of 88 | 249 |
| **260 + strip (shipped)** | **48 of 88** | **191** |
| 130 + strip (rejected) | 66 of 88 | 123 |

Stripping the definitional opener is free: identical meaning, 23% shorter.
Truncating to 130 was not. It landed worst on the two Critical 9.8 Cursor rows
(CVE-2026-50549, CVE-2026-50548), which ended up describing the sandbox that
was supposed to prevent the bug and stopping before the adversative that says
it fails. A clause-selection heuristic was tried and rejected: it improved the
aggregate (66 -> 50) but still missed those two rows, and it would have been a
third heuristic patching a second one.

**The ~90-char impact clause chosen at planning is not reachable by
truncation.** It needs rewriting, which is what `review_summary` is for and why
`summary_of()` already prefers it. That remains the open decision.

### Fixed this pass

- **P1** CVE-2026-11624 was NOT correctly blank. I judged it protocol guidance
  and encoded that in a test docstring as a permanent fact. Its CNA is
  `cve-coordination@google.com` and the fix is `--allowed-hosts` in v0.25.0 of
  Google's MCP Toolbox for Databases. A blank product beside Critical 9.4 made
  the page read as if MCP itself carried that score. Backfilled, test rewritten.
- **P1** the two Critical Cursor rows (see above).
- **P1** the 130-char budget (see above).
- **P2 (appsec)** `short_summary()`'s `review_summary` early return dropped the
  `str()` coercion the old call sites carried. A non-string written by the
  review pass raised `AttributeError` and aborted the daily render.
- **P2 (appsec)** the new verb pattern admitted prepositional-phrase subjects:
  "The vulnerability in Cline enables ..." extracted "vulnerability in Cline",
  putting a real vendor inside a phrase the advisory never asserted. Rejecting
  prepositions generally cost two correct captures ("Cursor for Windows",
  "gpt-researcher"), so only " in " is rejected.
- **P3 (appsec)** `DEFINITION_RE`'s `.{0,80}?` crossed sentence boundaries and
  deleted a real impact sentence preceding the gloss. Now `[^.]{0,80}?`.
- **P3 (appsec)** truncation could collapse a cell to "A..." on feed-controlled
  text.
- **P2** blank products 4 -> 0. aider, Cortex and Ansible Lightspeed MCP server
  backfilled by hand from NVD rather than by widening the regex, which would
  have reintroduced the false-positive class the closed verb set prevents.
- **P3** CVE-2026-59822 `published` backfilled to NVD's 2026-07-08, so it no
  longer renders a dash and sorts correctly.

### Open

- [ ] **`review_summary` for the Critical/High rows.** The one fix that would
      give real impact clauses without another heuristic. Needs the Phase 4
      scheduled Claude trigger, which is recurring and billable and still needs
      sign-off.
- [ ] **CVE-2026-57495 `vendor` is "Claude Code"; NVD says `agenticmail`.**
      Pre-existing `vendor_of()` misfire on `@agenticmail/claudecode`. It feeds
      `search_text()`, so searching "claude code" surfaces an AgenticMail
      advisory, and it feeds the caption's "57 of the 88" MCP count.
- [ ] Per-row CVSS version labels (needs a `score_version` field + backfill).
- [ ] Cross-links: nothing links into the tracker from `tools.html`,
      `ai-security.html` or the KEV pages.
- [ ] CVE-2026-13341's product string is long for a `nowrap` column.
