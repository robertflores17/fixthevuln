# AppSec Review — CISA KEV Batch

**Date:** 2026-04-14
**Reviewer:** Robert Flores, CISSP
**CVE Count:** 7

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 1 | CVE-2026-21643 |
| High | 6 | CVE-2012-1854, CVE-2025-60710, CVE-2023-21529, CVE-2023-36424, CVE-2020-9715, CVE-2026-34621 |
| Medium | 0 | — |
| Low | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2012-1854 | Microsoft | high | Insecure Library Loading / DLL Hijacking (RCE) |
| CVE-2025-60710 | Microsoft | high | Link Following / Symlink Abuse (LPE) |
| CVE-2023-21529 | Microsoft | high | Deserialization of Untrusted Data (Auth RCE) |
| CVE-2023-36424 | Microsoft | high | Memory Corruption / Out-of-Bounds Read (LPE) |
| CVE-2020-9715 | Adobe | high | Use-After-Free (RCE) |
| CVE-2026-21643 | Fortinet | critical | SQL Injection (Unauth RCE) |
| CVE-2026-34621 | Adobe | high | Prototype Pollution (RCE) |

---

## Trend Analysis

This batch is dominated by Microsoft products (4 of 7 CVEs), reflecting the continued targeting of the Windows ecosystem across both kernel-level privilege escalation (CLFS driver, link following) and application-layer attack surfaces (VBA, Exchange deserialization). The presence of legacy CVEs from 2012 and 2020 alongside 2025-2026 entries underscores a persistent pattern: threat actors revisit old vulnerabilities when large populations of unpatched systems remain reachable, particularly in environments running end-of-life Office or Acrobat versions. The single critical-rated entry — Fortinet FortiClient EMS SQL injection (CVE-2026-21643, CVSS 9.8) — demands immediate attention, as its unauthenticated remote exploitation profile mirrors the Fortinet SQLi wave of 2024 (CVE-2023-48788) that was weaponized globally within days of public disclosure.

Adobe Acrobat appears twice in this batch (CVE-2020-9715, CVE-2026-34621), reinforcing that document-based delivery remains a primary initial access mechanism. The JavaScript engine prototype pollution in CVE-2026-34621 is particularly notable as it represents an emerging class of memory safety bypass in scripting runtimes embedded within productivity applications — a trend that will likely accelerate as memory-safe rewrites leave legacy JavaScript engines as the remaining high-value attack surface.

---

## Blog Post Candidates

1. **"Fortinet FortiClient EMS SQL Injection (CVE-2026-21643): Anatomy of a Critical Perimeter Exploit"** — Deep dive into how unauthenticated SQLi on a network management product translates to full RCE, with detection and hunting guidance for enterprise defenders.

2. **"The CLFS Driver Problem: Why Windows Kernel LPE Keeps Haunting Ransomware Investigations"** — Analysis of the recurring exploitation of the Common Log File System driver (CVE-2023-36424 and predecessors) as a post-exploitation LPE primitive by ransomware affiliates and APT groups.

3. **"Old Dogs, New Tricks: Why CISA Added a 2012 Microsoft CVE to the KEV in 2026"** — Investigation into legacy CVE re-cataloguing, explaining why CVE-2012-1854 still matters and what it signals about long-tail patch compliance failures in enterprise Office deployments.

---

## Newsletter Snippet

This week's CISA KEV update brings 7 confirmed actively-exploited vulnerabilities across Microsoft, Adobe, and Fortinet — and the headline is unambiguous: Fortinet FortiClient EMS (CVE-2026-21643) carries a CVSS 9.8 rating for unauthenticated SQL injection enabling remote code execution. If your organization runs FortiClient EMS and hasn't applied the patch yet, treat this as a fire drill — Fortinet perimeter products have been aggressively targeted since 2024, and similar vulnerabilities moved from disclosure to mass exploitation within 72 hours. Federal agencies face a CISA remediation deadline of April 16, just two days away.

Beyond Fortinet, this batch reveals two important trends worth tracking. First, legacy CVEs are back: both CVE-2012-1854 (Microsoft VBA insecure library loading) and CVE-2020-9715 (Adobe Acrobat use-after-free) are years-old vulnerabilities that CISA confirmed as actively exploited in 2026 — a reminder that threat actors don't abandon old techniques when unpatched systems remain accessible. Second, Adobe Acrobat appears twice this cycle, with a modern prototype pollution RCE (CVE-2026-34621) joining the legacy entry, reinforcing that PDF-based document attacks remain a durable initial access vector. Prioritize patching Fortinet immediately, then work through the Microsoft kernel LPE and Exchange deserialization entries before the April 27 deadline.
