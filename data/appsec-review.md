# AppSec Review — CISA KEV Batch
**Date:** 2026-04-21
**Reviewer:** Robert Flores, CISSP
**CVEs Reviewed:** 8
**Pipeline Run:** generate_html → entity_extractor → generate_cve_pages → generate_cve_social → generate_llms_txt → propagate (403 host-allowlist error, non-blocking)

---

## Severity Breakdown

| Priority | Count |
|----------|-------|
| Critical | 1     |
| High     | 3     |
| Medium   | 3     |
| Low      | 1     |
| **Total**| **8** |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2025-32975 | Quest (KACE SMA) | critical | Authentication bypass (unauthenticated user impersonation) |
| CVE-2025-2749 | Kentico (Xperience) | high | Path traversal / arbitrary file upload |
| CVE-2023-27351 | PaperCut (NG/MF) | high | Authentication bypass |
| CVE-2024-27199 | JetBrains (TeamCity) | high | Relative path traversal |
| CVE-2026-20122 | Cisco (Catalyst SD-WAN Manager) | medium | Privileged API abuse / arbitrary file write |
| CVE-2026-20133 | Cisco (Catalyst SD-WAN Manager) | medium | Information disclosure |
| CVE-2025-48700 | Synacor (Zimbra ZCS) | medium | Cross-site scripting |
| CVE-2026-20128 | Cisco (Catalyst SD-WAN Manager) | low | Insecure credential storage (local only) |

---

## Trend Analysis

This batch is headlined by CISA's Emergency Directive 26-03 targeting Cisco Catalyst SD-WAN Manager, with three separate CVEs (CVE-2026-20122, CVE-2026-20133, CVE-2026-20128) covering a cluster of weaknesses — file-handling API abuse, information disclosure, and plaintext credential recovery — reflecting CISA's increasing willingness to bundle related vulnerabilities under a single directive when an attack chain is observed in the wild. The standout entry is CVE-2025-32975 in Quest KACE SMA, a CVSS 10.0 authentication bypass on an endpoint management appliance: attackers who compromise an SMA instance gain a trusted foothold capable of pushing malicious packages to every managed endpoint in the organization, making this a supply-chain-adjacent risk well beyond its individual CVSS score. Two legacy CVEs — PaperCut CVE-2023-27351 (2023 vintage) and JetBrains TeamCity CVE-2024-27199 (2024 vintage) — appearing in the KEV in April 2026 confirm that threat actors are actively returning to unpatched instances of these widely deployed DevOps and print-management platforms, consistent with patterns observed in ransomware and state-sponsored intrusion campaigns from 2023–2024 that never fully burned out.

---

## Blog Post Candidates

1. **"CISA ED-26-03: What the Cisco SD-WAN Emergency Directive Means for Network Teams"** — A practitioner-focused breakdown of the three CVEs covered by the directive, the attack chain they enable together, and actionable triage steps per the CISA Hunt & Hardening Guidance.

2. **"CVSS 10.0 in Your Endpoint Manager: Quest KACE SMA and the Risk of Trusting Your Management Plane"** — Deep-dive on CVE-2025-32975, exploring how authentication bypasses on management appliances translate into organization-wide compromise and what a zero-trust segmentation posture looks like for IT management infrastructure.

3. **"Why 2023's PaperCut Bugs Are Still Pwning Networks in 2026"** — Analysis of CVE-2023-27351's return to active exploitation, covering patch fatigue, the economics of targeting print-management systems, and detection guidance using SIEM signatures for SecurityRequestFilter bypass attempts.

---

## Newsletter Snippet

**This week CISA added 8 new vulnerabilities to the Known Exploited Vulnerabilities catalog**, including a CVSS 10.0 authentication bypass in Quest KACE Systems Management Appliance (CVE-2025-32975) that allows unauthenticated attackers to impersonate any user — a critical risk for organizations relying on KACE to manage their entire endpoint fleet. Three additional CVEs in Cisco Catalyst SD-WAN Manager (CVE-2026-20122, CVE-2026-20133, CVE-2026-20128) were added under CISA Emergency Directive 26-03, signaling that active exploitation of SD-WAN management planes is underway and federal agencies face a tight remediation deadline of April 23, 2026.

Also notable this week: PaperCut NG/MF (CVE-2023-27351) and JetBrains TeamCity (CVE-2024-27199) both returned to the KEV despite being two to three years old, a reminder that attackers routinely revisit proven vulnerabilities in widely-deployed enterprise tooling long after initial disclosure. If your organization hasn't patched these platforms, patch now — CISA's inclusion confirms these CVEs are under active, real-world exploitation today. Full details and remediation guidance for all 8 CVEs are available on fixthevuln.com.
