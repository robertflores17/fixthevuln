# AppSec Review — 2026-06-24

**Reviewer:** Robert Flores, CISSP  
**CVEs Reviewed:** 4  
**Review Date:** 2026-06-24  

---

## Severity Breakdown

| Priority | Count |
|----------|-------|
| Critical | 3     |
| High     | 1     |
| Medium   | 0     |
| Low      | 0     |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2025-67038 | Lantronix | critical | OS Command Injection (RCE, root) |
| CVE-2026-34910 | Ubiquiti | high | Command Injection (Improper Input Validation) |
| CVE-2026-34909 | Ubiquiti | critical | Path Traversal → Account Compromise |
| CVE-2026-34908 | Ubiquiti | critical | Improper Access Control (Unauthorized System Modification) |

---

## Trend Analysis

This batch reflects a continued focus on network infrastructure and edge device security, with three of four CVEs targeting Ubiquiti UniFi OS — a platform ubiquitous in enterprise, SMB, and prosumer networks. The clustering of three vulnerabilities (CVE-2026-34908, -34909, -34910) from the same vendor and CISA advisory bulletin (Bulletin 064) indicates a coordinated disclosure for a multi-flaw attack chain: an attacker with network access could traverse paths to obtain credentials (34909), bypass access controls to modify system state (34908), and chain to command injection for code execution (34910). The Lantronix EDS5000 entry (CVE-2025-67038, CVSS 9.8) is a stark reminder that industrial serial device servers remain high-value targets — unauthenticated root command injection in the username field represents a complete pre-auth compromise of OT/serial infrastructure with minimal attacker sophistication required.

---

## Blog Post Candidates

1. **"The Ubiquiti Triple-Threat: How CVE-2026-34908/34909/34910 Chain into Full Compromise"** — Walk through how path traversal to credential theft (34909) enables access control bypass (34908) that then enables command injection (34910), demonstrating chained exploitation on widely-deployed UniFi infrastructure.

2. **"Serial Killer: Unauthenticated RCE in Lantronix EDS5000 and the Forgotten OT Attack Surface"** — Explore how serial device servers bridging IT and OT networks are systematically overlooked in vulnerability management, using CVE-2025-67038 as the case study.

3. **"CISA BOD 26-04 in Practice: What the Three-Day Patch Window Means for Network Admins"** — Break down the new BOD 26-04 requirements using this batch of Ubiquiti/Lantronix KEV entries as real examples, covering forensics triage requirements and internet-exposure assessment obligations.

---

## Newsletter Snippet

**CISA KEV Alert — June 24, 2026:** This week's KEV additions are dominated by network infrastructure vulnerabilities demanding immediate attention. Ubiquiti UniFi OS received three simultaneous KEV entries (CVE-2026-34908, -34909, -34910), covering improper access control, path traversal, and command injection — all exploitable by any actor with network access to UniFi infrastructure. Two carry a perfect CVSS 10.0 score. If you manage UniFi equipment, patch now and review CISA's Bulletin 064 for forensics triage requirements under BOD 26-04. Lantronix EDS5000 serial device servers (CVE-2025-67038, CVSS 9.8) round out the batch with a pre-authentication root command injection — if you have EDS5000 units exposed, treat this as a critical incident response scenario.

The CISA KEV list now stands at 141 tracked vulnerabilities on this site, with 75% of this week's additions rated critical. The Ubiquiti cluster is particularly notable because UniFi OS serves as the control plane for switches, access points, and gateways — a compromised UniFi controller is effectively a compromised network. Combine that with Lantronix's foothold in OT environments and this batch represents a meaningful escalation in infrastructure risk. Patch windows are tight: CISA-mandated remediation due date is June 26, 2026.
