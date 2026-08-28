# AppSec Review — 2026-08-28

**Reviewer:** Robert Flores, CISSP  
**CVEs Reviewed:** 10  
**Review Date:** 2026-08-28

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 3 | CVE-2023-49105, CVE-2026-8452, CVE-2026-60004 |
| High | 5 | CVE-2026-53362, CVE-2021-23758, CVE-2015-5287, CVE-2022-0995, CVE-2019-1068 |
| Medium | 2 | CVE-2026-66384, CVE-2015-3246 |
| Low | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2023-49105 | ownCloud | Critical | Auth Bypass (Improper Authentication) |
| CVE-2026-53362 | Linux | High | Privilege Escalation (Heap Buffer Overflow, IPv6) |
| CVE-2026-66384 | JFrog | Medium | Path Traversal (CWE-22) |
| CVE-2021-23758 | Ajax.NET Professional | High | RCE (Unsafe Deserialization) |
| CVE-2015-3246 | Red Hat | Medium | LPE / Race Condition (CWE-367) |
| CVE-2015-5287 | Red Hat | High | LPE / Symlink Attack (CWE-59) |
| CVE-2022-0995 | Linux | High | LPE / Memory Corruption (OOB Write) |
| CVE-2026-8452 | Citrix | Critical | Memory Corruption / DoS (CWE-119, CVSS 9.8) |
| CVE-2019-1068 | Microsoft | High | RCE (SQL Server, CWE-20) |
| CVE-2026-60004 | Gitea | Critical | Code Injection / RCE (CWE-94) |

---

## Trend Analysis

This batch reflects two converging trends CISA has been accelerating in 2026. First, infrastructure and developer-tooling targets are increasingly prominent — Citrix NetScaler (CVE-2026-8452), Gitea (CVE-2026-60004), JFrog Artifactory (CVE-2026-66384), and ownCloud (CVE-2023-49105) are all platforms that appear in CI/CD pipelines or organizational file-sharing workflows, making them high-value pivot points for supply chain and lateral movement attacks. Second, the batch contains an unusually high proportion of legacy CVEs (2015, 2019, 2021) added now under BOD 26-04's expanded forensics triage requirements — a strong signal that federal agencies and their contractors are encountering these vulnerabilities in active incident response, not merely theoretical exposure. Red Hat libuser (2015), ABRT (2015), and AjaxPro (2021) all appear on end-of-life software still running in hardened government and enterprise enclaves, and their KEV additions confirm threat actors know exactly where to look when orgs have not managed legacy debt.

---

## Blog Post Candidates

1. **"The Return of the Dead: Why 10-Year-Old CVEs Are Back on CISA's KEV"** — Explores the 2015 Red Hat libuser and ABRT entries alongside AjaxPro 2021, examining how BOD 26-04 forensics requirements are surfacing exploitation of legacy software that organizations assumed was safely isolated.

2. **"Gitea and ownCloud: Self-Hosted Infrastructure Under Siege"** — Covers CVE-2026-60004 and CVE-2023-49105 together, focusing on why self-managed Git and file-sharing platforms are attractive KEV targets and what developer teams running on-prem tools must do differently.

3. **"Citrix NetScaler's Second Act: Another CVSS 9.8 on Network Edge Devices"** — A deep dive on CVE-2026-8452, placing it in the context of Citrix's persistent presence in the KEV catalog and what network-edge memory corruption vulnerabilities mean for zero-trust architecture.

---

## Newsletter Snippet

**CISA added 10 new vulnerabilities to the Known Exploited Vulnerabilities catalog this week, spanning critical infrastructure, Linux kernel, and developer platforms.** Three entries earned a critical priority: ownCloud's authentication bypass (CVE-2023-49105, CVSS 9.8) allows unauthenticated file access, Citrix NetScaler's memory corruption flaw (CVE-2026-8452, CVSS 9.8) targets widely-deployed network edge devices, and Gitea's code injection (CVE-2026-60004, CVSS 9.8) lets any repository contributor plant executable Git hooks and run shell commands as the service account. Five more entries are rated high, including two Linux kernel privilege escalation vulnerabilities and a Microsoft SQL Server RCE from 2019 that remains unpatched across enterprise deployments.

Notably, two entries date to 2015 — Red Hat libuser (CVE-2015-3246) and ABRT (CVE-2015-5287) — signaling that federal incident response teams are encountering these vulnerabilities in real compromises today, not just in vulnerability scanners. Organizations still running RHEL 6-era environments or legacy .NET applications with AjaxPro (CVE-2021-23758) should treat these KEV additions as confirmation of active exploitation, not a theoretical risk. All ten CVEs carry BOD 26-04 patching deadlines between August 28 and September 10, 2026.
