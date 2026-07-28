# AppSec Review — 2026-07-28

**Reviewer:** Robert Flores, CISSP  
**Date:** 2026-07-28  
**CVEs Reviewed:** 2  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog

---

## Severity Breakdown

| Priority  | Count |
|-----------|-------|
| Critical  | 1     |
| High      | 0     |
| Medium    | 1     |
| Low       | 0     |
| **Total** | **2** |

---

## CVE Summary

| CVE ID           | Vendor   | Product                   | Priority | Vuln Class              |
|------------------|----------|---------------------------|----------|-------------------------|
| CVE-2026-16812   | Arista   | VeloCloud Orchestrator    | critical | OS Command Injection    |
| CVE-2025-68686   | Fortinet | FortiOS                   | medium   | Information Disclosure  |

---

## CVE Details

**CVE-2026-16812 — Arista VeloCloud Orchestrator (CVSS 10.0, CWE-78)**  
OS command injection in the on-prem VeloCloud SD-WAN orchestrator allows a remote, unauthenticated attacker to execute privileged OS commands, fully compromising confidentiality, integrity, and availability of the orchestrator and all managed data. CVSS 10.0; VeloCloud Orchestrators are internet-facing SD-WAN management planes, making this a critical initial access vector for network infrastructure. CISA due date: 2026-07-30 — immediate patching required.

**CVE-2025-68686 — Fortinet FortiOS (CVSS 5.9, CWE-200)**  
Information disclosure vulnerability that allows a remote unauthenticated attacker to bypass the patch for FortiOS's symbolic link persistence mechanism via crafted HTTP requests. Exploitation requires prior filesystem-level compromise through a separate vulnerability, making this a post-exploit persistence bypass rather than an initial access vector. Despite the unauthenticated HTTP trigger, the dependency on prior compromise limits real-world severity.

---

## Trend Analysis

This week's KEV additions highlight two converging themes in 2026 threat activity: SD-WAN and network orchestration platforms as high-value targets, and the persistence of post-exploit bypass techniques targeting previously patched vulnerabilities. The Arista VeloCloud Orchestrator vulnerability is particularly concerning given the critical role SD-WAN orchestrators play in enterprise network topology — a full compromise of the VCO yields visibility into and control over an organization's entire SD-WAN fabric. Simultaneously, the Fortinet symbolic-link bypass (CVE-2025-68686) reflects an ongoing pattern where threat actors chain vulnerabilities: initial access through one CVE, then a bypass of defensive patches to maintain persistence. Both CISA's short remediation windows (Arista: 3 days, Fortinet: 14 days) underscore the urgency of patching network infrastructure components before ransomware operators or nation-state actors exploit these footholds at scale.

---

## Blog Post Candidates

1. **"CVSS 10.0: How Arista VeloCloud Orchestrator Command Injection Can Compromise Your Entire SD-WAN"** — Deep dive into CWE-78 exploitation paths in network management planes, with patch guidance and detection opportunities.
2. **"Patch Bypass: How Threat Actors Extend FortiOS Persistence After Initial Remediation"** — Explores the symbolic link persistence technique CISA flagged in CVE-2025-68686 and what defenders need beyond simply applying vendor patches.
3. **"SD-WAN Security: Why Orchestrators Are the New Firewall Targets"** — Broader piece on the trend of network management platforms appearing in the KEV catalog and how to reduce attack surface.

---

## Newsletter Snippet

**This Week in CISA KEV (2026-07-28):** CISA added two new vulnerabilities to the Known Exploited Vulnerabilities catalog, with Arista's VeloCloud Orchestrator commanding immediate attention. CVE-2026-16812 carries a perfect CVSS 10.0 score — a remote, unauthenticated OS command injection that can fully compromise the SD-WAN orchestrator and all networks it manages. Federal agencies have until July 30th to patch, making this a three-day remediation window. Also added: CVE-2025-68686 in Fortinet FortiOS, a medium-severity symbolic link bypass that lets attackers maintain persistence after a prior compromise, even if the original entry-point vulnerability was patched.

If you run Arista VeloCloud Orchestrator on-premises, drop everything and patch now — CVSS 10.0 vulnerabilities in internet-facing network management systems represent some of the highest-risk exposures possible. For Fortinet shops, CVE-2025-68686 is a reminder that patching isn't always sufficient: if you've experienced a prior FortiOS compromise, forensic triage per CISA's BOD 26-04 guidance is essential to confirm no persistent footholds remain. Both vendors have published advisories; links are in this week's vulnerability roundup on FixTheVuln.com.
