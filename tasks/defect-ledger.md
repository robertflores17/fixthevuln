# FixTheVuln blog pipeline: defect ledger (Atlas)

Owner: Atlas (`cto`). Added 2026-10-25 at Robert's request. Same row format and two-occurrence rule as
`linkedin-posts/tasks/defect-ledger.md`. Atlas diagnoses and decides; fixes go through Claude and `/pre-push-review`.

Scope: `publish-blog.yml` (Tue), `ai-trend-roundup.yml` (Fri), `publish_editorial.py`, `aggregate_ai_security_news.py`.
Not in scope: post copy, CVE/cert facts (Content Editor), product code (Rook).

## Health numbers (pull weekly with `gh run list` + newest `blog/*roundup*.html` `datePublished`)

| Number | Baseline 2026-10-25 | Target |
|---|---|---|
| Days from aggregator draft to live post | 4 (Fri draft, Tue publish) | 0 |
| Days since newest roundup went live (measured Sat/Sun) | 5 (10-16 roundup, live 10-20) | <= 2 |
| Draft items covered vs. window end | window ends Fri, post live next Tue | same day |
| Unpublished drafts older than 1 day | 2 (10-20, 10-23) | 0 |
| Off-topic items per digest (Content Editor count) | 8 of 8 (10-20), ~3 of 20 (10-23) | 0 |
| Workflow failures, last 8 runs each | 0 / 0 | 0 |
| Aggregator source warnings per run | arXiv cs.CR: 3 (parse, doctype, >1MB) on 2026-10-25 local run | 0 |

## Ledger

| Week | Item | Category | What happened | Root cause | Status |
|---|---|---|---|---|---|
| 2026-10-25 | AI roundup | delivery-lag | Friday draft published the following Tuesday; newest roundup always 10+ days behind window start | Two workflows, publish only in Tuesday job | Fixed: Friday job now runs `publish_editorial.py` + `generate_llms_txt.py`. Verify at next retro (10-30 run live same day?) |
| 2026-10-25 | AI roundup | duplicate-window | Manual `workflow_dispatch` on 10-20 created a second draft (10-13..10-20) beside the scheduled 10-16 one | Manual run after Tuesday publish; dedupe moved items into the extra draft | Not a defect (content real, published). Watch for repeat |
| 2026-10-25 | arXiv cs.CR source | source-flaky | Feed returned unparseable / doctype / >1MB response; roundup 10-23 shows arXiv items anyway | Unknown: needs the Actions log for 10-23, not a local run | Open: diagnose from `gh run view 40001527270 --log` |
| 2026-10-25 | AI roundup generator | relevance-filter | All 8 items of the 10-20 digest and several in 10-23 sit under "Prompt Injection & LLM Security" but are off-topic (a game, an obituary, a music video). Content Editor P2 | Keyword/category filter in `aggregate_ai_security_news.py` too loose | Fixed 2026-10-25: Willison feed now has `filter_keywords` (measured on the 14 Willison items in the merged post: 14 -> 4 kept, 3 clearly security). Verify on the 10-30 digest |
| 2026-10-25 | AI roundup generator | text-defects | "1 sources" pluralization; `&amp;#x27;` double-escaped apostrophe; arXiv "Announce Type: new Abstract:" boilerplate left in excerpts. Content Editor P2/P3 | Escape applied twice; no singular/plural handling; no boilerplate strip | Fixed 2026-10-25: `_clean_html` uses `html.unescape`, strips arXiv prefix, em-dash after decode; source count pluralized. Tests added |
| 2026-10-25 | AI roundup | publish-gate | Friday job now publishes with no human step; escaping is the only control (AppSec P3) | By design after delivery-lag fix | Fixed 2026-10-25: end-to-end hostile-item test (parses real tags/attrs; mutation-checked) |
| 2026-10-25 | Late posts | dating | 10-20 and 10-23 posts carry datePublished 10-25 | Backlog from Tuesday-only publish | Closed by delivery-lag fix; will not recur |
| 2026-10-25 | PHP post (hand-written) | misattribution | Draft said Willison "reports exploits circulating" from a search-result summary; round-1 reviewer then wrongly said he does not; committed text said "no source reports exploitation". Caught pre-push by second review | Facts taken from a search summary, not the primary page; reviewer also read from memory. Fixed by quoting Willison verbatim after a direct page read | Closed for this post. Rule: quote the primary page verbatim before writing any exploitation-status line. Second occurrence earns a checklist step |
| 2026-10-25 | Feeds | parse-failures | Local dry-run: Project Zero `unclosed CDATA`, CISA `no element found`, arXiv/NIST parsed=0 | Possibly the 2,000,000-byte `MAX_FEED_BYTES` cap truncating large feeds before parse; unconfirmed, local run only | Open: read the 10-30 Actions log (cloud check counts arXiv warnings). Two occurrences in Actions logs earns a fix |
| 2026-10-25 | Threat roundup | window-overlap + lag | 14-day lookback since Feb made each "This Week" post repeat ~half the last one (6/11, 5/14); titles spanned 2 weeks. First fix (7-day window) was caught pre-push: it would have lost 8 CVEs because KEV entries reach kev-data 1-3 days after `dateAdded` | Window on CISA's date, but site ingests later; overlap was masking the lag | Fixed 2026-10-25: 14-day lookback + skip CVEs already in an earlier roundup's `###` headings; quiet week skips; title starts at oldest included CVE. Verify at the 10-27 Tuesday run: no repeats vs 10-20 post, 6 Oct-20 CVEs included |
