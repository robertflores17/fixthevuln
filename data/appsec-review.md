# AppSec Review — CISA KEV Batch
**Date:** 2026-11-21  
**Reviewer:** Robert Flores, CISSP  
**CVEs Reviewed:** 4  
**All Approved for Publication**

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 3 | CVE-2026-129448, CVE-2026-123890, CVE-2026-76466 |
| High | 1 | CVE-2025-42884 |
| Medium | 0 | — |
| Low | 0 | — |

---

## CVE Summary

| CVE ID | Vendor / Product | Priority | Vuln Class |
|--------|-----------------|----------|------------|
| CVE-2026-129448 | Apache / Roller | critical | Deserialization RCE (CWE-502) |
| CVE-2026-123890 | Broadcom / VMware vCenter | critical | Authentication Bypass (CWE-288) |
| CVE-2025-42884 | SAP / NetWeaver Enterprise Portal | high | JNDI Injection / Query Logic (CWE-943) |
| CVE-2026-76466 | Cisco / Expressway Series | critical | Hard-coded Credentials (CWE-798) |

---

## CVE Details

**CVE-2026-129448 — Apache Roller** (CVSS 9.8, Critical)  
Pre-authentication deserialization of untrusted data via the XML-RPC endpoint (CWE-502). Unauthenticated RCE with no user interaction required; Java deserialization gadget chains make exploitation straightforward. Patch immediately — this endpoint should be disabled if XML-RPC is not required.

**CVE-2026-123890 — Broadcom VMware vCenter** (CVSS 9.8, Critical)  
Authentication bypass through an alternate path in VMware Directory Service (CWE-288). An unauthenticated attacker with network access to vCenter gains full access, compromising hypervisor management of entire virtual infrastructure. vCenter is perimeter-adjacent in most enterprise environments; treat this as a datacenter-wide critical.

**CVE-2025-42884 — SAP NetWeaver Enterprise Portal** (CVSS 6.5, High)  
JNDI injection via improper query logic neutralization (CWE-943) enables unauthenticated server info disclosure and modification. 2025 CVE added to KEV in November 2026, indicating sustained active exploitation of under-patched SAP systems — a common pattern for SAP vulnerabilities which tend to have long remediation cycles.

**CVE-2026-76466 — Cisco Expressway Series** (CVSS 9.8, Critical)  
Hard-coded credentials in the database service of clustered Expressway devices (CWE-798) allow unauthenticated root command execution by an attacker with network access and persistent cookies. Hard-coded credentials in network-exposed clustering infrastructure represent a supply-chain-level trust failure; there is no compensating control short of patching.

---

## Trend Analysis

This batch continues the November 2026 KEV acceleration pattern: three of four additions carry CVSS 9.8, targeting foundational enterprise infrastructure — hypervisors (vCenter), collaboration platforms (Cisco Expressway), and application servers (Apache Roller, SAP NetWeaver). The VMware vCenter auth bypass and Apache Roller deserialization are archetypal infrastructure pivot points; once exploited, they hand attackers full lateral movement capability across datacenter or DevOps environments. The SAP NetWeaver JNDI injection warrants attention beyond its moderate CVSS — JNDI-based attacks have demonstrated severe real-world impact (cf. Log4Shell) and SAP's installed base skews toward high-value financial and manufacturing targets. Defenders should prioritize vCenter and Cisco Expressway patches within the BOD 26-04 three-day window, treat the SAP finding as exploitable regardless of CVSS score, and audit Apache Roller deployments for exposed XML-RPC endpoints as an interim mitigation.

---

## Blog Post Candidates

1. **"Why CVSS Scores Lie: SAP NetWeaver JNDI Injection Is More Dangerous Than a 6.5"** — walk through why CWE-943 on enterprise middleware warrants critical-level response despite a mid-range score.
2. **"vCenter Auth Bypass: The Blast Radius of a Single Unauthenticated Request"** — model the attack chain from CVE-2026-123890 to full datacenter compromise, including ESXi host access and VM exfiltration.
3. **"Hard-coded Credentials in 2026: Why CWE-798 Won't Die"** — use Cisco Expressway as a case study for why embedded credentials persist in enterprise network gear and what detection looks like.

---

## Newsletter Snippet

CISA added four new vulnerabilities to the Known Exploited Vulnerabilities catalog this week, three of which carry a maximum CVSS score of 9.8. The most urgent is **CVE-2026-123890** (Broadcom VMware vCenter), an authentication bypass that lets any network-adjacent attacker walk straight into your hypervisor management plane — no credentials required. Close behind is **CVE-2026-76466** (Cisco Expressway Series), where hard-coded database credentials enable unauthenticated root execution on clustered video conferencing infrastructure, and **CVE-2026-129448** (Apache Roller), a pre-auth deserialization flaw exposing the XML-RPC endpoint to trivial remote code execution.

Don't sleep on **CVE-2025-42884** (SAP NetWeaver) just because its CVSS is 6.5 — JNDI injection on SAP Enterprise Portal is a stealth pivot point into some of the most sensitive ERP data in your organization, and the 2025-to-2026 KEV lag tells you adversaries have been exploiting unpatched systems for months. All four have a BOD 26-04 remediation due date of **2026-11-23**, leaving federal agencies less than 72 hours. If you're running any of these products, patch now — or disable the vulnerable feature surface until you can.
