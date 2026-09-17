# AppSec Review — 2026-09-17

**Reviewer:** Robert Flores, CISSP  
**Review Date:** 2026-09-17  
**CVEs Reviewed:** 2  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog  

---

## Severity Breakdown

| Priority | Count |
|----------|-------|
| Critical | 1     |
| High     | 1     |
| Medium   | 0     |
| Low      | 0     |
| **Total**| **2** |

---

## CVE Summary

| CVE ID | Vendor | Product | Priority | Vuln Class |
|--------|--------|---------|----------|------------|
| CVE-2026-58704 | Google | Pixel | High | Improper Authorization / Privilege Escalation |
| CVE-2026-76460 | Cisco | Identity Services Engine | Critical | Authentication Bypass (Unauth Remote) |

---

## Individual CVE Analysis

### CVE-2026-58704 — Google Pixel Improper Authorization (Cellular Modem)
**Priority: High | CVSS: 8.8 | CWEs: CWE-285, CWE-693**

A logic error in the cellular modem of Google Pixel devices allows an attacker to bypass permission checks and escalate privileges. The cellular modem attack vector makes this remotely exploitable without requiring physical access, and the widespread consumer deployment of Pixel devices amplifies exposure. CISA's BOD 26-04 directive designates this for priority remediation, and the short 3-day due date indicates active exploitation concern.

### CVE-2026-76460 — Cisco ISE Incorrect Use of Privileged APIs
**Priority: Critical | CVSS: N/A (pending) | CWEs: N/A**

Cisco Identity Services Engine (ISE) and ISE Passive Identity Connector contain an incorrect use of privileged APIs that enables an unauthenticated remote attacker to bypass the web-based management interface entirely. This is a canonical critical-severity pattern: unauthenticated network access to the administrative plane of a widely-deployed NAC/AAA product. Cisco ISE sits at the heart of enterprise network access control, so compromise can enable lateral movement, policy bypass, and credential harvesting at scale.

---

## Trend Analysis

Both vulnerabilities added in this batch reflect a continuing trend CISA has emphasized throughout 2026: privileged API misuse and authorization logic failures in high-value enterprise and consumer infrastructure. The Cisco ISE finding is particularly notable because network access control systems are high-value targets that, once compromised, can provide attackers with visibility into and control over the entire network authentication fabric. The Google Pixel modem vulnerability continues a pattern of hardware-adjacent attack surfaces (baseband, firmware) being weaponized against mobile devices — historically difficult to patch at scale given carrier dependency. The extremely tight 3-day remediation windows (BOD 26-04) on both entries underscore that CISA has evidence of active, ongoing exploitation in the wild.

---

## Blog Post Candidates

1. **"Why Cisco ISE Auth Bypass Is a SOC Nightmare"** — Deep dive into how Cisco ISE underpins Zero Trust architectures and what an unauthenticated management-plane bypass means for network segmentation and identity policies.

2. **"Cellular Modem Attack Surface: The Underrated Risk in Mobile Device Management"** — Explore how baseband/modem vulnerabilities bypass MDM controls and OS-level sandboxing, with mitigation guidance for enterprise mobile fleets.

3. **"CISA BOD 26-04 Three-Day Patches: How to Operationalize Emergency Remediation"** — Practical playbook for security teams on how to triage, prioritize, and patch KEV entries with sub-week SLAs, using these two CVEs as worked examples.

---

## Newsletter Snippet

**This Week in Active Exploitation (Sep 17, 2026)**

CISA added two high-stakes vulnerabilities to the Known Exploited Vulnerabilities catalog this week, both carrying 3-day remediation deadlines under BOD 26-04. The more severe of the two — CVE-2026-76460 in Cisco Identity Services Engine — is an unauthenticated remote authentication bypass that lets attackers walk straight past the management interface of one of the most widely deployed network access control platforms in the enterprise. If your organization relies on Cisco ISE for Zero Trust policy enforcement or network segmentation, this is a patch-now situation; there is no authentication barrier standing between an attacker and full administrative control of the device.

The second entry, CVE-2026-58704, targets the cellular modem in Google Pixel devices — a reminder that hardware-adjacent attack surfaces remain a blind spot for many security programs. Unlike app-layer vulnerabilities, modem exploits can bypass MDM controls and OS sandboxing entirely, making them attractive for targeted surveillance and espionage operations. Enterprise mobile device programs should apply the Pixel security bulletin immediately and review BOD 26-04 forensics triage requirements for any devices that may have been exposed. Both vulnerabilities are confirmed actively exploited; treat these as incidents-in-progress, not routine patch cycle items.
