# AppSec Review — 2026-11-01

**Reviewer:** Robert Flores, CISSP (FixTheVuln AppSec Reviewer)  
**CVE Count:** 2  
**Review Date:** 2026-11-01

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 0 | — |
| High     | 2 | CVE-2026-118527, CVE-2026-111357 |
| Medium   | 0 | — |
| Low      | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-118527 | Ivanti | High | Predictable Identifier / Arbitrary File Write |
| CVE-2026-111357 | Ivanti | High | Missing Authentication / Privilege Escalation |

---

## Trend Analysis

This batch continues a well-documented pattern of chained Ivanti Connect Secure vulnerabilities — both CVEs are explicitly linked to a third (CVE-2026-104935) forming a three-link exploit chain that moves an attacker from unauthenticated access through file write and into privilege escalation. Ivanti's VPN appliances have been a persistent target since 2024, and CISA's BOD 26-04 specifically calls out this product line for expedited patching timelines (note the seven-day remediation window on CVE-2026-111357, due 2026-11-02). The pattern of predictable identifiers enabling file writes to known paths is a common design flaw in appliance firmware stacks, suggesting the underlying codebase has not been fully audited post-disclosure. Organizations running Ivanti Connect Secure should treat all three CVEs as a single remediation unit and complete forensic triage per CISA's published requirements before re-exposing the appliance to the internet.

---

## Blog Post Candidates

1. **"Ivanti's Three-Link Chain: How CVE-2026-104935, -118527, and -111357 Combine for Full Compromise"** — A technical breakdown of how each vulnerability feeds the next, with a timeline of CISA advisories and patch availability.
2. **"BOD 26-04 in Practice: What the New CISA Patching Directive Means for Network Appliances"** — Explains the directive's seven-day and 14-day windows, forensic triage requirements, and how to build a compliant remediation workflow.
3. **"Why Ivanti Keep Making the KEV List: Appliance Security Anti-Patterns"** — A recurring-vendor analysis examining the architectural and development practices that produce predictable-identifier and missing-auth flaws in VPN/gateway appliances.

---

## Newsletter Snippet

**This week CISA added two new Ivanti Connect Secure vulnerabilities to the Known Exploited Vulnerabilities catalog, both part of a three-CVE exploit chain.** CVE-2026-118527 allows a remote authenticated attacker to write files to a predictable on-disk path, while CVE-2026-111357 (CVSS 7.0) enables a local attacker to escalate privileges through a missing authentication check on a critical function. Together with the previously catalogued CVE-2026-104935, these three flaws can be chained to achieve full appliance compromise from an unauthenticated starting position.

If your organization runs Ivanti Connect Secure, the clock is ticking: CVE-2026-111357 carries a remediation due date of **2026-11-02** under BOD 26-04, and CISA has published forensic triage requirements that must be completed before the appliance is returned to service. Patch guidance is available in Ivanti's security advisory linked from the KEV entry. As always, if patching cannot be completed before the deadline, CISA's guidance is to discontinue use of the product rather than leave it exposed.
