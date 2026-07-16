# AppSec Review — 2026-07-16

**Reviewer:** Robert Flores, CISSP  
**Review Date:** 2026-07-16  
**CVE Count:** 2  
**Database Total After Publish:** 158 vulnerabilities

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 1     | CVE-2026-46817 |
| High     | 1     | CVE-2023-4346  |
| Medium   | 0     | — |
| Low      | 0     | — |
| **Total**| **2** | |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-46817 | Oracle | critical | Auth Bypass / Improper Privilege Management (CWE-269, CWE-287, CWE-306) |
| CVE-2023-4346  | KNX Association | high | Account Lockout / Authorization Control Bypass (CWE-645) |

---

## Trend Analysis

This batch reflects two converging threat trends. CVE-2026-46817 continues a long-running pattern of high-severity vulnerabilities in Oracle enterprise software: an unauthenticated CVSS 9.8 privilege escalation in Oracle E-Business Suite that directly compromises Oracle Payments is exactly the type of target ransomware operators and nation-state actors prioritize for initial access and financial data exfiltration. The three CWEs (CWE-269, CWE-287, CWE-306) together describe a complete authentication-bypass chain, suggesting attackers can reach sensitive payment workflows with zero credentials, making the 3-day BOD 26-04 remediation deadline entirely appropriate.

CVE-2023-4346 highlights CISA's increasing attention to ICS/OT attack surfaces: a 2023 vulnerability in the KNX building-automation protocol was dormant in the NVD for nearly three years before confirmed active exploitation triggered its KEV addition. The ability to purge all KNX devices and set a BCU lock key — effectively bricking smart-building infrastructure — mirrors tactics seen in recent destructive attacks on critical infrastructure. Organizations operating KNX-based HVAC, lighting, or access-control systems should treat this as urgent given the 29 July 2026 BOD 26-04 deadline.

---

## Blog Post Candidates

1. **"Unauth to Owned: Breaking Down the Oracle Payments Auth Bypass (CVE-2026-46817)"** — Walkthrough of the CWE-269/287/306 chain and what privilege escalation to payment-system takeover looks like in practice; includes detection queries for network defenders.
2. **"ICS in the Crosshairs: How CVE-2023-4346 Lets Attackers Brick Your Building"** — Deep dive into the KNX protocol's authorization model, what BCU key manipulation means operationally, and compensating controls for building-automation environments lacking vendor patches.
3. **"CISA KEV Time Lag: Why a 2023 ICS CVE Just Got Added in 2026"** — Analysis of how vulnerabilities with delayed KEV additions signal shifts in threat-actor targeting, using this batch as a case study.

---

## Newsletter Snippet

This week's CISA KEV additions include a critical Oracle E-Business Suite auth bypass (CVE-2026-46817, CVSS 9.8) that lets unauthenticated attackers over HTTP take over Oracle Payments — no credentials required. If your organization runs Oracle EBS, patching against the May 2026 Critical Patch Update is not optional; BOD 26-04 sets a three-day remediation deadline (2026-07-18). Review network segmentation around Oracle EBS instances now, and check your SIEM for anomalous HTTP traffic to Oracle Payments endpoints.

Also added this week: CVE-2023-4346 in the KNX building-automation protocol, a three-year-old ICS vulnerability that CISA just confirmed as actively exploited. Attackers can purge all devices on a KNX network and permanently lock them with a BCU key — an irreversible denial of service against smart-building infrastructure. If you manage facilities using KNX for HVAC, lighting, or physical access control, contact your integrator about patching or network segmentation immediately. The BOD 26-04 deadline is 2026-07-29.
