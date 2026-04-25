# AppSec Review — 2026-04-25

**Reviewer:** Robert Flores, CISSP  
**Review Date:** 2026-04-25  
**CVEs Reviewed:** 4  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 2 | CVE-2024-7399, CVE-2024-57726 |
| High     | 2 | CVE-2025-29635, CVE-2024-57728 |
| Medium   | 0 | — |
| Low      | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2025-29635 | D-Link | high | Command Injection (CWE-77) |
| CVE-2024-7399 | Samsung | critical | Path Traversal / Arbitrary File Write (CWE-22, CWE-434) |
| CVE-2024-57728 | SimpleHelp | high | Path Traversal / Zip Slip RCE (CWE-22, CWE-59) |
| CVE-2024-57726 | SimpleHelp | critical | Missing Authorization / Privilege Escalation (CWE-862) |

---

## Trend Analysis

This batch reflects two converging threat patterns active in mid-2026. First, end-of-life network devices (D-Link DIR-823X) continue to surface in KEV — attackers increasingly target EoL SOHO and SMB equipment where no patch will ever exist, making CISA's "discontinue use" guidance the only viable remediation. Second, remote-access and digital-signage management platforms are drawing sustained attention: both SimpleHelp vulnerabilities (CVE-2024-57726 and CVE-2024-57728) were disclosed in late 2024 but CISA's 2026 KEV addition signals active in-the-wild exploitation, consistent with threat actors targeting MSP tooling to achieve broad downstream access. The Samsung MagicINFO path traversal follows the same delayed-exploitation pattern — a 2024 CVE now actively leveraged, likely against unpatched enterprise digital signage deployments. Defenders should treat any 2024 CVE appearing in a 2026 KEV batch as a signal of ongoing exploitation campaigns, not historical remediation debt.

---

## Blog Post Candidates

1. **"Zip Slip Is Back: SimpleHelp CVE-2024-57728 and the Enduring Danger of Archive Path Traversal"** — Deep-dive on how zip-slip attacks work, why archive upload features are a persistent RCE vector, and how to test for them in your own applications.

2. **"The MSP Kill Chain: Chaining SimpleHelp CVE-2024-57726 + CVE-2024-57728 for Full Compromise"** — Walk through how a low-privilege technician account can escalate to admin (CVE-2024-57726) and then achieve host-level code execution via zip slip (CVE-2024-57728), illustrating why MSP-platform vulnerabilities carry outsized blast radius.

3. **"End-of-Life Doesn't Mean End of Exploitation: D-Link DIR-823X and the EoL Device Problem"** — Examines why EoL devices like the DIR-823X are a long-tail risk, how organizations can inventory and prioritize decommissioning, and the policy implications of CISA issuing KEV alerts for devices with no available patch.

---

## Newsletter Snippet

**New KEV Additions — April 25, 2026:** CISA added four new vulnerabilities to the Known Exploited Vulnerabilities catalog this week, spanning D-Link, Samsung, and SimpleHelp. Two stand out as critical: Samsung MagicINFO 9 Server (CVE-2024-7399, CVSS 8.8) allows an attacker to write arbitrary files as SYSTEM — effectively unauthenticated remote code execution on enterprise digital-signage infrastructure — and SimpleHelp's missing authorization flaw (CVE-2024-57726, CVSS 9.9) lets any technician-level user forge admin API keys, paving the way for full server takeover. If you run MagicINFO or SimpleHelp in your environment, patch immediately; CISA's remediation deadline is May 8, 2026.

The remaining two CVEs continue a troubling pattern: the D-Link DIR-823X (CVE-2025-29635) is end-of-life with no patch available, and SimpleHelp's zip-slip RCE (CVE-2024-57728) was disclosed in 2024 but is only now confirmed actively exploited. Both illustrate a broader trend worth watching — attackers are increasingly mining older, unpatched CVEs in widely-deployed management tooling and legacy networking equipment. Organizations relying on EoL devices or slow patch cycles should treat this KEV batch as a forcing function to accelerate decommissioning and upgrade timelines.
