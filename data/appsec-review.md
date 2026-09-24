# AppSec Review — 2026-09-24

**Reviewer:** Robert Flores, CISSP  
**Pipeline run:** Automated scheduled review  
**CVEs reviewed:** 4  
**All approved:** Yes (CISA KEV = confirmed actively exploited)

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 4     | CVE-2026-93952, CVE-2026-94127, CVE-2026-93616, CVE-2026-85102 |
| High     | 0     | — |
| Medium   | 0     | — |
| Low      | 0     | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-93952 | Arista | critical | Improper Input Validation (CWE-20) — unauth access to privileged internals, CVSS 10.0 |
| CVE-2026-94127 | F5 | critical | Heap-based Buffer Overflow / RCE (CWE-122) — unauth RCE via OAuth+APM, CVSS 9.8 |
| CVE-2026-93616 | Check Point | critical | Path Traversal / RCE (CWE-22) — unauth arbitrary script upload/exec on mgmt plane, CVSS 9.8 |
| CVE-2026-85102 | Check Point | critical | Improper Certificate Validation / RCE (CWE-295) — unauth RCE via VPN cert bypass, CVSS 9.8 |

---

## Trend Analysis

This batch reflects a sharp focus by threat actors on **network security infrastructure** — SD-WAN orchestrators, application delivery controllers, security gateways, and management servers are all represented. Three of the four vulnerabilities allow unauthenticated remote code execution, and the fourth (Arista VCO) achieves a perfect CVSS 10.0 through unauthorized access to privileged orchestration functionality that can cascade to every managed network edge. Check Point's dual entries in a single KEV batch are particularly notable: path traversal against management servers combined with certificate validation bypass on perimeter gateways creates a compound attack surface where an adversary can potentially compromise both the enforcement layer and its control plane simultaneously. Organizations with Check Point environments should treat these as a coordinated exposure pair and prioritize both patches together rather than addressing them sequentially.

---

## Blog Post Candidates

1. **"When the Security Stack Is the Attack Surface: Lessons from the 2026-09-22 KEV Batch"** — Deep dive into how attackers pivot from compromising perimeter security products (Check Point gateways + management servers) to achieving full network control; includes detection and hardening guidance.
2. **"F5 BIG-IP OAuth RCE (CVE-2026-94127): How Heap Overflows Survive Modern Mitigations"** — Technical breakdown of the heap-based buffer overflow in BIG-IP APM and why OAuth feature interactions create unexpected attack surface on enterprise ADCs.
3. **"SD-WAN Orchestrators as High-Value Targets: The CVSS 10.0 Arista VeloCloud Story"** — Analysis of why network orchestration platforms represent asymmetric risk and what defenders should monitor post-exploitation.

---

## Newsletter Snippet

**4 Critical CVEs Added — Network Infrastructure Under Siege**

CISA's latest KEV additions (2026-09-22) are a stark reminder that the devices securing enterprise networks are themselves prime targets. This batch includes a CVSS 10.0 improper input validation flaw in Arista's VeloCloud SD-WAN Orchestrator that grants unauthenticated attackers access to privileged internal functionality, an unauthenticated RCE in F5 BIG-IP APM via heap overflow when OAuth is configured, and two Check Point vulnerabilities — one allowing unauthenticated arbitrary script execution on management servers via path traversal, and another enabling unauthenticated RCE through improper certificate validation in VPN configurations. All four carry CVSS scores of 9.8 or higher and have been confirmed as actively exploited in the wild.

If your organization runs any of these products, treat the CISA due date of 2026-09-25 as non-negotiable. Federal agencies are required to patch under BOD 26-04 and must also follow CISA's Forensics Triage Requirements before applying patches — meaning you should assume compromise and collect forensic artifacts first. For the Check Point entries in particular, consider both CVEs a paired exposure: attackers who can execute scripts on your management server and bypass certificate validation on your gateway have effectively owned your entire perimeter enforcement layer. Consult vendor advisories for interim iRules and mitigations where final patches are still pending.
