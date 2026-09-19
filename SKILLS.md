# FixTheVuln — Role Contract

This file defines the review roles that must sign off on non-trivial changes to FixTheVuln before they are pushed to GitHub. Each role is implemented as a Claude Code subagent in `.claude/agents/` and invoked via the Agent tool.

## Why this exists

FixTheVuln is a cybersecurity education platform. Its content (CVE writeups, cert comparisons, quiz answers, study material) is consumed as authoritative by readers preparing for certifications or patching real systems. A factual error in a CVE writeup can get someone fired; a wrong CWE mapping undermines the brand of a security-education site. Add to that: an LLM-generated publishing pipeline, RSS aggregation from public sources, a Stripe store, and quiz-feedback telemetry — all of which need separate, focused review lenses.

## Roles

| Role | Subagent | Primary concern | When to invoke |
|---|---|---|---|
| **COO** | `coo` | Content strategy, SEO, publishing cadence, cross-project consistency, cost discipline | New content plans, pipeline changes, marketing triage, scope decisions |
| **AppSec** | `appsec` | LLM-output validation, RSS/XML safety, ReDoS, XSS in generated pages, store worker hardening | Any change touching: scripts that write HTML/JSON, RSS parsers, quiz-feedback worker, store worker, regex patterns |
| **Content Editor** | `content-editor` | Factual accuracy of CVE/CWE/CVSS details, cert exam claims, tool/vendor facts, citation quality | Any change touching: CVE writeups, cert comparisons, quiz questions, blog posts, roadmaps, tool recommendations |
| **Tech Debt Auditor** | `tech-debt-auditor` | Generator rot, stale content drift, cache-bust misses, llms.txt/sitemap sync gaps, script duplication, worker cost drift | Mondays or ad-hoc via `/tech-debt-audit`. Writes date-stamped findings to `tasks/tech-debt.md`. Not a gate: it never blocks a push |

## Mandatory gates

- **Before `git push`:** run `/pre-push-review` (defined in `.claude/commands/`, not `.claude/skills/`) — chains the native `security-review` skill + AppSec subagent + Content Editor (if content changed).
- **Daily AppSec CVE Reviewer trigger** (10 AM PDT) auto-publishes CVEs. When that trigger ships broken content, this review gate is your only line of defense before it compounds across the site.
- **Never skip the Content Editor gate on CVE/cert/quiz changes.** An LLM-introduced factual error is the highest-impact failure mode for this project.

## What "good review" looks like

Each subagent returns a structured verdict:

```
VERDICT: approve | approve-with-fixes | block
FINDINGS: <numbered list; severity + file:line + what + why>
REQUIRED FIXES: <list; empty if approved>
NOTES: <optional context>
```

**The gate blocks on any P0 or P1 finding, whatever verdict string carries it.**
A `block` verdict is not the only stop condition, and reading it that way is the
live failure mode: on 2026-09-19 Content Editor returned `approve-with-fixes`
on the AI IDE tracker while reporting two P1s, one of which put CISA's
catalog-add date under a column headed "Published", eight weeks off the real
date. Treating that verdict as passing would have shipped it.

`approve` and `approve-with-fixes` with only P2/P3 findings proceed. Anything
else: fix, then re-run the whole gate, not just the reviewer that objected.

Severity follows the priority framework in `../CLAUDE.md`: P0 security, P1
production-down, P2 revenue, P3 user-facing bug, P4 performance/DX, P5
features/content. Content errors in published CVE, cert, or quiz material are
P0 here, not P3 — see Escalation below.

## Verify what a reviewer tells you

A subagent report is model output, not evidence. Before acting on a finding,
reproduce it; before dismissing one, check the file. Both directions bit on
2026-09-19:

- AppSec reported a P0 ReDoS in a subject-extraction regex. Measured before
  accepting: a 144-char hyphen chain took 0.529s and scaled ~1.75x per 4 tokens.
  Real, and the fix was verified to change none of the 88 stored extractions.
- Content Editor reported a CVSS provenance problem. Confirmed against the live
  NVD API, which showed 11 of 12 displayed CVEs carried no Primary rating at all.
- Twice a reviewer reported something already fixed while it was running. Check
  current file state rather than re-fixing.

Re-running the collector or generator after a fix is not optional. A finding
that only exists in prose has not been closed.

## Escalation

If two reviewers disagree: AppSec wins on security, Content Editor wins on facts, COO wins on scope/strategy. Content errors in published CVE writeups are P0 — treat them like security bugs.

## Not in scope for these roles

- Detailed architecture (that lives in `CLAUDE.md`).
- Task execution skills like `deploy`, `publish-cves`, `batch-generate` (those live in `.claude/skills/`).
- CI-level checks (pre-commit hooks, gitleaks). Wire those separately in `settings.json` when ready.
