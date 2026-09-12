# AppSec Review — 2026-09-12

**Reviewer:** Robert Flores, CISSP  
**CVEs Reviewed:** 2  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog  

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 1 | CVE-2026-86060 |
| High     | 1 | CVE-2026-67277 |
| Medium   | 0 | — |
| Low      | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-86060 | MikroTik | Critical | Argument Injection / Privilege Escalation |
| CVE-2026-67277 | MikroTik | High | Missing Authentication / Memory Disclosure + DoS |

---

## Analysis

**CVE-2026-86060** — MikroTik RouterOS Argument Injection (CWE-88), CVSS 9.8. This argument injection flaw allows an attacker to manipulate the trusted RouterOS policy mask, enabling privilege escalation. With a CVSS of 9.8 and no authentication barrier implied, this is a pre-auth or low-auth network-accessible vector on one of the most widely deployed router platforms in ISP and SMB environments. Priority: **Critical**.

**CVE-2026-67277** — MikroTik RouterOS Missing Authentication for Critical Function (CWE-306), CVSS 8.2. The btest (bandwidth test) service lacks authentication, exposing kernel memory and enabling denial of service remotely. While this doesn't provide full remote code execution, unauthenticated kernel memory disclosure is a high-impact primitive that can facilitate further exploitation or network reconnaissance. Priority: **High**.

---

## Trend Analysis

Both CVEs this cycle target MikroTik RouterOS, continuing a sustained focus by threat actors on networking infrastructure. RouterOS is prevalent in ISPs, SMBs, and home labs, making it a high-value target for botnet recruitment, traffic interception, and lateral movement into enterprise networks. The combination of an argument injection bug (CVSS 9.8) and a missing-authentication vulnerability in a bandwidth-testing service illustrates a pattern of fundamental design flaws being weaponized rather than sophisticated zero-days — these are the kind of implementation oversights that persist in embedded firmware and are difficult to patch at scale. Organizations should treat all RouterOS devices as internet-adjacent attack surfaces and prioritize immediate patching; MikroTik's September 2026 security advisory (referenced in CISA notes) provides the remediation path.

---

## Blog Post Candidates

1. **"MikroTik Under Fire: Two KEV Additions and What They Mean for Network Operators"** — Covers both CVEs, explains the attack surface of RouterOS in ISP/SMB environments, and gives practical remediation guidance.
2. **"Argument Injection: The Forgotten Injection Class"** — Uses CVE-2026-86060 as a case study to explain CWE-88, how it differs from command injection, and why it's underrepresented in training curricula despite high exploitability.
3. **"When Bandwidth Testing Becomes a Security Risk: Missing Auth in Network Services"** — Deep dive on CVE-2026-67277, the btest service design, and the broader problem of unauthenticated management/diagnostic services in embedded networking firmware.

---

## Newsletter Snippet

**This Week in Active Exploits:** CISA added two MikroTik RouterOS vulnerabilities to the KEV catalog this week, both with federal patch deadlines of September 13, 2026. The more severe of the two, CVE-2026-86060 (CVSS 9.8), is an argument injection flaw that lets attackers rewrite RouterOS policy masks and escalate privileges — effectively taking administrative control of affected devices. The second, CVE-2026-67277 (CVSS 8.2), exposes the btest (bandwidth test) service without authentication, leaking kernel memory and enabling denial of service. If you manage MikroTik devices, patching is not optional: these are confirmed actively exploited in the wild.

RouterOS turns up in KEV repeatedly because it sits at the intersection of ubiquity and infrequent patching — a dangerous combination. Many organizations run RouterOS devices on the network perimeter without centralized patch management, and threat actors know it. This week's additions reinforce the trend of targeting networking infrastructure as a beachhead rather than endpoints. Use this as a forcing function to audit your RouterOS inventory, apply the September 2026 advisory patches, and verify no devices are running exposed management or diagnostic services (btest, Winbox, API) on untrusted interfaces.
