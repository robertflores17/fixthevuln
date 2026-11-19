# AppSec Review — 2026-11-19

**Reviewer:** Robert Flores, CISSP  
**Date:** 2026-11-19  
**CVEs Reviewed:** 4  
**All Approved:** Yes (CISA KEV = confirmed actively exploited)

---

## Severity Breakdown

| Priority  | Count | CVEs |
|-----------|-------|------|
| Critical  | 3     | CVE-2024-10441, CVE-2026-90817, CVE-2026-90436 |
| High      | 1     | CVE-2026-40217 |
| Medium    | 0     | — |
| Low       | 0     | — |

---

## CVE Inventory

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2024-10441 | Synology | critical | Improper Output Encoding / RCE |
| CVE-2026-40217 | BerriAI (LiteLLM) | high | Unprotected Alternate Channel + Code Injection / RCE |
| CVE-2026-90817 | Vanderbilt University (REDCap) | critical | Code Injection / Unauthenticated RCE |
| CVE-2026-90436 | Apache | critical | Unsafe Reflection / RCE |

---

## Trend Analysis

This batch is dominated by unauthenticated remote code execution vulnerabilities (3 of 4 entries, all CVSS 9.8), reflecting a continued CISA focus on the most severe pre-auth attack surface. Notably, two entries target infrastructure that is difficult to rapidly patch: Apache Axis is explicitly flagged as end-of-life with no upstream patch available, while REDCap is a tightly version-controlled research platform deployed across healthcare and academic networks. The Synology DSM entry is a 2024 CVE only recently added to the KEV, strongly suggesting threat actor activity against NAS devices accelerated in late 2026 — consistent with the persistent ransomware interest in network-attached storage appliances. The LiteLLM entry is the most forward-looking: it represents the first AI/ML infrastructure platform to appear in this feed, underscoring that LLM API gateways and guardrail endpoints are becoming an active attack surface as organizations scale AI deployments without commensurate security review of the supporting middleware stack.

---

## Blog Post Candidates

1. **"The EoL Problem: Why Apache Axis in CISA KEV Signals a Legacy Debt Crisis"** — Deep dive on how end-of-life SOAP/XML frameworks remain embedded in enterprise Java middleware years after vendor support ends, and what organizations can do short of a full re-platform.

2. **"AI Infrastructure Under Fire: LiteLLM's /guardrails Endpoint and the Hidden Attack Surface of LLM Gateways"** — Explores how AI gateway products like LiteLLM introduce novel RCE vectors through code execution endpoints designed for custom guardrail logic, and what secure-by-default patterns should look like.

3. **"NAS Ransomware Targeting Escalates: Synology DSM Joins the KEV"** — Analysis of CISA's addition of a 2024 Synology vulnerability in late 2026, the threat actor patterns behind NAS targeting, and backup/segmentation guidance for SMB and enterprise environments.

---

## Newsletter Snippet

CISA added four new vulnerabilities to its Known Exploited Vulnerabilities catalog this week, all confirmed as actively exploited in the wild. Three carry CVSS scores of 9.8 and enable unauthenticated remote code execution: Synology DiskStation Manager (NAS appliances), Vanderbilt REDCap (healthcare research data platform), and Apache Axis (a widely-deployed but end-of-life SOAP framework). A fourth entry — BerriAI LiteLLM (CVSS 8.8) — marks the first AI/ML infrastructure product to appear in the KEV catalog, exploiting a code injection flaw in the guardrails API endpoint.

Federal agencies under BOD 26-04 must remediate the Synology, REDCap, and Apache Axis entries by **2026-11-21**, and the LiteLLM entry by **2026-12-02**. Organizations not subject to BOD 26-04 should treat all four as urgent given confirmed exploitation. The Apache Axis entry is particularly difficult to address quickly — it is end-of-life with no vendor patch, requiring organizations to audit their Java middleware stack for embedded copies and prioritize migration or isolation of affected services.
