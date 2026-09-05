# FixTheVuln — Lessons Learned

## Pattern: [What went wrong] → [What's correct] → [Prevention rule]

_Capture lessons here after any user correction._

### 2026-04-08: KEV pipeline silently broke for 13 days
- **What went wrong:** `fetch-vulnerabilities.yml` pushed `pending_review.json` to PR branches, but the AppSec CVE Reviewer trigger reads from main. PRs were never auto-merged, so pending CVEs accumulated on branches for 13 days without being published. Homepage showed "Updated Mar 26 · Checked Apr 8".
- **What's correct:** Fetch workflow now pushes `pending_review.json` directly to main. No intermediate PR branches — the trigger IS the reviewer, so human-review PRs were redundant.
- **Prevention rule:** Added `check_kev_pipeline_health()` to `audit_pages.py` — flags P1 action item if `lastUpdated` falls >7 days behind `lastChecked` in `kev-data.json`. Also: when designing automated pipelines, verify that every step can actually read the output of the previous step (same branch, same file location).
---

### 2026-06-21: One generator crash blacked out the blog for ~2 weeks
- **What went wrong:** `generate_threat_roundup.py` used `float(v.get('cvss', 0))`. A newly-added KEV entry stored `cvss: null` (key present, value None), so `.get` returned None and `float(None)` raised TypeError. `publish-blog.yml` ran its 10 generators sequentially with no error tolerance, so that one crash aborted the whole job before `publish_editorial.py` — no weekly roundup AND no AI-security roundups published from June 9 to June 21. Every other workflow stayed green, so the only signal was a weekly failure email that was easy to miss.
- **What's correct:** Use `float(v.get('cvss') or 0)` (the idiom already in `fetch_kev.py` and `generate_cve_social.py`). `dict.get(k, default)` only defaults on a MISSING key, never on a present-but-null value. Structurally, each generator in `publish-blog.yml` now runs `continue-on-error: true` with a step `id`, and a final `if: always()` gate publishes what succeeded, then fails the job red and names each crashed step.
- **Prevention rule:** (1) Never trust `dict.get(key, default)` to guard against null — only against missing. For nullable values use `(v.get(key) or default)` or an explicit None check. (2) In any multi-step automation where steps are independent, isolate failures (`continue-on-error` + an aggregation gate) so one crash can't take down the rest, and make the failure loud (red job + named culprit), not silent. Regression test: `tests/test_generate_threat_roundup.py`.
---

### 2026-09-05: Cloudflare's security scanner flagged the site's own working DNS as a vulnerability

**What went wrong:** Cloudflare Security Insights flagged 4 "Dangling A Record" findings (Moderate severity) as vulnerable to subdomain takeover. The 4 IPs were GitHub Pages' own official, currently-active shared IPs (`185.199.108-111.153`) — the site's actual, correct hosting configuration, still serving 200 OK. The scanner's heuristic (other unrelated hostnames also resolve to the same IP) can't distinguish "shared hosting IP legitimately serving your content" from "an abandoned resource someone else could claim," because GitHub Pages (like Netlify, Vercel, Fastly) is multi-tenant by design. Following the scanner's literal "remove this record" recommendation would have taken the live site offline.

**What's correct:** Verified against a full BIND zone export before touching anything — confirmed the flagged IPs matched GitHub's documented custom-domain setup exactly, plus a live 200 response and a real `www` CNAME to `robertflores17.github.io`. Left the records alone. Separately, used the same zone export to find genuinely dead DNS (7 SendGrid records with zero references anywhere in this repo's git history) — a real, safe cleanup, distinguished from the false positive precisely by tracing actual code usage instead of trusting the scanner's verdict either way.

**Prevention rule:** Same standing rule as this file's Bug Bounty Verification Rules, generalized: an automated security scanner's finding is a lead, not a verdict — verify against the actual live configuration (and, for "is this dead code" style findings, the full git history, not just current HEAD) before acting on its recommendation, especially before any change that touches live DNS, and doubly so for the record's own recommended fix if that fix is destructive.

---

### 2026-06-21: GitHub Actions `set -e` aborted a gate step using `[[ ]] && ...`
- **What went wrong:** The new "Fail if any generator crashed" gate used `check() { [[ "$2" == "failure" ]] && failed="$failed $1"; }`. GitHub Actions runs `run:` blocks with `bash -e`. When an outcome was NOT "failure", the `[[ ]]` returned non-zero, so the function returned non-zero, and `set -e` aborted the step — turning the job red even when every generator and the push succeeded (false alarm on every clean run).
- **What's correct:** Use an explicit `if`: `check() { if [[ "$2" == "failure" ]]; then failed="$failed $1"; fi; }`. An `if` whose condition is false returns 0, so the function is `set -e`-safe.
- **Prevention rule:** Under `set -e` (the Actions default), never end a function or step with a bare `[[ cond ]] && cmd` — it returns the test's exit status, non-zero when the test is false. Use an explicit `if`, or append `|| true`. Always exercise a new workflow step once via `workflow_dispatch` before trusting it — self-QA caught this within minutes.
