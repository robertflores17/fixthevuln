# Archived from todo.md 2026-10-29 (sections with zero open items, verbatim)

## Done — ISO 27001 study planners (2026-10-07)

Generator found (no rebuild): OneDrive `.../Documents/Invest/Business/Dropshipping/Etsy-Claude/`
— JSON per cert in `certifications/`, scripts in `Generate-scripts/Fillable` + `adhd-cert-planner`,
workflow in `.claude/skills/add-cert.md`. Its `store/*.sh` scripts have a stale BASE path
(`Documents/Home/Invest`). Steps 1–2 below are superseded by: write 4 JSON configs
(`pecb/iso27001_{li,la}.json` + `adhd_` pairs), run the 4 generators. Ships two new products: `pecb-iso27001-li` (Lead Implementer) and
`pecb-iso27001-la` (Lead Auditor). Each = 4 PDFs + `_bundle.zip` in R2.

Verified facts (pecb.com, 2026-10-07): 7 domains each (names below), credential tiers
(Provisional / Implementer|Auditor / Lead / Senior Lead), exam fee bundled into training,
free retake within 12 months. NOT published by PECB: domain weights, question count.
3 hours / 70% pass mark agree across third-party sources only → print with
"confirm with your training provider". No domain % badges (PECB doesn't weight them).

- [x] 1. (superseded) `scripts/generate_planners.py` (reportlab, in repo so it can't go missing again):
      cert data as a dict, standard layout (71 pp) + ADHD layout (123 pp), light/dark
      themes, AcroForm fields. Verify: page count + page titles diff against the CASP+
      reference PDFs via `pdftotext`; render pages to PNG and eyeball.
- [x] 2. ISO-specific replacements for IT-only pages: ports → Annex A theme map
      (control numbers + own wording, no ISO text), command line → ISMS mandatory
      documents, troubleshooting → PDCA / audit process, PBQ → scenario practice,
      powers-of-2 scratch → audit-sampling notes. Verify: no "port"/"PBQ" in output text.
- [x] 3. Generate 2 certs × 4 variants + 2 bundle zips into scratchpad (never committed).
      DONE 2026-10-07: configs in Etsy-Claude `certifications/pecb/`; 8 PDFs (72 pp std, 117 pp ADHD)
      + 2 bundles in Etsy-Claude `store/generated-pdfs/`. Added 4 optional config keys to the
      std/dark/ADHD generators (`reference_tables.commands_title`, `commands_notes_title`,
      `troubleshooting_methodology.page_title`, `brain_dump_sections`); CISM regenerates
      text-identical with old vs new scripts. Domain badges read "N of 7" (PECB publishes no weights).
- [x] 4. Store: add both IDs to `store/store.js` PRODUCTS + `CERT_NAMES` in
      `store/cloudflare-worker.js`; add to `store/security-governance.html` if it lists
      products statically. Verify: `node --check`, IDs match worker.
- [x] 5. ISO page CTA → link the ISO planners instead of the CISA one.
      DONE 2026-10-07: new vendor `pecb` (store.js PRODUCTS/VENDOR_GROUP_MAP/vendorDisplayName,
      worker CERT_NAMES, security-governance.html tab + PAGE_CONFIG + copy), store.js?v=8 on all
      10 store pages, iso-27001.html CTA. Verified in headless Chrome (PECB tab shows 2 cards).
- [x] 6a. R2 upload DONE 2026-10-07: 10 objects in `fixthevuln-planners`, each downloaded back
      and byte-compared to the local file (all match).
- [x] 6b. Worker deploy DONE 2026-10-07: version 60d9130d (deployed from a clean /tmp clone of HEAD
      + only the CERT_NAMES diff, which is still UNCOMMITTED locally — commit it with the site push).
      Live /checkout returns Stripe sessions for pecb-iso27001-li/la; unknown ID still rejected.
- [x] 6b2. Pre-push gate run 1 BLOCKED (content-editor P1: retake window). Fixed per PECB handbooks
      (LI v8.0, LA v7.0): retake = 12 months from coupon date after 15-day wait; open book, essay-type
      moving to MC; $1,000 standalone exam; 70% cited to handbook; allowed-materials checklist item.
      Regenerated all 10 files, re-uploaded to R2, byte-verified.
- [x] 6c. Shipped 2026-10-07: gate re-run PROCEED, `/self-qa` pass, PR #141 merged (1f49032d),
      worker redeployed from main (f0b1fdb8); live checkout verified for both IDs. Follow-ups merged
      same day: terms.html + email HTML escaping (#141), terms/privacy margins (#142, #143),
      Contact section alignment (#144), privacy footer Terms link (#145).

**Review:** Generator was never lost (it lives in Etsy-Claude on OneDrive), so the rebuild plan
was dropped after one search. Content Editor caught a real P1 (retake window counted from the
failed exam instead of the coupon date); the fix came from the PECB candidate handbooks, not the
product pages, which omit it. End-to-end paid purchase (email + download) not yet tested.

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

## Completed

- [x] PECB ISO/IEC 27001 Lead Implementer + Lead Auditor planners live in store (2026-10-07)
- [x] Sitemap: 381 → 450 URLs (2026-03-16)
- [x] Quiz analytics: POST /quiz/submit endpoint + sendBeacon client (2026-03-16)
- [x] generate_sitemap.py script (2026-03-16)
- [x] 12 LinkedIn hero marketing PNGs + captions (2026-03-16)
- [x] Merged 4 planner skills from Etsy-Claude (2026-03-16)
- [x] Created deploy + linkedin-content skills (2026-03-16)

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

## AppSec review of items 3-5 — fixes applied 2026-09-19

Verdict: approve (no P0/P1). Two P2/P3 findings acted on beyond the review's
own required-fixes list (none required, all P2/P3):

- **Hidden tests, two files.** 12 new tests in `test_aggregate_ai_ide_vulns.py`
  and all 28 tests appended across earlier passes in
  `test_generate_ai_ide_tracker.py` were sitting below the
  `if __name__ == '__main__': unittest.main()` guard. `unittest.main()` calls
  `sys.exit()`, so under direct invocation (`python3 tests/test_x.py`) those
  classes were never defined. Measured before the fix: 52 vs 64 direct/module
  in one file, 59 vs 87 in the other -- 28 tests silently not running under
  the invocation style a human would actually use. No CI workflow runs
  `unittest` at all, so this was purely a trust problem: a test that never
  runs reads as covered. Moved both blocks above the guard; all three test
  files now report identical counts under `python3 file.py` and
  `python3 -m unittest`.
- **A new false attribution, introduced by fixing the old one.** `vendor_of()`
  stripped scoped npm paths before slicing `text[:SUBJECT_CHARS]` for the
  weak-name window. Stripping shortens the string, so a name previously
  outside the 80-char window could land inside it. Reproduced: a scoped path
  early in an advisory pushed a later, unrelated "database cursor" mention
  into the window and mislabelled it "Cursor". Fixed by slicing the weak-name
  window from the original, unstripped text; only the strong-name search runs
  on the stripped copy. Verified all four cases (the repro, the original
  AgenticMail fix, a genuine scoped MCP product, a genuine Cursor lead) return
  correctly. Regression test added.
- **`score_version` was computed and discarded.** `fetch_cvss_from_nvd()`
  returned it but `format_for_review()` only wrote `cvss` into the pending
  entry, so the value never reached `pending_review.json` or `kev-data.json`.
  Now persisted as `cvss_version` in both the fresh-fetch and `--backfill`
  paths. Deliberately NOT wired into `generate_cve_pages.py`'s own
  `severity_label()`, which still assumes v3.1 bands -- that is a change to a
  separate, live-published pipeline with its own review surface, out of scope
  for items 3-5.
- **The sprint kit's CVSS ladder was a third, still-divergent copy.** Its
  docstring claimed to reuse fetch_kev.py logic while actually carrying no
  v4.0 branch and `metric_list[0]` with no Primary preference -- the exact
  defect item 4 fixed elsewhere, still live in the one pipeline that prints a
  score into a paid monthly PDF. Delegated to the shared
  `fetch_kev.cvss_from_metrics`, same pattern as the aggregator. Import wiring
  confirmed correct (the module import succeeds; `reportlab` is a pre-existing,
  unrelated dependency not installed in this sandbox, so the full module could
  not be exercised end-to-end here).

207 tests. Both AI IDE pages idempotent and unaffected by these fixes (none
changed currently-stored tracker data).

### Open, not done here

- [x] `generate_cve_pages.py`'s `severity_label()` — verified 2026-09-29, already fixed since this
      was written: the function takes `version` and caps v2 at HIGH, and all 3 call sites already
      pass `vuln.get('cvssVersion', '')`. No longer open.


## Stale-content remediation (2026-09-28) — from 5-way audit of pages dated Feb-Mar 2026

Order: batch 1 retired/renamed exams -> wrong exam codes -> wrong fees/format -> unsourced stats -> P2 drift.
Five editors run in parallel on disjoint file sets (Microsoft / AWS+Google+HashiCorp+K8s / CompTIA /
Cisco+ISC2+ISACA+EC+GIAC+OffSec / AI+evergreen). Rules: only apply facts verified against a vendor page;
unverifiable claims are softened or cut, never guessed; retired exams keep their URL and get a legacy
notice pointing to the successor; bump "Last updated" on edited generated/blog pages.
Gate: content-editor + appsec on the combined diff before any push.

- [x] Microsoft study guides (12) — pushed 57521920
- [x] AWS / Google / HashiCorp / K8s study guides (17) — pushed 57521920
- [x] CompTIA study guides (14) — pushed 57521920
- [x] Cisco / ISC2 / ISACA / EC-Council / GIAC / OffSec study guides (22) — pushed 57521920
- [x] AI + evergreen pages (genai-data-security, prompt-injection, ai-security-careers, 3 blog posts) — pushed 57521920, 650ba1af
- [x] Combined pre-push review, push, verify live — done

### Phase 2 (2026-09-28, same day) — certs/roadmaps/quizzes/store, found + fixed along the way

- [x] Fixed broken `ETSY_CERTS` path in 6 generator scripts — pointed at a local path that stopped
  existing after the 2026-08-09 OneDrive move; real source is
  `~/Library/CloudStorage/OneDrive-Personal/Documents/Invest/Business/Dropshipping/Etsy-Claude/certifications`.
  Read-only against that OneDrive data per Robert's call.
- [x] Added shared `RETIRED_EXAMS`/`retirement_notice()` to `scripts/lib/templates.py`, wired into
  `generate_cert_pages.py` + `generate_roadmaps.py`; regenerated all 66 certs + 66 roadmaps + hub +
  `data/cert-costs.json` (`retired`/`retired_note` fields) + `cert-cost-calculator.html` UI.
  Same 7 exams as the blog fix.
- [x] Found HashiCorp Terraform/Vault mislabeled everywhere (TA-003/VA-002, current is 004/003) and
  first-pass relabeled it — content-editor blocked (P0 x2): label changed but the OneDrive config's
  domain content is still the old curriculum (`vault_associate_003.json` file is misnamed — it holds
  VA-002 content). Fixed by reverting the label everywhere content is still old (~15 files) and adding
  a distinct `OUTDATED_CONTENT`/`outdated_content_notice()` (blue, not amber — these aren't discontinued,
  just showing an older version) pointing to the corrected blog study guide. Also fixed
  `generate_roadmaps.py`'s `exam_code` sourcing (was preferring the OneDrive config over the in-repo
  catalog, so roadmap and cert pages could show different labels for the same id) and caught a same-bug
  instance in `generate_cert_blog_posts.py`'s `CERT_BLOG_CONFIGS` that would have regenerated a
  mislabeled draft on the next `publish-blog.yml` run.
- [x] Pushed as of this writing — verify live site next. (verified live 2026-09-28)

### Phase 3-4 (2026-09-29) — quiz-page audit, all 68 pages

- [x] 7 retired-exam quizzes (ai900/az500/az204/ms900/ai102/aws-mls/aws-dbs) got the same
  `RETIRED_EXAMS` notice as their cert/roadmap pages — pushed 290a63e8
- [x] casp-plus/pentest-plus/linux-plus/data-plus/ceh quizzes: confirmed stale vs corrected blog
  guides, "Content note." added — pushed 17f82d16
- [x] Remaining ~52 quiz pages checked (exam code present in corresponding verified blog guide) —
  all current, no action needed. Confirmed the quiz domain-weight buttons are a generator-wide flat
  1/N% placeholder, not a staleness signal (checked against terraform-quiz, known-good).
- [x] Resolved `aws-security-quiz.html` (was ambiguous — confirmed stale, shows retired SCS-C02
  domains) and `aplus-quiz.html` (confirmed retired 220-1101/1102 generation) — "Content note."
  added to both, pushed f71ebc4e
- [x] `ai-security-quiz.html` / `cpts-quiz.html` — house-brand quizzes, no vendor blueprint to
  drift from, no action needed

### Phase 5 (2026-09-29) — aws-security-specialty cert/roadmap domain-name fix

- [x] Root cause: OneDrive `aws/security_specialty_scs-c03.json` pairs correct SCS-C03 weights
  with old SCS-C02 domain names (domains 1/2/6). Added `DOMAIN_NAME_OVERRIDES`/
  `apply_domain_overrides()` to `scripts/lib/templates.py` (in-memory correction, OneDrive file
  untouched), wired into `generate_cert_pages.py` + `generate_roadmaps.py`, regenerated. Verified
  against AWS's own SCS-C02->SCS-C03 comparison doc. Also fixed an AppSec P2: cert-page heatmap
  wasn't escaping domain names (roadmaps sibling already did) — pushed 24863451, verified live.

### Phase 6 (2026-09-29) — full site-wide re-audit via `scripts/audit_pages.py --skip-links`

- [x] AWS SysOps Administrator -> CloudOps Engineer rename (SOA-C02 -> SOA-C03) was already live and
  correct on the blog guide but stale in ~10 other places (CTA templates, comparison data, quiz
  registry, cross-links). Fixed all of them — pushed 6d7cae3d.
- [x] Found and fixed 9 stale/broken config-file-path entries in `generate_cert_blog_posts.py`'s
  `CERT_BLOG_CONFIGS` (a separate catalog from `generate_cert_pages.py`'s `PRODUCTS`, never
  reconciled) — 5 pointed at files that don't exist on disk at all (latent regeneration-breaks-page
  risk), 4 pointed at old-version files despite their live posts already being correct.
- [x] Added `comptia-data-plus` to `OUTDATED_CONTENT` (DA0-001 cert-page content vs DA0-002 current,
  verified live against comptia.org) — same pattern as HashiCorp Terraform/Vault.

### Phase 7 (2026-09-29) — "go fix whatever is left": closed all 4 Phase 6 follow-ups

- [x] `planner.html`'s aws-soa entry had genuinely stale domain content (6 domains, wrong weights/
  duration) — rewrote to match the verified-current SOA-C03 curriculum exactly.
- [x] Verified `cisco-ccnp-encor-study-guide.html` / `isc2-sscp-study-guide.html` via WebFetch
  against cisco.com/isc2.org — both accurate, no edits needed.
- [x] Fixed all individually-flagged stale-code mentions, then found and fixed the same pattern
  across career-paths.html, 3 comparison pages, and an sc-900-vs-security-plus mention.
- [x] Fixed `ai-security.html`'s unframed retired-exam quiz cards, then found and fixed the same gap
  on `practice-tests.html` (main hub) and all 13 auto-generated vendor pages — root-caused to
  `generate_practice_test_pages.py` having zero retirement awareness; added `RETIRED_QUIZZES`.
- [x] **Biggest find**: `data/blog_metadata.json` had 18 of 124 posts with stale title/excerpt text
  never updated when Phase 1 rewrote those posts. This file is live infrastructure (feeds
  blog/index.html, feed.xml, inject_blog_links.py cross-links) — NOT a "don't touch, historical"
  file like data/social/*. Fixed, regenerated everything downstream (9 more pages' cross-link cards
  updated as a result).
- Pushed as 4208f35e, merged with a same-day automated `publish-blog.yml` run (2 new posts), pushed
  as 31365355. Verified live.

Follow-ups still NOT done (unchanged from Phase 5/6, all require Robert or are non-blocking):
the store's other planner products for retired exams (`store/microsoft.html`, `resources.html` —
pricing/listing decision, needs Robert's call), `data/social/*`/`data/newsletters/*` snapshots
(deliberately left as historical artifacts, not rewritten), and a tech-debt note from
AppSec: `DOMAIN_NAME_OVERRIDES` is a second source of truth layered on the read-only OneDrive
config — fine as a one-off patch, revisit the override mechanism's location if more certs need the
same treatment.
