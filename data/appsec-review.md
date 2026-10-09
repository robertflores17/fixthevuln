# AppSec Review — 2026-10-09

**Reviewer:** Robert Flores, CISSP (automated via FixTheVuln AppSec Reviewer)
**CVE Count:** 5
**Source:** CISA KEV — dateAdded 2026-10-08

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 2 | CVE-2021-3199, CVE-2015-3306 |
| High     | 2 | CVE-2015-5477, CVE-2016-3081 |
| Medium   | 1 | CVE-2023-22894 |
| Low      | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2015-5477 | ISC (BIND) | High | Denial of Service (data processing / assertion failure) |
| CVE-2016-3081 | Apache (Struts) | High | Remote Code Execution (command injection) |
| CVE-2023-22894 | Strapi | Medium | Information Disclosure (cleartext sensitive data storage) |
| CVE-2021-3199 | ONLYOFFICE | Critical | Remote Code Execution (path traversal via file upload) |
| CVE-2015-3306 | ProFTPD | Critical | Remote Code Execution (improper access control / arbitrary file write) |

---

## Trend Analysis

This batch represents a BOD 26-04 retroactive sweep, with four of five CVEs dating from 2015–2021. CISA's pattern of revisiting decade-old vulnerabilities signals that legacy infrastructure — FTP servers, DNS resolvers, Java web frameworks, and document collaboration platforms — remains actively exploited in the wild, likely targeting unpatched government and enterprise assets. The presence of Apache Struts (CVE-2016-3081) alongside the ProFTPD module-copy flaw (CVE-2015-3306, CVSS 10.0) confirms that unauthenticated RCE on widely-deployed open-source servers continues to be a high-value attack surface. The Strapi chain (CVE-2023-22894 + CVE-2023-22621) is the only recent entry and illustrates how CMS/headless platforms are increasingly weaponized via privilege-escalation chains that convert partial access into full RCE on EoL software.

---

## Blog Post Candidates

1. **"The FTP File That Pwned Servers for a Decade: Inside ProFTPD CVE-2015-3306"** — Deep dive into mod_copy's SITE CPFR/CPTO abuse, real-world exploitation scenarios (e.g., combined with WordPress file-upload paths), and detection strategies using FTP log analysis.

2. **"Apache Struts Is Still in Production: Why CVE-2016-3081 Keeps Showing Up in KEV"** — Enterprise Java lifecycle management failures, how Dynamic Method Invocation persists in legacy codebases, and a timeline of Struts KEV additions from 2017 to 2026.

3. **"Chaining for RCE: The Strapi CVE-2023-22894 + CVE-2023-22621 Attack Path"** — Step-by-step technical breakdown of how admin panel information disclosure chains into template injection for unauthenticated RCE, and why EoL headless CMS platforms are a growing attack vector.

---

## Newsletter Snippet

**CISA added 5 new vulnerabilities to the Known Exploited Vulnerabilities catalog this week**, spanning legacy DNS, FTP, and Java web infrastructure alongside a modern headless CMS chain. Two reach critical severity: **ONLYOFFICE Docs (CVE-2021-3199, CVSS 9.8)** allows unauthenticated path traversal leading to remote code execution via a malformed image upload path, and **ProFTPD (CVE-2015-3306, CVSS 10.0)** exposes arbitrary file read/write through the mod_copy module — a flaw that has been actively weaponized for over a decade but remains unpatched across legacy FTP deployments. BOD 26-04 compliance teams should prioritize these two for immediate assessment.

The remaining three — **ISC BIND (CVE-2015-5477)**, **Apache Struts (CVE-2016-3081)**, and **Strapi (CVE-2023-22894)** — round out a week dominated by retroactive enforcement of old vulnerabilities on infrastructure that organizations assumed was already remediated. The Strapi entry is particularly noteworthy: rated medium at CVSS 4.9 in isolation, it chains with CVE-2023-22621 for full RCE and affects software that may already be end-of-life, meaning vendors will not issue patches. If your organization runs any self-hosted Strapi instance, the recommended action is upgrade or decommission — not patch.
