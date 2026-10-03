# AppSec Review — 2026-10-03

**Reviewer:** Robert Flores, CISSP  
**Review Date:** 2026-10-03  
**CVEs Reviewed:** 2  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 2     | CVE-2026-102490, CVE-2026-102489 |
| High     | 0     | — |
| Medium   | 0     | — |
| Low      | 0     | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-102490 | Zammad GmbH | Critical | Improper Privilege Management (LPE → Root) |
| CVE-2026-102489 | Zammad GmbH | Critical | Session Fixation (Remote Code Execution) |

---

## Trend Analysis

This batch represents a fully chained two-stage attack against Zammad, a widely-deployed open-source helpdesk and CRM platform. CVE-2026-102489 provides the remote entry point via session fixation, enabling unauthenticated attackers to execute code as the zammad service user; CVE-2026-102490 then escalates those privileges to root through improper privilege management. The deliberate chaining of these two vulnerabilities — both carrying CVSS 9.8 and added to KEV on the same date — is consistent with a coordinated threat actor campaign targeting helpdesk infrastructure, which commonly processes sensitive customer data and internal tickets. CISA's tight 3-day remediation window (due 2026-10-05) under BOD 26-04 underscores the urgency. Organizations running Zammad should treat this as an emergency patch given the active exploitation and full remote-to-root potential.

---

## Blog Post Candidates

1. **"Chained to Root: How CVE-2026-102489 + CVE-2026-102490 Turn Zammad Into a Full Compromise"** — Deep dive into the two-stage exploit chain, how session fixation enables RCE, and how organizations can detect exploitation attempts.

2. **"Why Helpdesk Software Is the New Perimeter: Lessons from the Zammad KEV Chain"** — Broader trend analysis on threat actors targeting internal tooling (Jira, Zammad, Zendesk) as initial access vectors into corporate networks.

3. **"CISA BOD 26-04 in Practice: Responding to a 3-Day Patch Deadline"** — Practical guide for security teams triaging and patching under BOD 26-04's compressed timelines, using this Zammad pair as a real-world case study.

---

## Newsletter Snippet

**CISA adds Zammad chain exploit to KEV — patch by October 5th.** Two critical vulnerabilities in Zammad GmbH's open-source helpdesk platform were added to CISA's Known Exploited Vulnerabilities catalog on October 2nd with a mandatory remediation deadline of October 5, 2026 under BOD 26-04. CVE-2026-102489 (session fixation, CVSS 9.8) allows an unauthenticated remote attacker to achieve code execution as the zammad service account, while CVE-2026-102490 (improper privilege management, CVSS 9.8) escalates that foothold to root. The two flaws are designed to be chained, making the combined attack fully remote and unauthenticated.

Federal agencies and any organization running Zammad should apply vendor patches immediately. If patches cannot be deployed within the window, CISA guidance requires either implementing compensating controls or discontinuing use of the product. Security teams should also audit Zammad logs for session anomalies and privilege escalation indicators, as active exploitation has already been confirmed in the wild per CISA's KEV addition.
