# AppSec Review — CISA KEV Batch

**Date:** 2026-03-27
**Reviewer:** Robert Flores, CISSP
**CVE Count:** 13

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 6 | CVE-2025-68613, CVE-2025-26399, CVE-2026-1603, CVE-2017-7921, CVE-2021-22681, CVE-2026-22719 |
| High     | 7 | CVE-2026-3910, CVE-2026-3909, CVE-2021-22054, CVE-2023-43000, CVE-2021-30952, CVE-2023-41974, CVE-2026-21385 |
| Medium   | 0 | — |
| Low      | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-3910 | Google | high | Memory Buffer Bounds / Sandbox RCE |
| CVE-2026-3909 | Google | high | Out-of-Bounds Write |
| CVE-2025-68613 | n8n | critical | Code Injection / RCE |
| CVE-2021-22054 | Omnissa | high | SSRF |
| CVE-2025-26399 | SolarWinds | critical | Deserialization / RCE |
| CVE-2026-1603 | Ivanti | critical | Authentication Bypass |
| CVE-2017-7921 | Hikvision | critical | Improper Authentication |
| CVE-2021-22681 | Rockwell | critical | Insufficient Credential Protection |
| CVE-2023-43000 | Apple | high | Use-After-Free / Memory Corruption |
| CVE-2021-30952 | Apple | high | Integer Overflow / RCE |
| CVE-2023-41974 | Apple | high | Use-After-Free / Kernel Privilege Escalation |
| CVE-2026-22719 | Broadcom | critical | Command Injection / RCE |
| CVE-2026-21385 | Qualcomm | high | Memory Corruption |

---

## Trend Analysis

This batch reflects two dominant themes in the current threat landscape. First, there is sustained attacker focus on enterprise and operational technology management platforms: Ivanti EPM, SolarWinds Web Help Desk, Omnissa Workspace ONE, Broadcom VMware Aria Operations, and Rockwell Automation controllers all appear — products that sit at the intersection of privileged access and broad network reach, making them prime targets for initial access brokers and ransomware operators. Second, legacy CVEs from 2017 and 2021 (Hikvision, Rockwell, Apple, Omnissa) continue to re-enter active exploitation years after initial disclosure, underscoring that patching rates in IoT/OT environments and unmanaged consumer devices remain critically low. The browser/rendering engine segment (Google Chromium V8, Skia, Apple WebKit) maintains a steady cadence of memory corruption findings being weaponized in-the-wild, a trend unlikely to abate given the ubiquity of web-based attack surfaces across both enterprise and consumer targets.

---

## Blog Post Candidates

1. **"The Patching Debt Crisis: Why 2017 and 2021 CVEs Are Still Being Exploited in 2026"** — Deep dive into Hikvision CVE-2017-7921 and Rockwell CVE-2021-22681 as case studies in the OT/IoT patching gap, covering why legacy industrial and surveillance systems remain exposed and what asset owners can do.

2. **"Enterprise Management Platforms: The New Crown Jewels for Attackers"** — Analysis of how Ivanti EPM, SolarWinds Web Help Desk, and VMware Aria Operations represent a pattern of targeting privileged management tooling for lateral movement and credential harvesting.

3. **"n8n and the Workflow Automation Attack Surface"** — Exploration of CVE-2025-68613 in the context of the growing use of no-code/low-code automation tools in enterprise environments, covering how dynamic code execution features become RCE vectors and what security teams should evaluate before deploying these tools.

---

## Newsletter Snippet

**CISA added 13 new vulnerabilities to the Known Exploited Vulnerabilities catalog this cycle, with six rated critical — including an unauthenticated RCE in n8n (CVSS 9.9), a deserialization RCE in SolarWinds Web Help Desk (CVSS 9.8), and an authentication bypass in Ivanti Endpoint Manager. Three of the thirteen CVEs are legacy disclosures from 2017 and 2021 that have re-entered active exploitation: a Hikvision camera authentication bypass (CVE-2017-7921), a Rockwell Automation credential protection flaw in Logix controllers (CVE-2021-22681), and an Omnissa Workspace ONE SSRF (CVE-2021-22054). If these are in your environment and haven't been patched, treat them as actively compromised until proven otherwise.**

Organizations using any of the affected products should prioritize Ivanti EPM, SolarWinds WHD, and Broadcom VMware Aria Operations patches immediately given the combination of unauthenticated access vectors and wide enterprise deployment. Browser security teams should verify Chromium-based browsers are on the latest stable channel addressing CVE-2026-3910 and CVE-2026-3909. For OT/ICS environments running Rockwell Automation equipment, the path-based authentication bypass in Studio 5000 Logix Designer (CVE-2021-22681) should be treated as a critical remediation priority — network segmentation and controller firmware updates are both required to fully address exposure. Full details and remediation guidance for all 13 CVEs are available at fixthevuln.com.
