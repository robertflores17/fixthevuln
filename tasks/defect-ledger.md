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
| 2026-10-25 | AI roundup generator | relevance-filter | All 8 items of the 10-20 digest and several in 10-23 sit under "Prompt Injection & LLM Security" but are off-topic (a game, an obituary, a music video). Content Editor P2 | Keyword/category filter in `aggregate_ai_security_news.py` too loose | Open. First occurrence; fix on second (check 10-30 digest) |
| 2026-10-25 | AI roundup generator | text-defects | "1 sources" pluralization; `&amp;#x27;` double-escaped apostrophe; arXiv "Announce Type: new Abstract:" boilerplate left in excerpts. Content Editor P2/P3 | Escape applied twice; no singular/plural handling; no boilerplate strip | Open. Cheap one-pass fix, batch with relevance filter |
| 2026-10-25 | AI roundup | publish-gate | Friday job now publishes with no human step; escaping is the only control (AppSec P3) | By design after delivery-lag fix | Open: add hostile-title unit test for `_md_text`/`_link` |
| 2026-10-25 | Late posts | dating | 10-20 and 10-23 posts carry datePublished 10-25 | Backlog from Tuesday-only publish | Closed by delivery-lag fix; will not recur |
