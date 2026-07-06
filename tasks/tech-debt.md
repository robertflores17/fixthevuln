## 2026-07-06 — Weekly Tech-Debt Audit

**Headline:** Steady pipeline week — 2 new CVE pages (146 total), 2 new blog posts published; AI Security Roundup 2026-07-03 drafted Thursday (publishes Tuesday per schedule ✓); new growth-review.yml workflow needs `growth-review` GitHub label pre-created or it will fail on first run (P2); appsec-review.md at July 2 (4 days, P0-watch 3rd consecutive week, July 4 US federal holiday context mitigates); 5 prior items all still open.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): 2026-07-02 (content date — 4 days old, triggers >2-day P0 rule; `pending_review.json` `last_checked: 2026-07-05T15:59:42 UTC` with `total_pending: 0` confirms KEV daily fetch IS running; "Update KEV last checked timestamp" commits July 3, 4, 5 all present; July 4 US federal holiday — CISA published no new KEV entries July 3–5; pipeline idle not stalled ✓)
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-07-03.md`): 2026-07-03 (Thursday — on schedule ✓; HTML publish pending Tuesday July 8 per publish-blog.yml schedule)
- `data/pending_review.json` pending count: 0 (last_checked: 2026-07-05T15:59:42 UTC ✓)

**New this week:**
- P2 workflow — `.github/workflows/growth-review.yml:56` — New workflow added 2026-07-04 (commit d9c9717) creates GitHub issues with `--label "growth-review"`. GitHub's `gh issue create` requires the label to pre-exist in the repo; if the label is absent, the step fails. No label-creation guard is present. Scheduled to run Mondays at 17:00 UTC — first run may be today. Fix: add `gh label create "growth-review" --color "0E8A16" --force` as a step before the issue create/edit block — Effort: XS
- P0-watch pipeline — `data/appsec-review.md` — Content date 2026-07-02 (4 days old, strictly triggers >2-day P0 rule, 3rd consecutive week flagged). Mitigating evidence: `pending_review.json` `last_checked: 2026-07-05` with `total_pending: 0`; daily KEV-fetch "Update KEV last checked timestamp" commits July 3 (4c60b6d), July 4 (1f17929), July 5 (904a4df); July 4 US federal holiday explains CISA gap. Assessment: holiday quiet period, pipeline NOT stalled. No GitHub issue created this cycle. Monitor: if no new CVE published by Tuesday 2026-07-08 EOD, escalate to hard P0 and file issue — Effort: monitor only

**Still open from prior audits:** 5
1. P1 content — `practice-tests/*.html:466` (13 pages) — `<p class="pt-timestamp">Last updated: April 2, 2026</p>` still present on all 13 practice-test hub pages. Open 3 weeks. Fix: remove timestamp block from `scripts/generate_practice_test_pages.py` template; re-run — Effort: XS
2. P2 generator — `scripts/` (14 files >500 LOC, unchanged) — `generate_guides.py` 2,896 · `generate_sprint_kit.py` 1,991 · `fetch_kev.py` 865 · `etsy_to_pinterest.py` 829 · `entity_extractor.py` 765 · `generate_linkedin_posts.py` 716 · `publish_editorial.py` 707 · `audit_pages.py` 661 · `generate_quiz_pages.py` 627 · `generate_cert_pages.py` 595 · `inject_store_ctas.py` 588 · `generate_practice_test_pages.py` 572 · `generate_roadmaps.py` 517 · `generate_cve_pages.py` 504 — Refactor candidates — Effort: L
3. P2 hygiene — repo-wide — `requirements.txt` absent; Pillow (`create_hero.py:4`, `generate_linkedin_posts.py:12`) and reportlab (`generate_sprint_kit.py:33–45`) undeclared external deps; `security-audit.yml` pip-audit silently no-ops — Create `requirements.txt` with pinned versions; add install step to CI — Effort: XS
4. P3 hygiene — `scripts/` (9 instances across 8 scripts) — Broad `except Exception:` without logging: `fetch_kev.py:63`, `generate_sitemap.py:86`, `update_sitemap.py:29`, `audit_pages.py:250,382`, `inject_error_reporter.py:46`, `generate_linkedin_posts.py:72`, `create_hero.py:51`, `health_check.py:127` — Add `logging.exception()` before each silent except — Effort: S
5. P3 hygiene — repo root — No `CLAUDE.md`; editorial rules uncodified in-repo — Create `CLAUDE.md` — Effort: XS

**Resolved since last audit:** None. 2 CVE pages published this week: CVE-2026-45659 (Microsoft SharePoint, July 2). AI Security Roundup 2026-07-03 drafted and blog/weekly-threat-roundup-2026-06-30.html published. Reconcile-sitemap.yml ran July 3, 4, 5, 6 keeping llms.txt/sitemap current.

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*, roadmaps/*): 322 (146 CVE + 66 cert + 43 comparisons + 67 roadmaps) — +2 CVE vs last week (320)
- Blog pages: 106 (was 104, +2: ai-security-roundup-2026-06-26.html + weekly-threat-roundup-2026-06-30.html)
- Sitemap entries: 583 (was 579, +4 ✓)
- Evergreen pages with timestamps (should be 0): 13 (practice-tests/*.html only — unchanged, P1 open 3 weeks)
- Pages missing from llms.txt: 0 (counts match on-disk ✓ — llms.txt updated to 146 CVE, 106 blog)
- Cache-bust drift count: 0 (no CSS/JS modified this week ✓)
- Scripts >500 LOC: 14 (unchanged)
- Store worker LOC: 1,151 (unchanged; `verifyStripeSignature` webhook HMAC at line 703 confirmed ✓; PRICING 599/1599 cents ↔ $5.99/$15.99 frontend ✓; CP_PRICING 899/1699, 1299/2499, 1699/3499 cents ✓)
- D1 migrations: 2 (0001_error_log, 0002_quiz_feedback — no new tables)
- Python scripts with bare `except Exception:` without logging: 9 instances / 8 scripts (unchanged)

---

## 2026-06-29 — Weekly Tech-Debt Audit

**Headline:** Quiet positive week — CVE pipeline active (6 new pages since last audit: 4 on June 24, 2 on June 26), KEV daily checks confirmed June 27 and June 28 with 0 pending, Friday AI roundup published June 26 on schedule, llms.txt/sitemap fully in sync; appsec-review.md content date is June 26 (3 days old, same weekend-quiet pattern as June 22 audit); no new material findings; 5 prior items all still open.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): 2026-06-26 (content date — 3 days old, triggers >2-day rule; mitigated: "Update KEV last checked timestamp" commits 2026-06-27 and 2026-06-28 confirm pipeline running daily; `pending_review.json` `last_checked: 2026-06-28T16:01:52 UTC` with `total_pending: 0` ✓; pipeline idle not stalled — weekend/Monday quiet period)
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-06-26.md`): 2026-06-26 (Friday — on schedule ✓)
- `data/pending_review.json` pending count: 0 (last_checked: 2026-06-28T16:01:52 UTC ✓)

**New this week:**
- P0-watch pipeline — `data/appsec-review.md` — Content date 2026-06-26 (3 days old, strictly triggers >2-day P0 rule). Mitigating evidence: KEV pipeline ran 2026-06-27 and 2026-06-28 (git: "Update KEV last checked timestamp"); `pending_review.json` last_checked=2026-06-28T16:01 with total_pending=0; CVE pipeline was active June 24 (4 CVEs: Lantronix, Ubiquiti ×3) and June 26 (2 CVEs: PTC, Cisco). Assessment: weekend quiet, not stalled. No GitHub issue created. Monitor: if no new CVE published by Tuesday 2026-07-01 EOD, escalate to hard P0. — Effort: monitor only

**Still open from prior audits:** 5
1. P1 content — `practice-tests/*.html:466` (13 pages) — `<p class="pt-timestamp">Last updated: April 2, 2026</p>` still present on all 13 practice-test hub pages. Open since June 22 audit. Fix: remove timestamp block from `scripts/generate_practice_test_pages.py` template; re-run — Effort: XS
2. P2 generator — `scripts/` (14 files >500 LOC, unchanged) — `generate_guides.py` 2,896 · `generate_sprint_kit.py` 1,991 · `fetch_kev.py` 865 · `etsy_to_pinterest.py` 829 · `entity_extractor.py` 765 · `generate_linkedin_posts.py` 716 · `publish_editorial.py` 707 · `audit_pages.py` 661 · `generate_quiz_pages.py` 627 · `generate_cert_pages.py` 595 · `inject_store_ctas.py` 588 · `generate_practice_test_pages.py` 572 · `generate_roadmaps.py` 517 · `generate_cve_pages.py` 504 — Refactor candidates — Effort: L
3. P2 hygiene — repo-wide — `requirements.txt` absent; Pillow (`create_hero.py:4`, `generate_linkedin_posts.py:12`) and reportlab (`generate_sprint_kit.py:33–45`) are undeclared external deps; `security-audit.yml` pip-audit silently no-ops — Create `requirements.txt` with pinned versions; add install step to CI — Effort: XS
4. P3 hygiene — `scripts/` (9 instances across 8 scripts) — Broad `except Exception:` without logging: `fetch_kev.py:63`, `generate_sitemap.py:86`, `update_sitemap.py:29`, `audit_pages.py:250,382`, `inject_error_reporter.py:46`, `generate_linkedin_posts.py:72`, `create_hero.py:51`, `health_check.py:127` — Add `logging.exception()` before each silent except — Effort: S
5. P3 hygiene — repo root — No `CLAUDE.md`; editorial rules (evergreen-page timestamp ban, cache-bust policy, pipeline health thresholds) uncodified in-repo — Create `CLAUDE.md` — Effort: XS

**Resolved since last audit:** None. CVE pipeline published 6 pages this week (June 24: Lantronix + 3×Ubiquiti; June 26: PTC + Cisco). All reconcile-sitemap.yml commits current.

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*, roadmaps/*): 320 (144 CVE + 66 cert + 43 comparisons + 67 roadmaps) — +6 CVE vs last week (314)
- Blog pages: 104 (was 103, +1)
- Sitemap entries: 579 (was 572, +7 ✓)
- Evergreen pages with timestamps (should be 0): 13 (practice-tests/*.html only — unchanged)
- Pages missing from llms.txt: 0 (all counts match on-disk ✓)
- Cache-bust drift count: 0 (no CSS/JS modified in last 7 days ✓)
- Scripts >500 LOC: 14 (unchanged)
- Store worker LOC: 1,151 (unchanged; `verifyStripeSignature` webhook HMAC at line 703 confirmed; PRICING 599/1599 cents ↔ $5.99/$15.99 frontend ✓; CP_PRICING 899/1699, 1299/2499, 1699/3499 cents ↔ CAREER_PATH_PRICING $8.99/$16.99, $12.99/$24.99, $16.99/$34.99 ✓)
- D1 migrations: 2 (0001_error_log, 0002_quiz_feedback — no new tables)
- Python scripts with bare `except Exception:` without logging: 9 instances / 8 scripts (unchanged)

---

## 2026-06-22 — Weekly Tech-Debt Audit

**Headline:** Strong resolution week — prior P0 (sitemap/llms.txt drift) and 3 other high-priority items fully closed; sitemap now clean (572 entries, 0 dupes, all blog+CVE counts match on-disk); one P0-watch: `appsec-review.md` content date is June 19 (3 days, triggers rule) but KEV pipeline confirmed healthy June 21 with 0 pending — contextually benign weekend quiet period, not a stall; 13 practice-test hub pages still carry evergreen timestamp from April 2.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): 2026-06-19 (content date — 3 days old, triggers P0 rule; `pending_review.json` `last_checked: 2026-06-21T16:24 UTC` with `total_pending: 0` confirms KEV daily fetch IS running; last CVE published June 19 (Splunk); no new KEV entries from CISA over the weekend — pipeline idle, not stalled ✓)
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-06-19.md`): 2026-06-19 (Friday — normal ✓; next due 2026-06-26)
- `data/pending_review.json` pending count: 0 (last_checked: 2026-06-21T16:24:28 UTC ✓)

**New this week:**
- P0-watch pipeline — `data/appsec-review.md` — Content date 2026-06-19 (3 days old, strictly triggers >2-day P0 rule). Mitigating evidence: `pending_review.json` `last_checked` is 2026-06-21 with `total_pending: 0`; daily KEV-fetch commits ("Update KEV last checked timestamp") present for June 20 and June 21; no new CISA KEV entries published over the June 19–22 weekend. Assessment: rule triggered but pipeline NOT stalled — weekend quiet period. No GitHub issue created this cycle. If `appsec-review.md` remains at June 19 by Tuesday June 24 EOD, escalate to hard P0 and file issue. — Effort: monitor only
- P1 content — `practice-tests/*.html` (13 files, e.g. `practice-tests/comptia.html:466`) — All 13 practice-test hub pages still carry `<p class="pt-timestamp">Last updated: April 2, 2026</p>`. The June 21 fix (`f4f6d63`) removed timestamps from the 47 quiz-root pages but did NOT regenerate the practice-test hub templates. These are evergreen hub pages — timestamps violate CLAUDE.md rule and mislead visitors. Fix: remove `pt-timestamp` block from `scripts/generate_practice_test_pages.py` template; re-run generator — Effort: XS

**Still open from prior audits:** 5
1. P1 content — `practice-tests/*.html:466` (13 pages) — "Last updated: April 2, 2026" still present on all 13 practice-test hub pages; quiz-root pages fixed June 21 but hub template not updated — Remove timestamp from `generate_practice_test_pages.py` template; re-run — Effort: XS
2. P2 generator — `scripts/` (14 files >500 LOC, unchanged) — `generate_guides.py` 2,896 · `generate_sprint_kit.py` 1,991 · `fetch_kev.py` 865 · `etsy_to_pinterest.py` 829 · `entity_extractor.py` 765 · `generate_linkedin_posts.py` 716 · `publish_editorial.py` 707 · `audit_pages.py` 661 · `generate_quiz_pages.py` 627 · `generate_cert_pages.py` 595 · `inject_store_ctas.py` 588 · `generate_practice_test_pages.py` 572 · `generate_roadmaps.py` 517 · `generate_cve_pages.py` 504 — Refactor candidates — Effort: L
3. P2 hygiene — repo-wide — `requirements.txt` absent; Pillow (`create_hero.py:4`, `generate_linkedin_posts.py:12`) and reportlab (`generate_sprint_kit.py:33–45`) are undeclared external deps; `security-audit.yml` pip-audit silently no-ops — Create `requirements.txt` with pinned versions; add install step to CI — Effort: XS
4. P3 hygiene — `scripts/` (9 instances across 8 scripts, +1 new: `health_check.py:127`) — Broad `except Exception:` without logging: `fetch_kev.py:63`, `generate_sitemap.py:86`, `update_sitemap.py:29`, `audit_pages.py:250,382`, `inject_error_reporter.py:46`, `generate_linkedin_posts.py:72`, `create_hero.py:51`, `health_check.py:127` — Add `logging.exception()` before each silent except — Effort: S
5. P3 hygiene — repo root — No `CLAUDE.md`; editorial rules (evergreen-page timestamp ban, cache-bust policy, pipeline health thresholds) uncodified in-repo — Create `CLAUDE.md` — Effort: XS

**Resolved since last audit:**
- ✅ P0 pipeline/llms — Sitemap/llms.txt drift: `fd41592` (June 15) wired `generate_sitemap.py` into publish workflows; daily `reconcile-sitemap.yml` (added June 21, `155ea65`) now keeps sitemap idempotent. Sitemap now 572 entries, **0 duplicates** (was 92 CVE dupes, 644 total), blog 103/103 match, CVE 138/138 match — fully resolved.
- ✅ P1 cache-bust/JS — `f4f6d63` (June 21): `error-reporter.js?v=1` and `quiz-engine.js?v=1` now on all HTML references — resolved.
- ✅ P2 pipeline — Overlapping sitemap-mutation logic resolved via daily reconcile job (`reconcile-sitemap.yml`) + `generate_sitemap.py` wired into `publish-blog.yml` and `auto-publish-cve.yml` — resolved.
- ✅ P2 content — `ai-agent-security-threats.html` confirmed present in `GUIDE_PAGES` at `scripts/generate_llms_txt.py:154` — resolved.

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*, roadmaps/*): 314 (138 CVE + 66 cert + 43 comparisons + 67 roadmaps) — +5 CVE vs last week (309)
- Evergreen pages with timestamps (should be 0): 13 (practice-tests/*.html only; quiz-root pages now 0 ✓)
- Pages missing from llms.txt: 0 (103 blog + 138 CVE both match on-disk ✓)
- Cache-bust drift count: 0 (resolved ✓)
- Sitemap duplicate entries: 0 / total entries: 572 (resolved ✓)
- Scripts >500 LOC: 14 (unchanged)
- Store worker LOC: 1,151 (unchanged; HMAC webhook verification confirmed at `verifyTokenHmac`; pricing cross-check: worker 599/1599 cents vs frontend $5.99/$15.99 — all match ✓)
- Python scripts with bare `except Exception:` without logging: 9 instances / 8 scripts (was 8 instances; `health_check.py:127` added)

---

## 2026-06-15 — Weekly Tech-Debt Audit

**Headline:** Escalating to P0: last week's "12 blog pages missing from sitemap" P1 has worsened to 14 (2 more added this cycle) and `llms-full.txt` now overstates CVE pages 225 vs 133 on disk (was 210/117) — the sitemap/llms.txt drift this audit has flagged at XS effort for three consecutive weeks is now producing a measurably wrong AI/LLM discovery surface; daily CVE and Friday roundup pipelines are healthy; 9 prior items still open, none resolved.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): 2026-06-13 (2 days old — at threshold; `pending_review.json` `last_checked` 2026-06-14T16:15 UTC with 0 pending — healthy ✓; 2 CVEs published 2026-06-13: Oracle, Ivanti)
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-06-12.md`): 2026-06-12 (Friday — draft present, not yet published; awaiting Tuesday `publish-blog.yml` cycle — normal ✓)
- `data/pending_review.json` pending count: 0 (last_checked: 2026-06-14T16:15:23 UTC ✓)

**New this week:**
- P0 pipeline/llms — `sitemap.xml` + `llms-full.txt` + `.github/workflows/publish-blog.yml:69` — Escalating last week's P1: blog pages missing from sitemap grew from 12 to 14 — this week's Tuesday publish added `blog/ai-security-roundup-2026-06-05.html` and `blog/weekly-threat-roundup-2026-06-09.html` on disk but neither appears in `sitemap.xml` because `publish-blog.yml`'s commit step (`git add blog/ cve/ comparisons/ data/ drafts/ sitemap.xml *.html` — note: `sitemap.xml` is listed but never regenerated/staged with new content since no `generate_sitemap.py`/`update_sitemap.py` step runs before it); compounding the existing CVE dedup drift (92 dupes, sitemap now 644 total/552 unique, was 637/545), `llms-full.txt` now lists 225 CVE entries vs 133 real CVE pages on disk (was 210/117 three weeks ago — drift accelerating ~+15 phantom entries/week); AI crawlers and LLM agents discovering this site via `llms.txt`/`llms-full.txt` now receive a page inventory that is wrong by a wide and growing margin, meeting this audit's P0 "wrong llms.txt" criterion — Fix (unchanged, still XS): add `python3 scripts/generate_sitemap.py` (rebuilt from disk with dedup) before the `git add` in `publish-blog.yml` and `auto-publish-cve.yml`; backfill the 14 missing blog URLs; regenerate `llms-full.txt` — Effort: XS

**Still open from prior audits:** 9
1. P1 cache-bust/JS — `js/error-reporter.js` + `js/quiz-engine.js` — Still no `?v=` cache-bust parameter on 120+ HTML references; Fix: add `?v=1` to all `<script src>` references; update `inject_error_reporter.py:46` and `generate_quiz_pages.py` templates — Effort: S
2. P1 content — `scripts/generate_quiz_pages.py:387` — Evergreen quiz/hub timestamps unchanged at 60 pages (47 quiz root + 13 practice-test hub); root cause: emits `<p>Last updated: {TODAY}</p>` on every regeneration — Remove timestamp block from quiz/practice-test templates; re-run generators — Effort: S
3. P2 content — `scripts/generate_llms_txt.py:154` — `ai-agent-security-threats.html` still absent from `GUIDE_PAGES`; page present on disk, AI crawlers see it under "Other Pages" not "Security Guides" — Add to `GUIDE_PAGES` set; re-run `generate_llms_txt.py` — Effort: XS
4. P2 generator — `scripts/` (14 files >500 LOC, unchanged) — `generate_guides.py` 2,896 · `generate_sprint_kit.py` 1,991 · `fetch_kev.py` 865 · `etsy_to_pinterest.py` 829 · `entity_extractor.py` 765 · `generate_linkedin_posts.py` 716 · `publish_editorial.py` 707 · `audit_pages.py` 661 · `generate_quiz_pages.py` 630 · `generate_cert_pages.py` 595 · `inject_store_ctas.py` 588 · `generate_practice_test_pages.py` 572 · `generate_roadmaps.py` 517 · `generate_cve_pages.py` 504 — Refactor candidates — Effort: L
5. P2 hygiene — repo-wide — `requirements.txt` still absent; Pillow (`create_hero.py:4`, `generate_linkedin_posts.py:12`) and reportlab (`generate_sprint_kit.py:33–45`) remain undeclared external deps; `security-audit.yml` pip-audit silently no-ops — Create `requirements.txt` with pinned versions; add install step to CI — Effort: XS
6. P2 pipeline — `scripts/generate_sitemap.py` + `scripts/update_sitemap.py` — Overlapping sitemap-mutation logic; no dedup guard; not wired into publish workflows (direct root cause of the new P0 above; fifth consecutive audit with this symptom) — Merge into single `sitemap.py` with `--build`/`--update` modes; wire into all publish workflows — Effort: S
7. P3 hygiene — `scripts/` (8 instances, unchanged) — Broad `except Exception:` without logging: `fetch_kev.py:63`, `generate_sitemap.py:86`, `update_sitemap.py:29`, `audit_pages.py:250,382`, `inject_error_reporter.py:46`, `generate_linkedin_posts.py:72`, `create_hero.py:51` — Add `logging.exception()` before each silent except — Effort: S
8. P3 hygiene — repo root — No `CLAUDE.md`; editorial rules uncodified in-repo — Create `CLAUDE.md` documenting evergreen-page rule, cache-bust policy, pipeline health thresholds — Effort: XS
9. P3 store — `store/cloudflare-worker.js` — PRICING (599/599 cents) and CP_PRICING (2:{899,1699}, 3:{1299,2499}, 4:{1699,3499}) cross-checked against `store/store.js` frontend (5.99/5.99, 8.99/16.99, 12.99/24.99, 16.99/34.99) — all confirmed matching; webhook HMAC verification confirmed present at `verifyTokenHmac` (line 608); no action needed, retained as a standing check item — Effort: N/A

**Resolved since last audit:** None. CVE pipeline active (+2 pages this week: Oracle, Ivanti, both correctly in sitemap and llms-full.txt); `ai-security-roundup-2026-06-12.md` generated Friday June 12 (publication awaiting Tuesday cycle — normal).

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*, roadmaps/*): 309 (133 CVE + 66 cert + 43 comparisons + 67 roadmaps) — +6 vs last week (303)
- Evergreen pages with timestamps (should be 0): 60 (unchanged)
- Pages missing from llms.txt: 14 (blog: `ai-security-roundup-2026-04-24` through `2026-06-05` + `weekly-threat-roundup-2026-04-28` through `2026-06-09`; was 12)
- Cache-bust drift count: 2 JS files unversioned (error-reporter.js, quiz-engine.js; unchanged)
- Sitemap duplicate entries: 92 CVE dupes (644 total / 552 unique; was 92/637 last week) — `llms-full.txt` CVE entries: 225 vs 133 real pages (was 210/117)
- Scripts >500 LOC: 14 (unchanged)
- Store worker LOC: 1,151 (unchanged; webhook HMAC verification confirmed at `verifyTokenHmac`, line 608)
- Python scripts with bare `except:`: 0 / broad `except Exception:` without logging: 8 (unchanged)

---

## 2026-06-08 — Weekly Tech-Debt Audit

**Headline:** New silent P1: 12 published blog pages (6 AI Security Roundups, 6 Weekly Threat Roundups) exist on disk but are absent from `sitemap.xml` and `llms-full.txt` because `publish-blog.yml` never calls `update_sitemap.py` — these pages are invisible to search crawlers and AI discovery; sitemap duplicate CVE drift persists at 92 dupes (637 total entries); pipeline healthy; 9 prior items still open.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): 2026-06-06 — at 2-day threshold; `pending_review.json` `last_checked` confirms KEV pipeline ran 2026-06-07T16:05 UTC with 0 new entries — healthy ✓
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-06-05.md`): 2026-06-05 (Friday — draft present, not yet published; awaiting Tuesday `publish-blog.yml` cycle — normal ✓)
- `data/pending_review.json` pending count: 0 (last_checked: 2026-06-07T16:05:24 UTC ✓)

**New this week:**
- P1 content/SEO — `sitemap.xml` + `.github/workflows/publish-blog.yml` — 12 blog pages on disk missing from sitemap: `blog/ai-security-roundup-2026-04-24.html` through `ai-security-roundup-2026-05-29.html` (6 pages) and `blog/weekly-threat-roundup-2026-04-28.html` through `weekly-threat-roundup-2026-06-02.html` (6 pages) all exist on disk but have no `<url>` entry in `sitemap.xml`; `publish-blog.yml` runs `publish_editorial.py` and `generate_threat_roundup.py` to generate HTML but has no `update_sitemap.py` step before its commit; `generate_llms_txt.py` sources counts from sitemap so `llms-full.txt` lists 86 blog pages vs 98 on disk — search crawlers and AI agents cannot discover these 12 content pages; root cause is the same overlapping-sitemap-logic P2 (item #7 below) but manifests as P1 content drag since roundup SEO value decays with time — Fix: add `python3 scripts/update_sitemap.py` (or `generate_sitemap.py`) step to `publish-blog.yml` before the git commit block; then run once manually to backfill the 12 missing URLs — Effort: XS

**Still open from prior audits:** 9
1. P1 cache-bust/JS — `js/error-reporter.js` + `js/quiz-engine.js` — No `?v=` cache-bust parameter on 120+ HTML references (`error-reporter.js` on 50+ pages, `quiz-engine.js` on 70+ quiz pages); Fix: add `?v=1` to all `<script src>` references; update `inject_error_reporter.py:46` and `generate_quiz_pages.py` templates — Effort: S
2. P1 pipeline/sitemap — `sitemap.xml` — CVE duplicate drift persists: 637 total entries, 92 duplicate CVE entries, 1 blank `/cve/` entry (was 97 dupes/632 total last week; CVE dupe count down slightly but total still rising as 5 new CVEs published); `update_sitemap.py` still missing dedup guard — Fix: add dedup check to `update_sitemap.py`; wire `generate_sitemap.py` into `auto-publish-cve.yml` — Effort: XS
3. P1 content — `scripts/generate_quiz_pages.py:387` — Evergreen quiz/hub timestamps (60 pages: 47 quiz root + 13 practice-test hub); root cause: `generate_quiz_pages.py` emits `<p>Last updated: {TODAY}</p>` on every regeneration — Remove timestamp block from quiz and practice-test templates; re-run generators — Effort: S
4. P2 content — `scripts/generate_llms_txt.py:154` — `ai-agent-security-threats.html` absent from `GUIDE_PAGES`; page present on disk but AI crawlers see it under "Other Pages" not "Security Guides" — Add to `GUIDE_PAGES` set; re-run `generate_llms_txt.py` — Effort: XS
5. P2 generator — `scripts/` (14 files >500 LOC) — `generate_guides.py` 2,896 · `generate_sprint_kit.py` 1,991 · `fetch_kev.py` 865 · `etsy_to_pinterest.py` 829 · `entity_extractor.py` 765 · `generate_linkedin_posts.py` 716 · `publish_editorial.py` 707 · `audit_pages.py` 661 · `generate_quiz_pages.py` 630 · `generate_cert_pages.py` 595 · `inject_store_ctas.py` 588 · `generate_practice_test_pages.py` 572 · `generate_roadmaps.py` 517 · `generate_cve_pages.py` 504 — Refactor candidates — Effort: L
6. P2 hygiene — repo-wide — `requirements.txt` absent; Pillow (`create_hero.py:4`, `generate_linkedin_posts.py:12`) and reportlab (`generate_sprint_kit.py:33–45`) are undeclared external deps; `security-audit.yml` pip-audit silently no-ops — Create `requirements.txt` with pinned versions; add install step to CI — Effort: XS
7. P2 pipeline — `scripts/generate_sitemap.py` + `scripts/update_sitemap.py` — Overlapping sitemap-mutation logic; no dedup guard; not wired into publish workflows (root cause of items #2 above and new P1 finding) — Merge into single `sitemap.py` with `--build`/`--update` modes; wire into all publish workflows — Effort: S
8. P3 hygiene — `scripts/` (8 instances) — Broad `except Exception:` without logging: `fetch_kev.py:63`, `generate_sitemap.py:86`, `update_sitemap.py:29`, `audit_pages.py:250,382`, `inject_error_reporter.py:46`, `generate_linkedin_posts.py:72`, `create_hero.py:51` — Add `logging.exception()` before each silent except — Effort: S
9. P3 hygiene — repo root — No `CLAUDE.md`; editorial rules uncodified in-repo — Create `CLAUDE.md` documenting evergreen-page rule, cache-bust policy, pipeline health thresholds — Effort: XS

**Resolved since last audit:** None. CVE pipeline active (+5 pages: SolarWinds, Mirasvit, Linux, Android, Oracle WebLogic Server); `ai-security-roundup-2026-06-05.md` generated Friday June 5 (publication awaiting Tuesday cycle — normal).

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*, roadmaps/*): 303 (127 CVE + 66 cert + 43 comparisons + 67 roadmaps) — +5 CVE vs last week (298)
- Evergreen pages with timestamps (should be 0): 60 (47 quiz root + 13 practice-test hub; unchanged)
- Pages missing from llms.txt: 12 (blog: `ai-security-roundup-2026-04-24` through `2026-05-29` + `weekly-threat-roundup-2026-04-28` through `2026-06-02`)
- Cache-bust drift count: 2 JS files unversioned (error-reporter.js, quiz-engine.js — 120+ HTML refs; unchanged)
- Sitemap duplicate entries: 92 CVE dupes + 1 blank `/cve/` entry (637 total; was 97/632 last week)
- Scripts >500 LOC: 14 (unchanged)
- Store worker LOC: 1,151 (unchanged; Stripe HMAC webhook verification confirmed at lines 659–698)
- Python scripts with bare `except:`: 0 / broad `except Exception:` without logging: 8 (unchanged)

---

## 2026-06-01 — Weekly Tech-Debt Audit

**Headline:** JS cache-bust gap newly identified — `error-reporter.js` and `quiz-engine.js` carry no `?v=` parameters across 120+ HTML references (browsers cache stale JS indefinitely after any future update); sitemap duplicate drift worsened for the third consecutive week (627→632 entries, +5 CVE appends without dedup); pipeline healthy with 5 CVEs published; 8 prior items all still open.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): 2026-05-30 (pipeline confirmed run 2026-05-31T15:58 UTC via `pending_review.json` `last_checked` with 0 new KEV entries — healthy ✓; 5 CVEs published this week: Palo Alto Networks, Nx, TanStack, Daemon, LiteSpeed)
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-05-29.md`): 2026-05-29 (Friday — draft present, not yet published; awaiting Tuesday `publish-blog.yml` cycle — normal ✓)
- `data/pending_review.json` pending count: 0 (last_checked: 2026-05-31T15:58:57 UTC ✓)

**New this week:**
- P1 cache-bust/JS — `js/error-reporter.js` + `js/quiz-engine.js` — No `?v=` cache-bust parameter on any HTML file references: `error-reporter.js` loaded bare (`/js/error-reporter.js`) on 50+ pages (e.g. `kev-archive.html`, `password-policy.html`, `cvss-calculator.html`); `quiz-engine.js` loaded bare (`js/quiz-engine.js`) on 70+ quiz pages; both files last committed 2026-05-12 — browsers will cache stale JS indefinitely after any future update; CSS files are correctly versioned (style.min.css v=8, quiz.css v=3, comparison.css v=3, store.css v=12, practice-tests.css v=1) but JS files are not — Fix: add `?v=1` suffix to all `<script src="js/error-reporter.js">` and `<script src="js/quiz-engine.js">` references in HTML templates; update `inject_error_reporter.py:46` and `scripts/generate_quiz_pages.py` to emit versioned paths going forward — Effort: S

**Still open from prior audits:** 8
1. P1 — Evergreen quiz/hub timestamps (60 pages; 47 quiz root + 13 practice-test hub); root cause: `scripts/generate_quiz_pages.py:387` emits `<p>Last updated: {TODAY}</p>` on every regeneration
2. P1 — Sitemap duplicate drift worsening: 627→632 total entries this week (+5 CVE appends without dedup, estimated ~97 duplicate CVE entries + 1 blank `/cve/` entry); `update_sitemap.py` still missing dedup guard; `llms-full.txt` inherits overcounting via `generate_llms_txt.py`; direct root cause: item #6 below (fourth consecutive audit unresolved)
3. P2 — `ai-agent-security-threats.html` absent from `GUIDE_PAGES` in `scripts/generate_llms_txt.py:154`; page present on disk, AI crawlers see it in "Other Pages" not "Security Guides"
4. P2 — Script size: 14 scripts >500 LOC (generate_guides.py 2,896 · generate_sprint_kit.py 1,991 · fetch_kev.py 865 · etsy_to_pinterest.py 829 · entity_extractor.py 765 · generate_linkedin_posts.py 716 · publish_editorial.py 707 · audit_pages.py 661 · generate_quiz_pages.py 630 · generate_cert_pages.py 595 · inject_store_ctas.py 588 · generate_practice_test_pages.py 572 · generate_roadmaps.py 517 · generate_cve_pages.py 504)
5. P2 — `requirements.txt` absent; Pillow (`create_hero.py:4`, `generate_linkedin_posts.py:12`) and reportlab (`generate_sprint_kit.py:33–45`) are undeclared external deps; `security-audit.yml` pip-audit silently no-ops
6. P2 — `generate_sitemap.py` + `update_sitemap.py` overlapping sitemap-mutation logic; no dedup guard in publish workflows (direct root cause of P1 item #2 above; fourth consecutive audit with this symptom)
7. P3 — 8 broad `except Exception:` handlers without logging: `fetch_kev.py:63`, `generate_sitemap.py:86`, `update_sitemap.py:29`, `audit_pages.py:250,382`, `inject_error_reporter.py:46`, `generate_linkedin_posts.py:72`, `create_hero.py:51`
8. P3 — No `CLAUDE.md` in repository root

**Resolved since last audit:** None.

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*, roadmaps/*): 298 (122 CVE + 66 cert + 43 comparisons + 67 roadmaps) — +5 CVE vs last week
- Evergreen pages with timestamps (should be 0): 60 (unchanged; root cause script not yet fixed)
- Sitemap duplicate entries: ~97 CVE dupes + 1 blank `/cve/` entry (632 total; was 627 last week, +5 new appends)
- Pages missing from llms.txt: 0 (all CVE pages exist on disk; 0 true 404s)
- Cache-bust drift count: 2 JS files unversioned (error-reporter.js, quiz-engine.js — no `?v=` on 120+ HTML references; newly identified this audit)
- Scripts >500 LOC: 14 (unchanged)
- Store worker LOC: 1,151 (unchanged; Stripe HMAC webhook verification confirmed at lines 658–698)
- Python scripts with bare `except:`: 0 / broad `except Exception:` without logging: 8 (unchanged)

---

## 2026-05-25 — Weekly Tech-Debt Audit

**Headline:** Sitemap duplicate-CVE drift recurred (92 duplicate entries, 1 blank; 627 total vs 535 unique URLs) — `update_sitemap.py` re-appended without dedup on post-rebuild publishes; llms-full.txt overstates CVE count at 210 vs 117 unique pages; pipeline healthy; 7 prior items all still open.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): 2026-05-23 (content date; pipeline confirmed run 2026-05-24T15:54 UTC via `pending_review.json` `last_checked` with 0 new KEV entries — pipeline healthy ✓)
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-05-22.md`): 2026-05-22 (Friday — draft present, not yet published; awaiting Tuesday `publish-blog.yml` cycle — normal ✓)
- `data/pending_review.json` pending count: 0 (last_checked: 2026-05-24T15:54:13 UTC ✓)

**New this week:**
- P1 pipeline/sitemap — `sitemap.xml` + `llms-full.txt` — CVE sitemap duplicate drift: `sitemap.xml` has 627 total URLs but only 535 unique (92 duplicate CVE entries + 1 blank `/cve/` entry); `update_sitemap.py` re-appended CVE URLs on post-rebuild publish cycles without checking for existing entries; all 117 CVE pages exist on disk (0 true orphans, 0 404s) but `generate_llms_txt.py` sources counts from sitemap, so `llms-full.txt` overstates CVE count as 210 vs 117 real pages and lists each of 92 CVEs twice; same root cause as 2026-05-11 P0 (P2 item #5 unfixed) — Fix: run `python3 scripts/generate_sitemap.py` to rebuild sitemap from disk; add dedup guard to `update_sitemap.py` before appending new URLs; wire sitemap rebuild into `auto-publish-cve.yml` — Effort: XS

**Still open from prior audits:** 7
1. P1 — Evergreen quiz/hub timestamps (60 pages; 47 quiz root + 13 practice-test hub); root cause: `scripts/generate_quiz_pages.py:387` emits `<p>Last updated: {TODAY}</p>` on every regeneration
2. P2 — `ai-agent-security-threats.html` absent from `GUIDE_PAGES` in `scripts/generate_llms_txt.py:154`; page present on disk, AI crawlers see it in "Other Pages" not "Security Guides"
3. P2 — Script size: 14 scripts >500 LOC (generate_guides.py 2,896 · generate_sprint_kit.py 1,991 · fetch_kev.py 865 · etsy_to_pinterest.py 829 · entity_extractor.py 765 · generate_linkedin_posts.py 716 · publish_editorial.py 707 · audit_pages.py 661 · generate_quiz_pages.py 630 · generate_cert_pages.py 595 · inject_store_ctas.py 588 · generate_practice_test_pages.py 572 · generate_roadmaps.py 517 · generate_cve_pages.py 504)
4. P2 — `requirements.txt` absent; Pillow (`create_hero.py:4`, `generate_linkedin_posts.py:12`) and reportlab (`generate_sprint_kit.py:33–45`) are undeclared external deps; `security-audit.yml` pip-audit silently no-ops
5. P2 — `generate_sitemap.py` + `update_sitemap.py` overlapping sitemap-mutation logic; no dedup guard in publish workflows (direct root cause of new P1 above; now third consecutive audit with this symptom)
6. P3 — 8 broad `except Exception:` handlers without logging: `fetch_kev.py:63`, `generate_sitemap.py:86`, `update_sitemap.py:29`, `audit_pages.py:250,382`, `inject_error_reporter.py:46`, `generate_linkedin_posts.py:72`, `create_hero.py:51`
7. P3 — No `CLAUDE.md` in repository root

**Resolved since last audit:** None.

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*, roadmaps/*): 293 (117 CVE + 66 cert + 43 comparisons + 67 roadmaps) — +10 CVE vs last week
- Evergreen pages with timestamps (should be 0): 60 (unchanged; root cause script not yet fixed)
- Sitemap duplicate entries: 92 CVE dupes + 1 blank `/cve/` entry (627 total → 535 unique)
- Pages missing from llms.txt: 0 (all 117 CVE pages exist on disk; 0 true 404s)
- Cache-bust drift count: 0 (no CSS/JS commits in past 7 days; versions: style.min.css v=8, quiz.css v=3, comparison.css v=3, store.css v=6, practice-tests.css v=1)
- Scripts >500 LOC: 14 (unchanged)
- Store worker LOC: 1,151 (unchanged; Stripe webhook HMAC verification confirmed at lines 521–529)
- Python scripts with bare `except:`: 0 / broad `except Exception:` without logging: 8 (unchanged)

---

## 2026-05-18 — Weekly Tech-Debt Audit

**Headline:** All-clear week — last week's P0 (91 orphaned CVE entries in sitemap/llms-full.txt) is resolved; 107 CVE pages perfectly synced across sitemap, llms-full.txt, and disk; daily KEV pipeline healthy; 7 prior debt items remain open with no new findings.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): 2026-05-16 (2 days — at threshold; daily fetch confirmed run 2026-05-17 via `last_checked` field with 0 new KEV entries — pipeline healthy ✓)
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-05-15.md`): 2026-05-15 (Friday — draft present, not yet published; normal pre-Tuesday cadence ✓)
- `data/pending_review.json` pending count: 0 (last_checked: 2026-05-17T15:49:51 UTC — KEV fetch ran yesterday ✓)

**New this week:**
- None. No new P0/P1/P2/P3 findings.

**Still open from prior audits:** 7
1. P1 — Evergreen quiz/hub timestamps (60 pages; was 61 — down 1; 47 quiz root + 13 practice-test hub); root cause: `scripts/generate_quiz_pages.py:387` emits `<p>Last updated: {TODAY}</p>` on every regeneration
2. P2 — `ai-agent-security-threats.html` absent from `GUIDE_PAGES` in `scripts/generate_llms_txt.py:154`; page present on disk, AI crawlers see it in "Other Pages" not "Security Guides"
3. P2 — Script size: 14 scripts >500 LOC (generate_guides.py 2,896 · generate_sprint_kit.py 1,991 · fetch_kev.py 865 · etsy_to_pinterest.py 829 · entity_extractor.py 765 · generate_linkedin_posts.py 716 · publish_editorial.py 707 · audit_pages.py 661 · generate_quiz_pages.py 630 · generate_cert_pages.py 595 · inject_store_ctas.py 588 · generate_practice_test_pages.py 572 · generate_roadmaps.py 517 · generate_cve_pages.py 504)
4. P2 — `requirements.txt` absent; `security-audit.yml` pip-audit silently no-ops; Pillow (`create_hero.py:4`, `generate_linkedin_posts.py:12`) and reportlab (`generate_sprint_kit.py:33–45`) are undeclared external deps
5. P2 — `generate_sitemap.py` + `update_sitemap.py` overlapping sitemap-mutation logic; no reconciliation guard in publish workflows
6. P3 — 8 broad `except Exception:` handlers without logging: `fetch_kev.py:63`, `generate_sitemap.py:86`, `update_sitemap.py:29`, `audit_pages.py:250,382`, `inject_error_reporter.py:46`, `generate_linkedin_posts.py:72`, `create_hero.py:51`
7. P3 — No `CLAUDE.md` in repository root

**Resolved since last audit:**
- **P0** pipeline/llms — CVE orphan drift resolved: `sitemap.xml` rebuilt from disk (617 URLs; 0 orphaned CVEs; 0 CVEs on disk missing from sitemap); `llms-full.txt` regenerated and synced (all 107 CVE pages present, 0 orphaned entries); GitHub issue #83 closed. Pipeline commits this week: `ebf0e14` (1 CVE published), `a6377dd`/`660a08d` (KEV auto-fetch 2026-05-15/16), `2282866` (KEV timestamp update 2026-05-17).

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*, roadmaps/*): 283 (107 CVE + 66 cert + 43 comparisons + 67 roadmaps) — +3 CVE vs last week
- Evergreen pages with timestamps (should be 0): 60 (was 61 — down 1; 47 quiz root + 13 practice-test hub)
- Pages missing from llms.txt: 0 (llms-full.txt and disk in perfect sync ✓)
- Cache-bust drift count: 0 (no CSS/JS commits in past 7 days; versions: style.min.css v=8, quiz.css v=3, comparison.css v=3, store.css v=6, practice-tests.css v=1)
- Scripts >500 LOC: 14 (unchanged)
- Store worker LOC: 1,151 (unchanged; Stripe webhook HMAC verification confirmed present)
- Python scripts with bare `except:`: 0 / broad `except Exception:` without logging: 8 (unchanged)

---

## 2026-05-11 — Weekly Tech-Debt Audit

**Headline:** P0 regression: sitemap.xml has 91 orphaned CVE entries after the 104-CVE batch publish; llms-full.txt inherits 92 dead CVE links via generate_llms_txt.py; AI crawlers receive 404s for 88% of listed CVE URLs — GitHub issue #83 filed; pipeline and roundup are healthy; 7 prior items remain open.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): 2026-05-11 (today — healthy ✓)
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-05-08.md`): 2026-05-08 — draft present, awaiting Tuesday `publish-blog.yml` cycle (normal for Monday)
- `data/pending_review.json` pending count: 0 (last KEV check 2026-05-10)

**New this week:**
- P0 pipeline/llms — `sitemap.xml` + `llms-full.txt` + `llms.txt` — CVE orphan drift: `sitemap.xml` lists 195 CVE URLs but only 104 CVE pages exist on disk (91 orphaned `<url>` elements); `generate_llms_txt.py:188` reads from sitemap rather than scanning disk, so `llms-full.txt` inherits 92 orphaned CVE links + 1 duplicate entry; `llms.txt` reports "197 CVE pages" vs 104 on disk; AI crawlers following llms-full.txt get 404s for 88% of listed CVE URLs; additionally `CVE-2026-42208` exists on disk but is missing from llms-full.txt — Root cause: `auto-publish-cve.yml`/`publish-blog.yml` append CVE URLs via `update_sitemap.py` without purging removed pages after batch replaces — Fix: run `python3 scripts/generate_sitemap.py` to rebuild from disk, then `generate_llms_txt.py`; wire `generate_sitemap.py` into `auto-publish-cve.yml` after any CVE add/delete — Effort: XS — GitHub issue: #83

**Still open from prior audits:** 7
1. P1 — Evergreen quiz/hub timestamps (61 pages; was 60 — flat; 48 quiz root + 13 practice-test hub); root cause: `scripts/generate_quiz_pages.py` and `scripts/generate_practice_test_pages.py` still emit timestamp blocks
2. P2 — `ai-agent-security-threats.html` absent from `GUIDE_PAGES` in `scripts/generate_llms_txt.py:141–157`; falls into "Other Pages" in llms-full.txt (from 2026-05-04 audit, unfixed)
3. P2 — Script size: 14 scripts >500 LOC (generate_guides.py 2,896 · generate_sprint_kit.py 1,991 · fetch_kev.py 865 · etsy_to_pinterest.py 829 · entity_extractor.py 765 · generate_linkedin_posts.py 716 · publish_editorial.py 707 · audit_pages.py 661 · generate_quiz_pages.py 630 · generate_cert_pages.py 595 · inject_store_ctas.py 588 · generate_practice_test_pages.py 572 · generate_roadmaps.py 517 · generate_cve_pages.py 504)
4. P2 — `requirements.txt` absent; `security-audit.yml` pip-audit silently no-ops
5. P2 — `generate_sitemap.py` + `update_sitemap.py` overlapping sitemap-mutation logic; no reconciliation step in publish workflows (root cause of P0 above)
6. P3 — 8 broad `except Exception:` handlers without logging: `fetch_kev.py:63`, `generate_sitemap.py:86`, `update_sitemap.py:29`, `audit_pages.py:250,382`, `inject_error_reporter.py:46`, `generate_linkedin_posts.py:72`, `create_hero.py:51`
7. P3 — No `CLAUDE.md` in repository root

**Resolved since last audit:** None. `ai-security-roundup-2026-05-01.md` published as expected (normal Tuesday pipeline, not a tracked finding).

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*, roadmaps/*): 280 (104 CVE + 66 cert + 43 comparisons + 67 roadmaps)
- Evergreen pages with timestamps (should be 0): 61 (was 60 — flat; 48 quiz root + 13 practice-test hub)
- Pages missing from llms.txt: 1 (`CVE-2026-42208` on disk, absent from llms-full.txt); 91 orphaned CVE entries in sitemap → 92 dead links in llms-full.txt (P0)
- Cache-bust drift count: 0 (no CSS/JS commits in past 7 days; versions: style.min.css v=8, quiz.css v=3, comparison.css v=3, store.css v=6, practice-tests.css v=1)
- Scripts >500 LOC: 14 (up from 10 confirmed last audit; full enumeration above)
- Store worker LOC: 1,151 (unchanged; Stripe webhook HMAC verification confirmed at line 703)
- Python scripts with bare `except:`: 0 / broad `except Exception:` without logging: 8 (unchanged)

---

## 2026-05-04 — Weekly Tech-Debt Audit

**Headline:** Pipeline healthy (appsec-review.md 2 days old, within threshold); evergreen timestamp P1 worsened from 20 → 60 pages as new quiz content was regenerated without the fix; `ai-agent-security-threats.html` miscategorized in `llms-full.txt`; all six prior debt items remain open.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): 2026-05-02 17:05 UTC (~45 h old — within 2-day threshold ✓)
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-05-01.md`): 2026-05-01 — draft present, awaiting Tuesday `publish-blog.yml` publication cycle (normal)
- `data/pending_review.json` pending count: 0 (all CVEs processed; last KEV check 2026-05-03)

**New this week:**
- P1 content — `scripts/generate_quiz_pages.py:387` — Evergreen timestamp regression: quiz+practice-test hub pages with banned "Last updated" grew from **20 → 60** (47 quiz + 13 practice-test hub) as new quiz content was regenerated without removing the timestamp block; root cause is line 387 in `generate_quiz_pages.py` still emits `<p>Last updated: {TODAY}</p>` — Remove the timestamp block from the quiz and practice-test page templates; re-run generators to clear all 60 instances — Effort: S
- P2 content — `scripts/generate_llms_txt.py:141` — `ai-agent-security-threats.html` falls into the catch-all "Other Pages (1 pages)" section in `llms-full.txt` because it is absent from `GUIDE_PAGES`; AI agents discovering the site via llms-full.txt will not see it listed under Security Guides — Add `"ai-agent-security-threats.html"` to `GUIDE_PAGES` set and re-run `generate_llms_txt.py` — Effort: XS

**Still open from prior audits:** 6
1. P1 — Evergreen quiz/hub timestamps (60 pages; was 20 — worsening)
2. P2 — Script size: `generate_guides.py` (2,896 LOC; note: prior audit's "5,189 LOC" figure was incorrect — actual is unchanged at 2,896), `generate_sprint_kit.py` (1,991 LOC)
3. P2 — `requirements.txt` absent; `security-audit.yml` pip-audit silently no-ops
4. P2 — Sitemap `lastmod` not wired into `auto-publish-cve.yml` or `publish-blog.yml`
5. P3 — 8 broad `except Exception:` handlers without logging across `fetch_kev.py:63`, `generate_sitemap.py:86`, `update_sitemap.py:29`, `audit_pages.py:250,382`, `inject_error_reporter.py:46`, `generate_linkedin_posts.py:72`, `create_hero.py:51`
6. P3 — No `CLAUDE.md` in repository root

**Resolved since last audit:**
- P2 pipeline — `drafts/ai-security-roundup-2026-04-24.md.published` — Apr 24 roundup now published as `blog/ai-security-roundup-2026-04-24.html` ✓
- Metric correction — `generate_guides.py` LOC: prior audit (2026-04-27) reported 5,189 LOC; actual file is 2,896 LOC (unchanged since 2026-04-20 audit); the prior figure was erroneous

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*, roadmaps/*): 278 (102 CVE + 66 cert + 43 comparisons + 67 roadmaps)
- Evergreen pages with timestamps (should be 0): **60** (was 20 — regression; 47 quiz + 13 practice-test hub)
- Pages missing from llms.txt: 0 (ai-agent-security-threats.html is present but miscategorized as "Other Pages")
- Cache-bust drift count: 0 (no CSS/JS commits in past 7 days; versions: style.min.css v=8, quiz.css v=3, comparison.css v=3, store.css v=6, practice-tests.css v=1)
- Scripts >500 LOC: 10 (unchanged)
- Store worker LOC: 1,151 (unchanged; webhook HMAC signature verification confirmed present)
- Python scripts with bare `except:`: 0 / broad `except Exception:` without logging: 8 (unchanged)

---

## 2026-04-27 — Weekly Tech-Debt Audit

**Headline:** Pipeline healthy and CVE automation current; 20 evergreen quiz pages still carry banned "Last updated" timestamps, `CLAUDE.md` remains absent, and `generate_guides.py` grew from 2,896 → 5,189 LOC since last audit — the refactor case is now urgent.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): 2026-04-26 17:15 UTC (1 day old — healthy)
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-04-24.md`): 2026-04-24 — draft exists but **not yet published** (no `.published` suffix; prior week's `ai-security-roundup-2026-04-17.md.published` published correctly)
- `data/pending_review.json` pending count: 0 (all CVEs processed as of Apr 26)

**New this week:**

- P1 content — `*.html` (20 quiz pages, repo-wide) — Evergreen quiz pages still contain hardcoded "Last updated: March 30, 2026" timestamps; reduced from ~92 last audit but not zero; CLAUDE.md rule: evergreen pages must carry no `Last updated` date — Strip timestamp injection from quiz generators; confirm `generate_quiz_pages.py` no longer emits the block — S
- P2 generator — `scripts/generate_guides.py:1` — **Grew from 2,896 → 5,189 LOC** since last audit (+2,293 lines in one week); now ~10× the 500-LOC threshold with distinct entry paths for AI Security, GRC, and Blue Team content — Split into per-domain modules sharing a common `scripts/lib/html_builder.py` — L
- P2 generator — `scripts/generate_sprint_kit.py:1` — 2,115 LOC (~4× threshold); mixes PDF generation, CISA KEV enrichment, and template rendering — Extract KEV enrichment into a shared library callable by other generators — M
- P2 generator — `scripts/generate_cert_pages.py:1` — 1,224 LOC; data loading and HTML rendering interleaved — Separate data layer from rendering layer — S
- P2 generator — `scripts/entity_extractor.py:1` (849 LOC) and `scripts/audit_pages.py:1` (768 LOC) — Both parse CVE/page structures and likely share utility logic — Extract shared CVE-parsing helpers into `scripts/lib/` — S
- P2 pipeline — `scripts/generate_sitemap.py` + `scripts/update_sitemap.py` — Two scripts with overlapping sitemap-mutation logic and nearly identical imports; consolidation candidate — Merge into a single `sitemap.py` with `--build` and `--update` modes — S
- P2 pipeline — `drafts/ai-security-roundup-2026-04-24.md` — Friday Apr 24 roundup draft exists but lacks `.published` suffix; `publish-blog.yml` may not have triggered or the file was not staged — Verify `publish-blog.yml` is wired to consume roundup drafts automatically on Fridays — XS
- P2 hygiene — repo-wide — `requirements.txt` still absent (carried from prior audit); Pillow/PIL confirmed in `create_hero.py` and `generate_linkedin_posts.py`; `security-audit.yml` runs `pip-audit -r requirements.txt` which silently no-ops — Create `requirements.txt` with pinned versions; add install step to CI — XS
- P2 hygiene — `scripts/` (8 instances) — Broad `except Exception:` handlers without structured logging in `fetch_kev.py:63`, `generate_sitemap.py:86`, `update_sitemap.py:29`, `audit_pages.py:250`, `audit_pages.py:382`, `inject_error_reporter.py:46`, `generate_linkedin_posts.py:72`, `create_hero.py:51` (reduced from 14 last audit but not zero) — Add `logging.exception()` before silencing — S
- P2 content — `sitemap.xml` — `lastmod` dates for non-CVE pages frozen at 2026-03-22; `update_sitemap.py` is not wired into auto-publish workflows — Add `update_sitemap.py` invocation to `auto-publish-cve.yml` and `publish-blog.yml` — S
- P3 hygiene — repo root — `CLAUDE.md` still absent (carried from prior audit); editorial rules are uncodified in-repo — Create `CLAUDE.md` documenting the evergreen-page rule, cache-bust policy, and pipeline health thresholds — XS
- P3 SEO — `404.html`, `analytics.html`, `kev_cards.html`, `store/success.html` — Four utility pages missing OG, Twitter Card, and canonical meta tags — Add minimal tags if any indexing risk exists — XS
- P3 data — `data/kev.json` — 1.1 MB full CISA KEV catalog mirror loaded by scripts querying only a small field subset — Add a filtered loader in `scripts/lib/` to avoid full-file reads on each run — M
- P3 store — `store/cloudflare-worker.js` vs `store/store.js` — Server-side PRICING (standard $29, adhd $39, dark $39, adhd_dark $49) verified in worker; client prices served dynamically (not statically duplicated) — no mismatch; verify both files updated atomically on next pricing change — XS

**Still open from prior audits:** 6
1. P1 — Evergreen quiz pages with timestamps (20 remain; was ~92)
2. P2 — Script size refactoring (`generate_guides.py` worsened significantly)
3. P2 — `requirements.txt` absent
4. P2 — Sitemap `lastmod` not wired into publish workflows
5. P3 — Broad `except Exception:` without logging (8 blocks; was 14)
6. P3 — No `CLAUDE.md` in repository root

**Resolved since last audit:**
- P0 pipeline — `data/appsec-review.md` stall — resolved; file updated 2026-04-26, pipeline running on schedule
- P2 llms.txt/sitemap gap — resolved; reconciliation closed the ~129-file gap; sitemap now matches all 546 HTML pages; llms-full.txt regenerated 2026-04-27
- P2 store worker webhook verification — confirmed present; constant-time HMAC comparison verified in `store/cloudflare-worker.js`

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*): 299 (191 CVE + 66 cert + 42 comparison)
- Evergreen pages with timestamps (should be 0): 20 (was ~92)
- Pages missing from llms.txt: 0 (was ~129)
- Cache-bust drift count: 0 (style.min.css v=8 ×532, quiz.css v=3 ×68, comparison.css v=3 ×42, store.css v=12 ×12, practice-tests.css v=1 ×14 — all consistent)
- Scripts >500 LOC: ≥10 (top 5 confirmed: generate_guides.py 5,189 · generate_sprint_kit.py 2,115 · generate_cert_pages.py 1,224 · entity_extractor.py 849 · audit_pages.py 768; prior audit enumerated 10 total)
- Store worker LOC: 1,151 (unchanged)
- Python scripts with bare `except:`: 0 / broad `except Exception:` without logging: 8 (was 14)

---

## 2026-04-20 — Weekly Tech-Debt Audit

**Headline:** Daily CVE pipeline skips writing `appsec-review.md` on zero-KEV days, breaking the primary health signal; 92 evergreen pages carry illegal "Last updated" timestamps.

**Pipeline pulse:**
- Daily CVE trigger last output (`data/appsec-review.md`): **2026-04-17** ⚠️ STALE (3 days — P0)
- Friday AI trend roundup last file (`drafts/ai-security-roundup-2026-04-17.md.published`): 2026-04-17 (Friday ✓)
- `data/pending_review.json` pending count: 0–1 (file is 253 bytes)

**New this week:**

- **P0** Pipeline health — `data/appsec-review.md` — Last written 2026-04-17; daily KEV fetch is running (commits `dd098fb`, `05aad4d` update `data/latest-update.json` on Apr 18–20) but the file is only written on publish days. Zero-CVE days produce no review log, making staleness an unreliable health signal. Fix: write a daily "0 new CVEs — pipeline healthy" entry in `scripts/fetch_kev.py` whenever pending count = 0; confirm `.github/workflows/fetch-vulnerabilities.yml` always touches the file. GitHub issue: #75 — Effort: S

- **P1** Content/evergreen — `ai102-quiz.html:630` (and ~79 other quiz pages, ~12 practice-test hub pages, `index.html`) — Visible `<p>Last updated: <date></p>` rendered in page header on pages classified as evergreen (quizzes, practice-test category hubs, landing page). CLAUDE.md rule: evergreen pages must carry no `Last updated` timestamp. Grep confirms 250 total HTML files contain the string; approximately 92 are genuinely evergreen (quiz + practice-test hub + index). Roadmaps, comparisons, and blog posts may legitimately carry dates. Fix: remove the timestamp injection from `scripts/generate_quiz_pages.py` and `scripts/generate_practice_test_pages.py` for quiz/hub output; audit `scripts/generate_cert_pages.py` for the same. — Effort: S

- **P2** Script size — `scripts/generate_guides.py` (2,896 LOC), `scripts/generate_sprint_kit.py` (1,991 LOC) — Both exceed the 500-LOC refactor threshold by 4–5×; each has multiple independent entry paths (generate_guides handles 60+ guide types; generate_sprint_kit handles PDF layout, R2 upload, and manifest writing). 8 additional scripts between 504–865 LOC also exceed threshold: `fetch_kev.py` (865), `etsy_to_pinterest.py` (829), `entity_extractor.py` (765), `generate_linkedin_posts.py` (716), `publish_editorial.py` (707), `audit_pages.py` (661), `generate_quiz_pages.py` (630), `generate_cert_pages.py` (595). Total: 10 scripts >500 LOC. Fix: split generate_guides.py into domain-specific modules (wstg, owasp, compliance, etc.); extract PDF/R2/manifest into separate sprint_kit sub-modules. — Effort: L

- **P2** Python hygiene — No `requirements.txt` — The only external dependency (`reportlab`) is installed ad-hoc via `pip install reportlab` in `.github/workflows/generate-sprint-kit.yml`. The monthly `security-audit.yml` runs `pip-audit -r requirements.txt` which silently no-ops when the file is absent, leaving the Python dep audit completely blind. Fix: create `requirements.txt` with `reportlab>=4.0` and pin a version. — Effort: XS

- **P2** Store worker growth — `store/cloudflare-worker.js` at **1,151 LOC** — New route sections (`CP_PRICING`, career-path expansion) added since original launch. Several new code paths (career-path checkout, seller notification email) have minimal inline comments. Webhook signature verification was not explicitly confirmed in this static audit. Fix: verify Stripe webhook signature verification is present (`stripe.webhooks.constructEvent` or manual HMAC check) before next store deploy; add section-level comments to new paths. — Effort: S

- **P2** llms.txt/sitemap gap — `sitemap.xml` (401 URLs) vs 530 HTML files on disk — Gap of ~129 files. `generate_llms_txt.py` sources from sitemap, so any file absent from sitemap is also absent from llms.txt and llms-full.txt. Likely innocent (store/success.html, error pages, excluded hubs) but unconfirmed. No orphaned entries detected (generation is automated from sitemap). Fix: run a reconciliation pass — list HTML files not in sitemap.xml and confirm each is intentionally excluded; add missing content pages. — Effort: S

- **P3** Python hygiene — `scripts/audit_pages.py:376,382`, `scripts/update_sitemap.py:29`, `scripts/create_hero.py:51`, `scripts/generate_sitemap.py:86`, `scripts/generate_linkedin_posts.py:72`, `scripts/inject_error_reporter.py:46` — 14 `except Exception` / bare `except:` blocks across 10 scripts; lines 376 and 382 of `audit_pages.py` swallow exceptions without any logging, making silent failures invisible. Fix: add `print(f"[warn] {e}", file=sys.stderr)` at minimum in the silent catches. — Effort: XS

- **P3** Cache-bust process — `scripts/lib/constants.py` (`STYLE_CSS_VERSION=8`, `QUIZ_CSS_VERSION=3`, `COMPARISON_CSS_VERSION=3`, `STORE_CSS_VERSION=6`, `PRACTICE_TESTS_CSS_VERSION=1`) — Version bumps are manual with no guard against forgetting. No CSS/JS changes detected in the past 7 days so no active drift this week. Fix: add a pre-commit hook or CI check that fails if a CSS/JS file is modified without a matching constants.py bump. — Effort: S

- **P3** Repo hygiene — No `CLAUDE.md` in repository root — Project rules referenced in this audit (evergreen page timestamps, pipeline health thresholds) are not codified in the repo, making them invisible to contributors and automation. Fix: create `CLAUDE.md` documenting the evergreen-page rule, cache-bust policy, and pipeline health definitions. — Effort: XS

**Still open from prior audits:** 0
**Resolved since last audit:** N/A (first audit)

**Metrics tracked:**
- Total generated pages (cve-*, cert-*, comparisons/*): 288 (139 CVE + 66 cert + 83 comparisons)
- Evergreen pages with timestamps (should be 0): ~92 (80 quiz + 12 practice-test hubs + index.html)
- Pages missing from llms.txt: ~129 (530 HTML on disk vs 401 in sitemap)
- Cache-bust drift count: 0 (no CSS/JS commits in past 7 days)
- Scripts >500 LOC: 10
- Store worker LOC: 1,151
- Python scripts with broad/bare except: 14 blocks across 10 files

---
