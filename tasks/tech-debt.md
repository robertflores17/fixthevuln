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
