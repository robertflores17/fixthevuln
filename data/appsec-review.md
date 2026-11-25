# AppSec Review — 2026-11-25

**Reviewer:** Robert Flores, CISSP (FixTheVuln AppSec Reviewer)
**Date:** 2026-11-25
**CVEs Reviewed:** 3
**Source:** CISA KEV (dateAdded: 2026-11-24)

---

## Severity Breakdown

| Priority  | Count | CVEs |
|-----------|-------|------|
| Critical  | 2     | CVE-2026-131914, CVE-2026-132165 |
| High      | 1     | CVE-2026-132224 |
| Medium    | 0     | — |
| Low       | 0     | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vuln Class |
|--------|--------|----------|------------|
| CVE-2026-132224 | Optimizely | High | External Control of Critical State Data / JS Supply-Chain Injection (CWE-642) |
| CVE-2026-131914 | Idunno (Blowdart) | Critical | Deserialization of Untrusted Data / Unauthenticated RCE (CWE-502) |
| CVE-2026-132165 | Drupal | Critical | Unauthenticated RCE via Install Script (Fail-Open) |

---

## Trend Analysis

This batch is notable for the breadth of attack surface it touches. Two of the three CVEs enable unauthenticated remote code execution — one through classic .NET deserialization (a vulnerability class still turning up in EoL libraries years after Mandiant and others first flagged it in legacy ASP.NET stacks), and one through an open installer endpoint, a Drupalgeddon-era pattern that continues to resurface in CMS deployments that skip hardening checklists. The Optimizely finding is the most operationally interesting: rather than direct code execution on a server, it enables attacker-controlled JavaScript to ride Optimizely's own CDN into the browsers of visitors on affected customer sites — a supply-chain injection vector with significant downstream reach that may be underweighted purely on CVSS score. CISA's tight 3-day remediation window (due 2026-11-27) for all three reflects the confirmed in-the-wild exploitation noted in the KEV addition, and the combination of a CMS RCE, an EoL library RCE, and a SaaS JS injection in a single batch suggests threat actors are actively broadening their initial-access toolkit.

---

## Blog Post Candidates

1. **"Install.php Still Kills: Drupal CVE-2026-132165 and Why CMS Hardening Checklists Matter"** — Covers the recurring pattern of accessible install scripts as an RCE vector across Drupal's history (Drupalgeddon through present), with practical hardening steps (remove/rename install.php, server-side block, monitoring).

2. **"Supply-Chain JS Injection via SaaS Platforms: Lessons from CVE-2026-132224"** — Explores how third-party script providers (A/B testing, analytics, tag managers) represent a high-impact, often-overlooked attack surface; includes Subresource Integrity (SRI), CSP, and vendor security review guidance.

3. **"Deserialization Is Still Alive in Legacy .NET: CVE-2026-131914 and EoL Risk Management"** — Examines why deserialization vulnerabilities persist in EoL/.NET libraries, how to detect exposure in dependency inventories, and when "just migrate" is the only viable remediation.

---

## Newsletter Snippet

CISA added three actively exploited vulnerabilities to the Known Exploited Vulnerabilities catalog this week, all with a 3-day federal remediation deadline (due 2026-11-27). The most severe are a deserialization RCE in Idunno AntiCsrf (CVSS 9.8, unauthenticated, now EoL) and a Drupal Core installer bypass that lets unauthenticated attackers execute arbitrary code by triggering a site reinstall via install.php — both warrant emergency patching or service discontinuation. A third vulnerability in Optimizely Web Experimentation (CVSS 8.7) is lower on the CVSS scale but potentially high in real-world impact: exploitation allows attacker-controlled JavaScript to be injected into Optimizely's CDN-hosted assets and silently executed in the browsers of visitors to affected customer sites.

If your organization uses any of these products, treat this as an active incident response situation, not a standard patch cycle. Verify that install.php is inaccessible on all Drupal instances, check Optimizely's incident report and status page for indicators of compromise, and audit whether any applications still reference the Idunno AntiCsrf library — if so, plan an accelerated migration. All three are confirmed in-the-wild exploits; CISA's 3-day window reflects genuine urgency.
