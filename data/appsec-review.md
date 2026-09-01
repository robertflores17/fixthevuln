# AppSec Review — 2026-09-01

**Reviewer:** Robert Flores, CISSP  
**CVEs Reviewed:** 2  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog  
**Review Date:** 2026-09-01

---

## Severity Breakdown

| Priority | Count |
|----------|-------|
| Critical | 2     |
| High     | 0     |
| Medium   | 0     |
| Low      | 0     |
| **Total**| **2** |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-82078 | PaperCut | Critical | Unsafe Reflection / RCE |
| CVE-2026-81578 | PaperCut | Critical | Missing Authentication (Auth Bypass) |

---

## Trend Analysis

This batch surfaces a dangerous chained exploit pairing in PaperCut NG/MF, a widely-deployed enterprise print management platform. CVE-2026-81578 (CVSS 9.8) provides the unauthenticated entry point — an attacker with network access to the PaperCut application server can modify critical system configurations without any credentials. That foothold directly enables CVE-2026-82078 (CVSS 9.1), which leverages unsafe Java reflection to execute arbitrary bytecode already present on the application classpath, achieving full server compromise. The compound attack path — unauthenticated config write leading to code execution — mirrors the 2023 PaperCut exploitation wave (CVE-2023-27350/27351) and confirms that print management infrastructure remains a persistent attacker target. CISA's addition under BOD 26-04 and the 14-day remediation window signal confirmed in-the-wild exploitation; organizations should treat unpatched PaperCut servers as actively compromised until patched and forensically triaged per CISA's published requirements.

---

## Blog Post Candidates

1. **"PaperCut Under Fire Again: Anatomy of the 2026 Auth Bypass + RCE Chain"** — Deep-dive into how CVE-2026-81578 + CVE-2026-82078 chain together, with detection guidance and YARA/Sigma rules for hunting indicators.
2. **"Why Print Servers Keep Getting Popped: A Pattern Analysis"** — Retrospective comparing the 2023 and 2026 PaperCut KEV additions; makes the case that print management infrastructure deserves the same exposure-minimization treatment as VPNs and Exchange.
3. **"BOD 26-04 in Practice: What the 14-Day Patch Window Means for Your Program"** — Practitioner guide to operationalizing CISA's binding directive, using this PaperCut batch as the worked example.

---

## Newsletter Snippet

**CISA added two critical PaperCut vulnerabilities to the KEV catalog this week**, and they chain together for unauthenticated remote code execution. CVE-2026-81578 (CVSS 9.8) allows an attacker with network access to modify PaperCut system configurations without logging in. That config-write primitive directly feeds CVE-2026-82078 (CVSS 9.1), which abuses unsafe Java reflection to execute arbitrary bytecode under the PaperCut server process — full compromise in two steps, no credentials required. Both carry a September 14 remediation deadline under BOD 26-04, and CISA has published forensics triage requirements alongside the patch guidance, signaling they have evidence of active exploitation.

If you're running PaperCut NG or MF, patch immediately and follow CISA's forensic triage steps to confirm whether you were hit before the patch landed. This mirrors the 2023 PaperCut exploitation wave almost exactly: the vulnerability class, the chaining pattern, and the breadth of exposed instances are all consistent with that campaign. Print management servers tend to have broad internal network access and service-account privileges — making them high-value pivots once compromised. Minimize external exposure, apply the vendor patch, rotate credentials on the PaperCut service account, and review logs for the indicators CISA published in the BOD 26-04 implementation guidance.
