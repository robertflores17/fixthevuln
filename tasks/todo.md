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

## Backlog

### SEO & Distribution (from 2026-03-16 growth plan)
- [x] Sitemap expanded to 454 URLs (4 new blog posts added)
- [x] IndexNow propagation (450 URLs submitted)
- [x] Quiz analytics endpoint + client wiring deployed
- [x] 12 LinkedIn hero PNGs + captions created
- [x] Submit sitemap in Google Search Console — already submitted, GSC "Verify fix" triggered on 331 pages (2026-03-16)
- [x] Start LinkedIn cadence — first post published (2026-03-16)
- [ ] Monitor GSC validation on 331 "discovered not indexed" pages (check in 1-2 weeks)

## Review Notes

_Add post-implementation review notes here._

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
- [x] Verify: `workflow_dispatch` manual run, check `gh run list`. Dispatched three times
      across the build (initial secret check, arXiv 406 fix, NVD key validation); all
      `completed/success`, confirmed via `gh run view --json jobs`.

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

- [x] Reassessed 2026-09-29, not fixing: `aggregate_ai_ide_vulns.py` DOCTYPE guard only scans
      `body[:2048]` — CPython's ElementTree installs no external-entity handler regardless of
      DOCTYPE position, so this is defense-in-depth on an already-XXE-immune parser. Taking a
      `defusedxml` dependency isn't worth it for that.
- [x] Fixed 2026-09-29: arXiv `title` now goes through `_trim(title, 200)`, matching every other
      text field from that parser. `resp.read()` on the NVD response left unbounded deliberately
      (trusted first-party HTTPS host, matches this project's DOS-exclusion precedent).
- [x] `severity_label()` v2/v3.1 band mismatch — not a live bug, no v2 row exists on this page.
- [x] Already resolved: `_cvss_from_metrics` in `aggregate_ai_ide_vulns.py` is now a thin wrapper
      over `fetch_kev.cvss_from_metrics`, which owns `CVSS_METRIC_ORDER` for the whole site — the
      duplicate, differently-ordered copy this item warned about no longer exists.
- [x] Fixed 2026-09-29: `render_row()` now uses `long_date()` instead of a bare ISO string.
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
- [x] `SKILLS.md` is untracked and has never been committed, though `CLAUDE.md`
      references it. Not part of this change set.

## Plan: scale the AI IDE tracker section (2026-09-19)

Decided with Robert: full archive moves to its own page, the blog post keeps a
short teaser, and the summary column gets shortened. Not started.

**Why:** 12 of 88 shown, 76 already invisible, `MAX_STORED` is 500 (roughly a
year at 5-9 disclosures/week). The section is already the longest thing in the
post and the 200-char summary column is what makes it tall.

### Phase A — new page `/ai-ide-mcp-disclosures.html`

- [x] Renderer writes a standalone page from the same `data/ai-ide-vulns.json`.
      Extend `generate_ai_ide_tracker.py` rather than adding a second script:
      it already owns `render_row`, `safe_url`, `esc`, `severity` colours.
- [x] Full table, all stored entries, not a 12-row window.
- [x] Client-side severity filter chips + product/text search + sortable date
      and severity columns. Vanilla JS, no framework, no backend. All data is
      already in the DOM, so filtering is a class toggle.
- [x] Follow the standard page pattern: OG + Twitter Card meta, canonical,
      Cloudflare Analytics before `</body>`, social share bar.
- [x] Auto-generated page, so it KEEPS a "Last updated" timestamp in
      `Month Day, Year` format (`strftime('%B %-d, %Y')`) per the timestamp rules.
- [~] Move the table CSS into `style.css`. **Not done deliberately**: the
      archive's classes exist only on that page, and moving them would mean
      re-minifying and bumping `?v=` across 740 pages for no shared use.
      Superseded line kept for context:
- [x] (was) Move the table CSS out of inline `style=` attributes into `style.css`,
      since it will now be used on two pages. Re-minify and bump `?v=`.
- [x] Register: add to `sitemap.xml`, add to `TOOL_PAGES` in
      `generate_llms_txt.py`, re-run it, then `propagate.py`.

### Phase B — blog post becomes a teaser

- [x] Drop `DEFAULT_LIMIT` 12 -> 10 and tighten columns.
- [x] Add "View all N disclosures" linking to the new page. N must come from
      the data, not a literal.
- [x] Caption stays accurate about what the *table* shows vs what the archive
      holds. The CNA-score caveat and the earliest-published span stay.

### Phase C — summary column

- [x] Strip the leading definitional sentence ("X is a Model Context Protocol
      server for Y.") before truncating. Verified against real data: fires on
      66 of 88 entries (75%), cuts roughly 40% of row height.
- [~] Truncate to ~110 chars. **Rejected after measurement**: 130 chars cost
      18 of 88 cells their impact language. Shipped the boilerplate strip at
      the original 260 instead (same meaning, 23% shorter).
- [ ] **Known ceiling:** the result reads as a mid-sentence fragment and is
      heavy with file paths (`crates/rmcp/src/transport/common/reqwest/...`).
      True 90-char impact clauses need semantic rewriting, not truncation.
      `summary_of()` already prefers `review_summary`, so the Phase 4 Claude
      trigger is the real fix. Do not build a second extraction heuristic to
      fake it: `affected_product()` took several iterations and shipped a P0.

### Gates

- [x] `appsec` on the new page's client-side filter/sort JS (DOM injection,
      and the search box is user input rendered back to the page).
- [x] `content-editor` on the new page's copy and any caption changes.
- [x] `/pre-push-review` before push. Blocks on any P0/P1.

## Open: gitleaks pre-commit hook (2026-09-19, paused)

gitleaks 8.30.1 installed via brew. `core.hooksPath` still unset, no hook written.

Baseline scan: **773 findings in the working tree, all false positives.** This
site teaches secret handling, so the default ruleset fires on its own lesson
content: 766 `generic-api-key` across quiz/guide pages, 4 `curl-auth-header` in
`api-security.html`, 2 `jwt` in `jwt-decoder.html`, 1 `stripe-access-token` in
`secrets-management.html` (verified a placeholder: 13 chars, 1 distinct char).
History scan finds 794 across 918 commits.

- [x] Write `.gitleaks.toml` with an allowlist for the teaching paths, or
      generate a baseline file and scan against it.
- [x] Only then add `.githooks/pre-commit` + `git config core.hooksPath`, so
      the hook is tracked rather than living in `.git/hooks`.
- [x] Hook must use `--redact` (printing the secret defeats the purpose and
      breaks the project's "never display secret values" rule) and `--staged`.
      Note `gitleaks protect` is gone in 8.x; it is `gitleaks git --staged`.
- [x] A gate that fires 773 times gets bypassed on day one. Tune before arming.

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

- [x] **10 of 88 rows have a blank "Affected product" cell** on a page whose
      description promises "search by product": CVE-2026-85674 (aider),
      CVE-2026-53965, CVE-2026-49986, CVE-2026-44192, CVE-2026-57495,
      CVE-2026-15643, CVE-2026-13341, CVE-2026-11624, CVE-2026-45609,
      CVE-2026-59822. All ten name the product in their own first clause, and
      search still finds them because the haystack covers the summary. This is
      a data/extraction gap, not a renderer bug. Belongs with Phase C.
- [x] **Per-row CVSS version labels** — fixed 2026-09-29, pushed 1951624a.
- [x] **Cross-links** from `ai-security.html`, `tools.html`, `exploit-tracker.html` — fixed
      2026-09-29, pushed 1951624a. (`resources.html`/`blog/index.html` still don't link it — minor,
      not chased down.)
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
- [x] **CVE-2026-57495 `vendor` misattribution** — verified 2026-09-29, already fixed: `vendor` is
      now `"Unknown"` / `product` is `"AgenticMail"` in `data/ai-ide-vulns.json`, not "Claude Code".
- [x] Per-row CVSS version labels — fixed 2026-09-29 (`reverify_entries()` backfill +
      `render_archive_row()` display), pushed 1951624a.
- [x] Cross-links from `tools.html`, `ai-security.html`, `exploit-tracker.html` — fixed 2026-09-29,
      pushed 1951624a.
- [x] CVE-2026-13341's product string shortened to "Kong Konnect MCP Server" — fixed 2026-09-29,
      pushed 1951624a.


# OPEN ITEMS — reconciled 2026-09-19 (second pass)

Supersedes every list above, including the "consolidated" one from earlier
today, which went stale within the same day (items 3-5 shipped in commit
a7a654b3 while still listed there as open). This is the authoritative list.

## Needs a decision from Robert

1. **`review_summary` via the Phase 4 scheduled Claude trigger.** Recurring and
   billable, never created. It is the only thing that turns the summary column
   into real impact clauses -- the plumbing already exists (`summary_of()`
   prefers the field, `short_summary()` leaves it uncut, `status: "excluded"`
   drops a row from both the table and the count). Would fix the two Critical
   9.8 Cursor rows that describe Cursor's sandbox rather than the flaw. Draft
   trigger prompt is above, in the Phase 4 section. **Nothing below costs
   anything.**
2. ~~Rotate the two Resend API keys~~ **Done** -- confirmed rotated;
   `.claude/settings.local.json` still holds the two dead key literals in its
   Bash allowlist (cosmetic now, cleanup command given separately).
   `RESEND_API_KEY`/`RESEND_EMAIL_API` GitHub secrets still show their old
   2026-06-22 update timestamp -- if the *old* key was what those used,
   `notify-on-failure.yml`'s email step and `health-check.yml` are silently
   broken until `gh secret set RESEND_API_KEY` runs. Not yet confirmed either
   way.
3. **AI vuln-intel draft/publish pipeline** (unrelated to the tracker, older
   item). Deliberately deferred 2026-09-14 to stay manual-review-only. Spec at
   `docs/superpowers/specs/2026-09-12-ai-vuln-intel-pipeline-design.md`.

## Shipped since the last reconciliation

Items 3, 4, 5 (vendor misattribution, one CVSS precedence, v2 severity bands)
and the third divergent CVSS copy in `generate_sprint_kit.py` -- see "Items 3-5
fixed" and "AppSec review of items 3-5" sections below for the full detail.
`generate_cve_pages.py`'s own `severity_label()` remains unfixed (separate
live-published pipeline, needs its own review) -- carried forward below.

## P2 — wrong data on a published page

~~4. `generate_cve_pages.py`'s `severity_label()`~~ **Fixed 2026-09-20.** Now
   `severity_label(cvss, version)`, caps v2 at HIGH. `cvssVersion` travels
   `fetch_kev.py` -> `pending_review.json` (`cvss_version`) ->
   `generate_html.py`'s `convert_to_kev_format` -> `kev-data.json`
   (`cvssVersion`) -> the three call sites in `generate_cve_pages.py`. Verified
   0 of 227 currently-published entries change label (latent-not-live fix, per
   design). AppSec: approve, no P0/P1. One optional P3 noted and left as-is: a
   human hand-editing `pending_review.json`'s `cvss` for a genuine v2 score
   without also setting `cvss_version` would still print CRITICAL -- fails in
   the conservative (over-, not under-) direction, so not worth guarding.
   `tests/test_generate_cve_pages_severity.py`, 7 tests.

## P3 — hardening, no live exploit path

5. ~~**arXiv DOCTYPE guard only scans `body[:2048]`.**~~ **Reassessed 2026-09-29, not fixing.**
   The code's own comment already covers why: CPython's ElementTree installs no external-entity
   handler regardless of DOCTYPE position, so the guard is defense-in-depth on top of an already-
   XXE-immune parser, not the only control. Taking a `defusedxml` dependency for this is not
   worth it per the project's own "no new dependency for what stdlib already handles" bias.
6. ~~**`resp.read()` on the NVD response is unbounded**~~ **Reassessed 2026-09-29, not fixing.**
   NVD is a trusted first-party HTTPS host with a 30s timeout; matches the project's own DOS/
   resource-exhaustion exclusion precedent. Fixed the other half: **arXiv `title` now goes
   through `_trim(title, 200)`** (2026-09-29).
7. **No CSP anywhere on the site.** Escaping is the only XSS control on these
   pages. Pre-existing and site-wide; any CSP needs `'unsafe-inline'` or a
   nonce pass across 740 pages because the nav toggle uses inline `onclick`. Still open --
   its own project, out of scope for a quick pass.

## P4/P5 — polish and reach

8. **[x] Per-row CVSS version labels — fixed 2026-09-29.** `reverify_entries()` now backfills
   `score_version` on entries missing it using the record it already fetches for the rejection
   check (no extra NVD call), and `render_archive_row` appends ` (v3.1)`/`(v4.0)`/etc. to the
   severity cell when present. The 88 pre-existing entries backfill passively over ~5 weeks at
   the existing `REVERIFY_BATCH=20/week` rate.
9. **[x] Cross-links into the tracker — fixed 2026-09-29.** Added cards/links from `tools.html`,
   `ai-security.html`, and `exploit-tracker.html` (the KEV page).
10. **[x] Table cells render bare ISO dates — fixed 2026-09-29.** `render_row` (blog teaser table)
    now uses `long_date()`, matching `render_archive_row`.
11. **[x] CVE-2026-13341's product string — fixed 2026-09-29.** Shortened to "Kong Konnect MCP
    Server" in `data/ai-ide-vulns.json`.
12. **Monitor GSC validation on 331 "discovered not indexed" pages** — due ~2026-03-30, now
    overdue. Not fixable from here (no GSC API access); ask Robert to check the Search Console
    UI directly next time SEO work comes up.

## Known and deliberate — do not "fix"

- **GHSA has contributed 0 of 88 rows.** NVD dedup wins. Documented in
  `generate_ai_ide_tracker.py`. Do not rewrite the caption to drop the source.
- **GHSA runs unauthenticated on purpose.** urllib replays headers across
  redirects and the Actions `GITHUB_TOKEN` is write-scoped. 60 req/hr per
  shared runner IP, so a 403 is possible; it degrades to "no GHSA rows".
- **Archive page weight** is ~500 KB uncompressed at `MAX_STORED = 500`, marked
  with a `ponytail:` comment naming the ceiling. Revisit only near the cap.

## AI Vuln Intel Reviewer trigger updated 2026-09-20

Robert asked to "loop with Marlowe, Sable and Griggs" and "auto-commit". The
trigger already existed (created 2026-09-13 in an earlier session I hadn't
discovered) -- it had already auto-published once, 2026-09-18, 9 entries, via
an inline verification pass that predated the three agent personas. Updated
via `RemoteTrigger` (`trig_017xceZFhTAxS5hL9bGr6KMF`), not created.

**Key finding that changed the design:** the plan's Task 14 assumed
Marlowe/Sable/Griggs would run via Agent-tool subagent dispatch. This
account's own Caption Loop (Harlow/Flint) trigger's prompt documents that this
hangs 15-40+ minutes with zero output inside a scheduled routine session --
confirmed by a prior diagnostic, not theoretical. The updated prompt performs
every persona inline via explicit perspective-switching instead, the same
proven pattern Caption Loop and AppSec CVE Reviewer already use, and inlines
the actual standards text since `.claude/agents/*.md` is gitignored and does
not exist in a fresh remote clone.

Added a STEP 0 (ensure clean start on main, fix a detached HEAD before any
edits) not in the original design, directly motivated by a failure just
observed in AppSec CVE Reviewer's same-day run (see below).

Next fire: Friday 2026-09-25 15:00 UTC.

## URGENT, unrelated: AppSec CVE Reviewer (daily KEV pipeline) failed today

Discovered while investigating the above. `trig_01QS6sm2WZe1crAsB5fpFQJi`
fired 2026-09-19T17:09Z, ran 11 minutes, **status FAILED**.

Root cause, from the run log: the sandbox started on a **detached HEAD**
several commits behind `main` (this session pushed heavily throughout the
day). The routine's own recovery attempt (`git checkout main` ->
`git stash -u` -> `git stash pop`) produced merge conflicts across every
`cve/*.html` file. Two Claude Code auto-mode classifier denials correctly
blocked destructive recovery attempts (`git checkout -- cve/` with the only
backup already dropped). The run then hit **the org's monthly Claude spend
limit** while still fighting the conflict and ended without committing.

**Verified the real repo is unaffected:** `pending_review.json` still shows
both pending CVEs (`CVE-2025-39964`, `CVE-2026-53266`) as `include_on_site:
false`, `kev-data.json` still has 227 entries (not 229, confirming the
sandbox's in-progress edits never reached origin/main), `git status` on a
fresh clone is clean. Nothing corrupted -- the only cost is that today's 2
CVEs did not get published and the routine will likely repeat this exact
failure tomorrow (17:00 UTC) unless fixed, since it has no equivalent of the
STEP 0 guard just added to AI Vuln Intel Reviewer.

- [x] **STEP 0 fix applied to AppSec CVE Reviewer** 2026-09-20T00:55:35Z, after
      Robert confirmed. Update diffed programmatically against the original
      before sending: every line outside the new STEP 0 block is byte-identical
      -- approval logic, publish pipeline commands, and commit rules untouched.
      Next run 2026-09-20T17:08:46Z is the first real test.
- [x] **Spend limit raised by Robert** 2026-09-20.

## Backlog — added 2026-10-03

- [ ] **Store favicon.** `store/store.html` uses `/favicon.ico`, while the other pages use the blue "F" SVG. Robert likes the store tab icon as-is, so keep it unless that changes.
- [ ] **CISM quiz weights on Nov 3, 2026. Source unverified, do not implement yet.** ISACA confirms the outline is updated effective 3 Nov 2026, but the new domain percentages (18/20/33/29 from a press-release summary) are not verified against a primary ISACA source. Before Nov 3: capture the ISACA URL and published weights, then update `cism-quiz.html` (lines 626-629 and the `domains` map near line 808) and drop the dated note.
- [ ] **Newsletter form (10 pages).** The beehiiv form sends the email as a `?email=` query parameter. Needs the embed snippet from the beehiiv dashboard.
- [x] **CISSP quiz (done 2026-10-03)** — weights now 16/10/13/13/13/12/13/10 to match the ISC2 outline effective 2024-04-15.

## Em-dash voice pass — 2026-10-19

Baseline: 7,463 em-dashes in 766 HTML pages; ~5,600 come from generators/data. Robert chose phased.

Phase 1 (rule-based, generators + HTML together so regeneration doesn't undo it):
- [x] `<strong>Label</strong> — text` → `Label: text` (~859)
- [x] `<title>`, og/twitter title, JSON-LD headline: dash → ": " (" - " if left side already has a colon)
- [x] meta/og/twitter description: dash → ": " after a short label, ", " after a full sentence (~871)
- [x] Same literals in generators (build_practice_tests_hub, generate_guides, generate_quiz_pages,
      inject_seo_questions, lib/ai_vuln_pages, generate_cve_pages, generate_roadmaps,
      generate_comparisons, generate_wstg_pages)
- [x] Verify: re-run an offline generator, diff shows no dash regressions; self-QA; spot screenshots
- [ ] Pre-push review (security-review, AppSec, Content Editor), push

Phase 2 (later, by section, hand-rewritten): the ~5,230 mid-sentence prose dashes + data/*.json + blog markdown.

Phase 1 review (2026-10-19): 2,272 dashes removed (7,463 plus 147 double-escaped -> 5,338 left in HTML). 20 mid-sentence bold
phrases deliberately skipped (Phase 2). Generators + data/ai-vuln-content.json fixed at source; verified
by regenerating 8 offline generators in a scratch copy: transform then finds 0 remaining Phase 1 cases.
inject_seo_schema.py quiz-name split now handles ": " as well as the old dash.
Found and fixed a live bug: 49 pages showed a literal "&mdash;" in <title>/og/twitter titles
(html_head double-escaped "&mdash;" to "&amp;mdash;").

### Phase 2 batch 1 — 2026-10-19
- [x] Boilerplate repeated on 5+ pages (51 phrases): CyberFolio CTA, link-list "Name — desc", CVSS badges,
      planner/subscribe price buttons, cert heatmap + focus lines, roundup RSS/KEV/curation lines, quiz
      disclaimer, store trust/bundle lines. Fixed in HTML + generators (cert, cve, roadmaps, threat roundup,
      cert blog posts, injectors). Regenerated 10 generators in a scratch copy: 0 phrases return.
- [x] Stale figure fixed on 66 cert pages: "3,150+ questions across 66 certifications" -> "10,500+ ... 68"
      (matches practice-tests.html hub). The literal is hardcoded in generate_cert_pages.py and will drift again.
- Result: 2,025 removed, 3,313 left.

Phase 2 rule for later batches: do NOT rewrite quoted third-party text (AI roundup excerpts, attributed
quotes, CVE descriptions from CISA/NVD). Only FixTheVuln's own copy.
Content Editor extension: also leave alone CISA KEV fields (vulnerabilityName, shortDescription,
requiredAction), NVD/vendor advisory text, third-party article/paper titles used as link text, vendor
exam-objective wording, and anything in <code>/<pre>. Our own intro/summary sentences are fair game.
Next batches by section: certs/cve/comparisons/store/wstg/practice-tests (small), then root guides,
roadmaps, blog (largest).

- [x] **Bundle "~30% off" copy (done 2026-10-20: "Multi-cert bundles save 25% or more").** All-format career bundles save 45-48%, so "up to 29%" would understate them. Actual savings vs $5.99/cert from worker
      CP_PRICING: 2 certs 25%, 3 certs 28%, 4 certs 29%. Accurate options: "Save up to 29%" or "25% to 29% off".
      On 7 store pages (aws, cisco, comptia, google-cloud, microsoft, offensive-devops, security-governance).
      Route through the gate with Revenue Guardian.
- [x] **(2026-10-21: worker + store.js PRODUCT_BUNDLE_PRICING, $13.47 single-format / $35.97 all-format, tests/test_store_pricing_parity.py) Productivity Bundle "Save 25%" badge looks wrong (Robert's call, checkout pricing).** store.js shows
      "3 planners · Save 25%", but the worker prices 'lifestyle-bundle' via PRICING[variant] like a single
      planner: $5.99 (standard) or $15.99 (bundle variant) for 3 planners. Neither matches 25%. Decide the
      intended price, then fix worker + badge together through the gate.

### Phase 2 batch 2 — 2026-10-20
- [x] ai-vulnerabilities, comparisons, practice-tests, store, wstg, cve/comparisons index headers: 0 own-copy
      dashes left (fixed in data/ai-vuln-content.json, data/cert-comparisons, and 4 generators too).
- Left: blog 2,172, root guides 529, roadmaps 487.

### Phase 2 batches 3-4 — 2026-10-20
- [x] Batch 3 roadmaps (487): generate_roadmaps._dash_to_parens at render time; nested-paren topics (32) use ". " instead.
- [x] Batch 4 root pages (529 -> 13): quiz taglines/cards "Quiz: N Questions" (rule), then 387 hand decisions
      (spec in session scratchpad), mirrored into generate_guides.py, generate_quiz_pages.py, quiz data JSON.
      13 left on purpose: ai-ide-mcp-disclosures advisory text (third-party), "[un]prompted 2026 — ..." talk
      title, OWASP table empty-cell placeholders (3), one HTML comment.
- [x] (2026-10-22) mlsecops.html/threat-hunting.html drift: both pages were hand-edited many times since
      their original generation (dark mode, FAQ schema, canonical URL fixes, new content) with generate_guides.py
      never kept in sync. Deleted their PAGE_CONFIGS entries (dead code; `'related'` cross-links from other
      pages to these two files are untouched and still correct). Verified by regenerating in a scratch copy:
      both pages are now fully untouched by the script. owasp-llm-top10.html stayed in sync separately, in the
      2026-edition-restore commit.
- [x] (2026-10-23) Fixed the remaining 9 drifted PAGE_CONFIGS pages. Audited each (not just line counts):
      ai-security-careers.html's entry held an entirely superseded title/description/FAQ (pre-dates the
      "Roles That Didn't Exist Last Year" rewrite); prompt-injection.html's entry was missing the whole
      hand-added "2026 Update: AI IDE & MCP Attack Surface" section; owasp-llm-top10.html's entry (despite
      being deliberately corrected during the 2026-edition restore) had drifted from the live page in ways
      that predate the later ranking-wording fix (2683fe48, which correctly kept both files in sync for the
      lines it touched) — the generator's copy still said "holds the top spot for the third edition running"
      and "supply chain risks" where the live page had already dropped both, plus injected cross-link tiles
      never mirrored back. Drift's origin wasn't tracked down (not in `git log -S` for that phrase). The
      other 6 showed the same pattern (injector-script output + hand edits the generator never learned about).
      Confirmed no other script imports generate_guides.py or calls PAGE_CONFIGS (same as the mlsecops/
      threat-hunting fix), so deleted all 9 remaining dead entries, which empties PAGE_CONFIGS entirely.
      `main()` now generates 0 pages but still calls `generate_ai_vuln_pages.main()` for the AI-VULN-GRID
      markers (that part reads/writes the live HTML directly, independent of PAGE_CONFIGS, and is unaffected).
      Verified via scratch-copy regeneration: all 9 pages are now fully untouched by the script. Helper
      functions (`build_related`, `build_quiz_links`, `generate_page`) are now dead code too; left in place,
      not in scope here.
- Left: blog 2,172.

### Phase 2 batch 5 (final) — 2026-10-20
- [x] Blog: AI roundups (byline "Source: X, date", GHSA "(owner/repo)", titles, feed-excerpt dashes -> ", " exactly as
      aggregate_ai_security_news._clean_html already does for new roundups); threat roundups ("CVE-…: Name" headings,
      3 template sentences in generate_threat_roundup.py); study guides (379 week items via _dash_to_parens in
      generate_cert_blog_posts.py); 91 hand decisions + 8 "isn't X, it's Y" rewrites; blog index/feed/blog_metadata
      titles and the stale "released during RSA" excerpt.
- [x] Quiz data (fetched at runtime by quiz-engine.js): 177 options "Term: description" (answers are int indexes),
      168 explanation/question decisions + 2 hand rewrites. Edited as raw string replacements, formatting untouched.
- [x] Content Editor follow-ups from batch 4: 5 "not X, it's Y" sentences, 4 double colons, template CTA wording
      ("Free blank templates or $4.99/mo for pre-filled intelligence...").
- Result: 19 em-dashes left site-wide, all deliberate (third-party titles/advisory text, table placeholders, one comment).
- [x] (2026-10-21, ISC2 cissp-salary page: NA median $150,000, global $127,000) Unsourced figure to verify (Content Editor): cybersecurity-job-trends.html "CISSP holders earn an average of $150,000+".
- [x] (2026-10-21, now "At least 11 U.S. states") Figure to verify (Content Editor): blog/ai-notetaker-security-risk.html "California, Illinois, and 9 other U.S. states
      require all-party consent". Published counts vary 11-13 depending on how MI, CT and OR are treated.

- [x] Batch 5 polish (2026-10-20): roundup bylines end with a period (old posts + aggregator), SecAI 40% sentence,
      2 quiz sentences, 3 more "not X, it's Y" sentences in editorial posts.

### Store delivery fix — 2026-10-21
- [x] R2 had no lifestyle-bundle files in any format (buyers paid, got nothing), and no lifestyle product had an
      adhd_dark (except business-templates) or 4-format zip. Worker now delivers lifestyle-bundle as its 3
      planners (expandPurchasedItems) and refuses formats missing from R2 (PRODUCT_FORMATS); store.js shows
      "Not in this format". Productivity Bundle: $13.47, Standard/ADHD/Dark only.
- [x] (2026-10-22) Checked with Robert: zero lifestyle-bundle purchases ever went through. The flag was
      precautionary (the product was listed/purchasable for ~8 months with no R2 files behind it), not
      based on a confirmed sale. No buyers to make whole.
- [x] Spot-check that cert planners really have all five formats in R2 (only lifestyle products were checked).
      Done 2026-10-22: full inventory, not a spot-check — all 65 certs x 5 files = 325 checks, 0 missing.

### Store + figures follow-ups — 2026-10-21
- [x] Education planners checked in R2: teacher/student have all 4 single formats, no 4-format zip; adhd-student-planner
      has only Standard and Dark. Added to PRODUCT_FORMATS (worker + store.js).
- [x] Lifestyle/education format pickers: 4-Format Bundle removed, "/planner" labels, ADHD-Dark availability notes;
      a format remembered from another page falls back to Standard on pages that don't offer it.
- [x] FAQ copy: lifestyle/education "what do I get" no longer quotes cert page counts; store.html 4-Format FAQ scoped.
- [x] CISSP "$135K-$165K average" (6 places) -> ISC2 North America median $150,000 / global $127,000, linked.
- [x] (2026-10-22) CISM/OSCP/AWS figures on best-cybersecurity-certifications.html sourced:
      ISACA states $149,000+ for CISM (isaca.org/credentialing/cism, no year given); ZipRecruiter via
      direct fetch puts OSCP at $119,895 average / $96K-$141K range as of July 2026
      (ziprecruiter.com/Salaries/OSCP-Salary); AWS Security Specialty has no verifiable salary figure from
      AWS, ZipRecruiter, CertMag, PayScale or Infosec Institute (3 fetch attempts, all 403/404) so the
      specific dollar claim was cut. Two adjacent unsourced claims in the AWS section (role-salary range,
      "outperforming Azure/GCP") also softened since they sat right next to the fix.
- [x] (2026-10-22) Cert store FAQ "55-75 pages" / "100+ pages" claim verified by downloading and measuring
      7 real planner PDFs from R2 (pdfinfo): Standard 62-79 pages, ADHD-Friendly 116-118 pages. Updated to
      "60-80 pages" / "115+ pages" to match. Applied to all 7 cert vendor store pages.
- [x] (2026-10-22) R2 spot-check of ALL 65 cert planners (not just a sample): checked all 5 files per cert
      (standard/adhd/dark/adhd_dark/bundle.zip) = 325 checks. 0 missing. Unlike lifestyle/education, every
      cert planner has every format.

### Tech-debt cleanup — 2026-10-23
- [x] generate_sitemap.py CONTENT_DIRS was missing "wstg" and "practice-tests" (26 live pages never made
      it into sitemap.xml despite reconcile-sitemap.yml running this script daily). Added both; sitemap.xml
      791 URLs (was 765). GUIDE_PAGES was missing ai-agent-security.html, genai-data-security.html, and
      agentic-skills-top-10.html (misclassified "Other Pages" 0.7 instead of "Security Guides" 0.8 priority;
      the third one wasn't in the tech-debt.md note, found while auditing the same set). llms.txt/
      llms-full.txt regenerated too (independently stale, same pages missing there as well).
- [x] requirements.txt added (Pillow, reportlab, requests) so security-audit.yml's pip-audit step checks
      something instead of silently no-oping with no file present.
- [x] 7 of 9 bare `except Exception:` blocks now print a warning to stderr before their existing fallback
      (update_sitemap.py, generate_sitemap.py, audit_pages.py x2, inject_error_reporter.py, health_check.py,
      fetch_kev.py). Left generate_linkedin_posts.py/create_hero.py's font-path-probing ones alone:
      those try multiple paths by design, most "failing" routinely, so logging every miss would be noise.
- [x] Found + fixed while regenerating llms-full.txt: generate_llms_txt.py's ABBREVIATIONS mapped standalone
      "ec" straight to "EC-Council", so ec-council.html rendered as "EC-Council Council" (loop re-processed
      "council" separately). First fix (3774c40c) replaced "ec" with the combo key "ec-council", which broke
      9 other EC-Council pages (ec-ceh/chfi/cnd.html x3 each) that depend on the single-word "ec" plus a
      separate cert-code lookup — they started rendering "Ec CEH" instead of "EC-Council CEH". Caught before
      Content Editor flagged it; fixed in a39f9677 by keeping both keys (the combo check runs first in the
      loop, so "ec-council" intercepts the 2-token case and "ec" alone still covers the 3-token titles).
      Verified all 10 ec*.html pages render correctly.
- [x] Practice-tests vendor-page timestamp (the 5th item, P1, was 20 weeks open): flagged the conflict
      between tech-debt.md's suggested fix (remove the timestamp) and CLAUDE.md's documented policy (keep
      it, auto-generated pages do). Robert confirmed: regenerate the date, don't remove it. Verified via
      scratch-copy regen first (every page's diff was exactly the one timestamp line, 0 content drift),
      then ran `generate_practice_test_pages.py` for real across all 13 vendor pages.

## 2026-10-31 Store price reposition (Hormozi anchor + "too cheap" perception) — PLAN, awaiting go-ahead

Decision (Robert, 2026-10-31): raise singles + add a high-priced anchor. Exact numbers still to confirm.
Reference: Hormozi LinkedIn post (tier spacing + "always have a very expensive item"). No sales yet, so no A/B possible; judgment call.

Proposed: single $5.99 -> ~$9.99; 4-format bundle $15.99 -> ~$19.99 (still ~50% off $39.96); career-path tiers rescaled so
the ladder stays monotonic; one new anchor ($49-79 full-library/vendor pack) on store.html.

- [ ] Confirm final numbers + anchor contents (what does the $49-79 item actually deliver? needs R2 files)
- [ ] worker PRICING / CP_PRICING / PRODUCT_BUNDLE_PRICING + store.js mirrors + store.html cards; tests/test_store_pricing_parity.py
- [ ] "$5.99/$15.99" copy on ~209 pages (certs/, roadmaps/ ~66 each, 1 promo per tool/guide page, js/, scripts/ generators): fix at the generator, regenerate, don't hand-edit
- [ ] "Save X%" badges, JSON-LD/offers, llms-full.txt, Stripe checkout copy, cache-bust ?v=
- [ ] Existing buyers/open Stripe sessions unaffected (price_data is server-side per session) — verify
- [ ] Gate: Revenue Guardian + /pre-push-review; self-qa.sh; one deploy
- 2026-10-31 decisions: single $9.99, 4-format bundle $19.99, anchor = "CompTIA Complete" $59 (14 certs x all 4 formats, delivered as 14 `__bundle` zips via expandPurchasedItems, no new R2 files).
  Needs a forced-variant field on PRODUCT_BUNDLE_PRICING (today it accepts any client variant at the flat price). Vendor packs feasible: comptia 14, microsoft 12, aws 8 (rest <=5, skip).

### 2026-10-31 build result (uncommitted, not pushed)
Final: single $9.99, 4-format bundle $19.99, career paths 2/3/4 certs $14.99/$21.99/$28.99 single and $21.99/$31.99/$41.99 all-format,
Productivity Bundle $22.47, packs CompTIA Complete $79 (14), Microsoft Complete $69 (12), AWS Complete $59 (8), bundle-only via PRODUCT_FORMATS.
- [x] worker + store.js tables, pack cards (hub featured + vendor pages via forVendor), 209 pages' copy, generators, cert-costs data/calculator
- [x] tests: parity (price tables + packs), worker checkout tests (12 pass), self-qa.sh pass, headless render checked store/comptia/aws
- [x] cache-bust: store.js v14->v15 (10 store pages), quiz-engine.js v1->v2 (68 quizzes + generate_quiz_pages.py)
- [ ] /pre-push-review (Revenue Guardian), then deploy worker (wrangler) BEFORE/with static push so site and checkout prices never disagree
- [ ] Known gap: a pack plus an individual cert it contains can both sit in the cart (career paths have an overlap guard, packs do not)
- [ ] Review 2026-11-30: did packs cannibalize $19.99 bundles? ($79 pack beats buying 4 CompTIA certs at $19.99)
- 2026-10-31 revision (Robert): 4-format bundle $19.99 -> $24.99; career-path all-format bundles +$5 (2/3/4 certs = $26.99/$36.99/$46.99). Singles, single-format paths, Productivity Bundle and packs unchanged. Tests + self-qa pass.
- 2026-10-31 follow-up #3 (Robert chose "remove the limit"): purchase record now spans purchased_items, purchased_items_2, ... (<=480 chars each, whole ids) so a 20-line cart no longer exceeds Stripe's 500-char metadata cap; /verify and webhook read via readPurchasedItems; checkout returns a generic error instead of Stripe's raw message. 20-line cart cap kept (abuse limit). Remaining open: #2 email size, #4 pack/cert overlap, #5 success.html names, #6 skill docs.
