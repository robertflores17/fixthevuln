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
