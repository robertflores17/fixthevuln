# AppSec Review — 2026-09-11

**Reviewer:** Robert Flores, CISSP  
**CVEs Reviewed:** 4  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog  

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 2 | CVE-2026-19490, CVE-2026-20079 |
| High     | 2 | CVE-2025-25249, CVE-2026-87491 |
| Medium   | 0 | — |
| Low      | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-19490 | Citrix | critical | Authentication Bypass (CWE-288) |
| CVE-2025-25249 | Fortinet | high | Heap-Based Buffer Overflow / RCE (CWE-122, CWE-787) |
| CVE-2026-87491 | Google | high | Out-of-Bounds Write / Memory Corruption (CWE-787) |
| CVE-2026-20079 | Cisco | critical | Authentication Bypass → Root RCE (CWE-288) |

---

## Trend Analysis

This batch reflects an ongoing and intensifying pattern of unauthenticated authentication bypass vulnerabilities targeting enterprise network security infrastructure. Two of the four CVEs — Citrix NetScaler (CVSS 9.8) and Cisco FMC/SCC (CVSS 10.0) — exploit alternate-path authentication flaws (CWE-288) that allow remote attackers to completely bypass access controls on gateway, VPN, and firewall management systems. These products sit at the perimeter of enterprise networks, meaning a successful exploit can serve as the initial access vector for ransomware or state-sponsored intrusions. The Fortinet heap overflow and Chrome V8 out-of-bounds write round out the batch with memory corruption chains that enable code execution, continuing a multi-year trend of memory safety failures in widely-deployed C/C++ codebases. The presence of a 2025-vintage Fortinet CVE in a September 2026 KEV addition signals that threat actors are revisiting older, under-patched vulnerabilities — organizations that deprioritized patching in 2025 are now demonstrably under active attack.

---

## Blog Post Candidates

1. **"Unauthenticated to Root: The Authentication Bypass Epidemic in Network Security Products"** — Deep dive into CWE-288 patterns across Citrix NetScaler and Cisco FMC, explaining how alternate-path flaws arise, how attackers exploit them, and what defenders should check beyond the patch.

2. **"Why CISA Added a 2025 Fortinet CVE in 2026: Understanding Deferred Exploitation"** — Analysis of why threat actors revisit older vulnerabilities, how to prioritize legacy CVEs, and what the Fortinet heap overflow tells us about operational security debt.

3. **"Browser Exploitation in 2026: V8 OOB Writes and the Limits of Sandbox Security"** — Technical primer on Chromium V8 memory safety issues, sandbox escape research, and why browser RCE remains a persistent enterprise risk despite years of hardening.

---

## Newsletter Snippet

**This Week's KEV Additions — Critical Patches for Citrix, Cisco, Fortinet, and Chrome**

CISA added four actively exploited vulnerabilities to the KEV catalog this week, two of which carry the highest possible or near-maximum severity scores. Cisco Secure Firewall Management Center (FMC) and Security Cloud Control (SCC) received a CVSS 10.0 rating for an unauthenticated authentication bypass that allows a remote attacker to execute scripts and gain root access to the underlying OS — this is about as bad as it gets for network security infrastructure. Citrix NetScaler ADC and Gateway are similarly affected by a CVSS 9.8 authentication bypass impacting SSL VPN and ICA Proxy configurations. Both have a CISA remediation due date of September 12, meaning federal agencies have essentially no time to spare.

Rounding out the batch: Fortinet FortiOS, FortiSwitchManager, and FortiSASE are affected by a heap-based buffer overflow (CVSS 8.1) that enables remote code execution via specially crafted packets — a 2025 CVE that CISA is now flagging due to confirmed in-the-wild exploitation. Google Chrome/Chromium (CVSS 8.8) has a V8 engine out-of-bounds write that allows sandbox-confined arbitrary code execution via a malicious web page, affecting Chrome, Edge, and Opera users. If your organization runs any of these products, treat the September 12 due date as your personal deadline — patch now.
