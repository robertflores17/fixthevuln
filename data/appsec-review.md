# AppSec Review — 2026-07-17

**Reviewer:** Robert Flores, CISSP  
**Review Date:** 2026-07-17  
**CVE Count:** 3  
**Database Total After Publish:** 161 vulnerabilities

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 3     | CVE-2026-58644, CVE-2026-25089, CVE-2026-39808 |
| High     | 0     | — |
| Medium   | 0     | — |
| Low      | 0     | — |
| **Total**| **3** | |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-58644 | Microsoft | critical | Deserialization / RCE (CWE-502) |
| CVE-2026-25089 | Fortinet  | critical | OS Command Injection (CWE-78) |
| CVE-2026-39808 | Fortinet  | critical | OS Command Injection (CWE-78) |

---

## Trend Analysis

All three CVEs added on 2026-07-16 share a common and deeply concerning pattern: unauthenticated remote code execution with CVSS scores of 9.8. The two Fortinet FortiSandbox advisories (CVE-2026-25089 and CVE-2026-39808) represent distinct vulnerabilities in the same product — FortiSandbox, FortiSandbox Cloud, and FortiSandbox PaaS — suggesting systemic issues in how HTTP request input is handled across the codebase. The presence of dual critical CVEs on a security product (a sandbox environment) is particularly alarming, as threat actors can leverage a compromised sandbox to study and evade organizational defenses. The Microsoft SharePoint deserialization vulnerability continues a long-standing pattern of .NET deserialization issues (CWE-502) in Microsoft's enterprise collaboration platform; SharePoint's prevalence in government and enterprise environments and its internet-facing deployment posture make this a prime initial-access vector for ransomware affiliates and nation-state actors alike. Organizations running any of these products should treat patching as an emergency given the CISA KEV due date of 2026-07-19 and mandatory BOD 26-04 compliance requirements.

---

## Blog Post Candidates

1. **"Double Trouble in FortiSandbox: Two Critical RCE CVEs and What They Mean for Your Security Stack"** — A deep dive into CVE-2026-25089 and CVE-2026-39808, exploring why security appliances attract attackers and how to harden sandbox deployments.
2. **"SharePoint Deserialization in 2026: Why CWE-502 Keeps Coming Back"** — Examines the recurring pattern of .NET deserialization vulnerabilities in enterprise Microsoft products and provides hardening guidance for SharePoint administrators.
3. **"BOD 26-04 and the 72-Hour Patch Window: How to Build a Rapid Response Program"** — Practical guide for security teams on meeting CISA's aggressive patching timelines for KEV vulnerabilities, using this week's advisories as a case study.

---

## Newsletter Snippet

This week CISA added three critical vulnerabilities to the Known Exploited Vulnerabilities catalog, all carrying a CVSS score of 9.8 and all exploitable by unauthenticated attackers over the network. Fortinet's FortiSandbox received two separate advisories — CVE-2026-25089 (affecting FortiSandbox, FortiSandbox Cloud, and PaaS) and CVE-2026-39808 — both OS command injection flaws triggered via crafted HTTP requests. Microsoft SharePoint was hit with CVE-2026-58644, a deserialization vulnerability allowing unauthenticated remote code execution, continuing a troubling pattern of CWE-502 issues in enterprise collaboration platforms.

Federal agencies face a remediation deadline of **2026-07-19** under BOD 26-04; private-sector organizations should treat this timeline as a best-practice benchmark. If your organization runs any of these products and they are internet-accessible, patch immediately or implement compensating controls — these vulnerability classes are trivially weaponized and actively exploited in the wild. Check your attack surface exposure via your ASM tooling and prioritize FortiSandbox instances given the double advisory, which suggests broader input-handling weaknesses in the product line.
