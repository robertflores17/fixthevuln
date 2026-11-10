# AppSec Review — 2026-11-10

**Reviewer:** Robert Flores, CISSP  
**Date:** 2026-11-10  
**CVEs Reviewed:** 4  
**All Approved for Publication**

---

## Severity Breakdown

| Priority | Count |
|----------|-------|
| Critical | 4     |
| High     | 0     |
| Medium   | 0     |
| Low      | 0     |

---

## CVE Summary

| CVE ID            | Vendor      | Product         | Priority | Vuln Class                       | CVSS |
|-------------------|-------------|-----------------|----------|----------------------------------|------|
| CVE-2026-102895   | GPUStack     | GPUStack        | critical | Improper Authentication / Unauth RCE | 9.8  |
| CVE-2026-123158   | OpenBSD      | OpenSSH         | critical | Authentication Bypass            | 8.1  |
| CVE-2026-116779   | SignalWire   | FreeSwitch      | critical | Code Injection / RCE             | 9.8  |
| CVE-2026-123218   | IBM          | Aspera Faspex   | critical | Incorrect Authorization / Priv Esc | 9.8  |

---

## Trend Analysis

This batch is notable for targeting foundational infrastructure components across three distinct categories: AI/ML compute platforms, remote access protocols, and enterprise file transfer. The GPUStack and OpenSSH vulnerabilities reflect a continued attacker focus on seizing control of AI and cloud-adjacent infrastructure — GPUStack's unauthenticated admin access with code execution via POST endpoint is especially concerning as GPU-backed inference platforms become operational targets. The OpenSSH authentication bypass is arguably the most systemic risk in the batch: SSH is the backbone of server administration worldwide, and a Linux-platform authentication bypass with active exploitation confirmed by CISA KEV status warrants emergency patching response. FreeSwitch and IBM Aspera Faspex round out a batch that spans VoIP/telecom and enterprise data transfer — both high-value attack surfaces for lateral movement and data exfiltration. All four vulnerabilities have CVSS scores at or above 8.1, with three at the ceiling of 9.8, underscoring an unusually severe batch with no medium or low-priority entries.

---

## Blog Post Candidates

1. **"SSH at Risk Again: What the OpenSSH Auth Bypass (CVE-2026-123158) Means for Every Linux Administrator"** — High-traffic angle given OpenSSH's universal deployment; covers detection, patching, and audit steps.

2. **"AI Infrastructure Under Attack: GPUStack's Unauthenticated RCE and the Security Debt in ML Platforms"** — Timely piece on the emerging threat surface of GPU inference servers as orgs rush to deploy LLM workloads without hardening.

3. **"Code Injection in VoIP: FreeSwitch CVE-2026-116779 and What Telecom Engineers Need to Know"** — Niche but high-relevance for security teams managing telecom infrastructure; pairs well with existing KEV coverage.

---

## Newsletter Snippet

This week's CISA KEV additions are a critical-only batch — four vulnerabilities, all rated Critical, spanning AI compute, remote access, enterprise file transfer, and VoIP. The headline is CVE-2026-123158, an authentication bypass in OpenBSD OpenSSH on Linux: if your Linux fleet exposes SSH (and it almost certainly does), this is an emergency patch, not a "schedule it next sprint" situation. Alongside it, CVE-2026-102895 in GPUStack allows completely unauthenticated administrative access and remote code execution — a stark reminder that the rush to deploy AI infrastructure is outpacing security hardening.

For enterprise and telecom teams, CVE-2026-116779 (FreeSwitch code injection) and CVE-2026-123218 (IBM Aspera Faspex privilege escalation) round out a week where attackers are clearly probing for high-value lateral movement paths. All four are confirmed actively exploited per CISA KEV. Prioritize patching OpenSSH and GPUStack immediately; FreeSwitch and Aspera Faspex upgrades should follow within the BOD 26-04 three-day window. Full technical details and remediation links are live at fixthevuln.com.
