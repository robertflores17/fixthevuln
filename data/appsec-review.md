# AppSec Review — 2026-10-24

**Reviewer:** Robert Flores, CISSP  
**Pipeline run:** 2026-10-24  
**CVEs reviewed:** 1  

---

## Severity Breakdown

| Priority | Count |
|----------|-------|
| Critical | 1     |
| High     | 0     |
| Medium   | 0     |
| Low      | 0     |
| **Total**| **1** |

---

## CVE Summary

| CVE ID | Vendor | Product | Priority | Vulnerability Class |
|--------|--------|---------|----------|---------------------|
| CVE-2026-114625 | Arista | VeloCloud Orchestrator | Critical | SQL Injection (CWE-89) |

---

## Trend Analysis

This cycle's addition reinforces an ongoing trend of critical-severity SQL injection vulnerabilities reaching CISA KEV in enterprise network infrastructure products. VeloCloud Orchestrator is a widely deployed SD-WAN management platform, and a CVSS 9.9 unauthenticated SQL injection at the orchestrator layer represents a worst-case scenario: an attacker who exploits this gains privileged access to all network policy, topology data, and credentials managed by the platform. The 3-day remediation window combined with BOD 26-04 forensics triage requirements signals confirmed active exploitation, likely by nation-state or sophisticated ransomware actors targeting enterprise network control planes. Organizations still running on-prem VeloCloud deployments should treat this as an emergency patch-or-isolate event.

---

## Blog Post Candidates

1. **"SQL Injection in the Control Plane: Why CVE-2026-114625 Is a Network-Wide Compromise"** — Walk through how a single SQL injection in an SD-WAN orchestrator can yield lateral movement paths across every branch site the platform manages.
2. **"CISA BOD 26-04 Forensics Triage: What It Means When CISA Asks for Evidence"** — Explainer on what the forensics triage requirement signals about the severity and breadth of active exploitation.
3. **"Enterprise SD-WAN Security Posture: Hardening VeloCloud Before the Next KEV"** — Practical guide to attack surface reduction for VeloCloud deployments including network segmentation, API access controls, and audit logging.

---

## Newsletter Snippet

**Critical SQL injection hits Arista VeloCloud Orchestrator — patch or isolate now.** CISA added CVE-2026-114625 to the Known Exploited Vulnerabilities catalog this week with an emergency 3-day remediation deadline under BOD 26-04. The vulnerability is a SQL injection (CVSS 9.9) in Arista's on-premises VeloCloud SD-WAN Orchestrator that allows remote attackers to access privileged internal functionality and fully compromise the orchestrator host, including all managed network configuration and data. CISA has also invoked forensics triage requirements, meaning agencies and critical infrastructure operators must collect evidence of potential exploitation — a strong indicator of confirmed in-the-wild activity against this target.

If your organization runs VeloCloud Orchestrator on-prem, treat this as an emergency. Apply the vendor patch immediately per [Arista Security Advisory 0199](https://www.arista.com/en/support/advisories-notices/security-advisory/24838-security-advisory-0199), or isolate the orchestrator management interface from internet-facing exposure while a patch window is arranged. Review orchestrator access logs for anomalous SQL error patterns or unexpected privilege escalation activity. Organizations that cannot patch within the window should follow BOD 26-04 cloud-service guidance and consider whether continued use of the on-prem product is operationally viable without compensating controls.
