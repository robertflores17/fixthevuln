# AppSec Review — 2026-10-17

**Reviewer:** Robert Flores, CISSP  
**CVEs Reviewed:** 2  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog

---

## Severity Breakdown

| Priority | Count |
|----------|-------|
| Critical | 1     |
| High     | 0     |
| Medium   | 1     |
| Low      | 0     |
| **Total**| **2** |

---

## CVE Summary

| CVE ID           | Vendor      | Priority | Vulnerability Class            |
|------------------|-------------|----------|--------------------------------|
| CVE-2026-102764  | BeyondTrust | critical | Authentication Bypass (CWE-290)|
| CVE-2025-61624   | Fortinet    | medium   | Path Traversal (CWE-22)        |

---

## Trend Analysis

This batch highlights two persistent themes in the CISA KEV catalog: privileged access management (PAM) platforms and Fortinet network infrastructure remain high-value targets for threat actors. BeyondTrust Remote Support's critical authentication bypass (CVSS 9.3) is consistent with a pattern of attackers targeting PAM and remote-access tooling — a trend accelerated since 2024 as nation-state and ransomware groups seek persistent, high-privilege footholds in enterprise environments. The Fortinet path traversal vulnerability, while requiring admin-level authentication, reflects continued active exploitation of Fortinet's broad product portfolio (FortiOS, FortiPAM, FortiProxy, FortiSwitchManager); CISA adding a 2025-era CVE in October 2026 strongly suggests newly confirmed in-the-wild exploitation, consistent with Fortinet's well-documented history of delayed exploitation timelines and government network targeting.

---

## Blog Post Candidates

1. **"Why PAM Tools Are the New Crown Jewels: BeyondTrust KEV Addition Explained"** — Examines how BeyondTrust Remote Support joins a growing list of PAM tools (CyberArk, Ivanti, ConnectWise ScreenConnect) actively targeted by threat actors, and what defenders should do when the keys to the kingdom have a known auth bypass.

2. **"The Long Tail of Fortinet Exploits: When CISA Adds a 2025 CVE in 2026"** — Explores why Fortinet vulnerabilities keep showing up in the KEV catalog long after initial disclosure, and the organizational risk of assuming patched equals safe.

3. **"BOD 26-04 and the 3-Day Patch Window: Is Your Team Ready?"** — Both CVEs this batch carry a 3-day CISA remediation deadline under BOD 26-04, raising the question of whether most organizations can operationalize that timeline.

---

## Newsletter Snippet

**Two new CISA KEV additions this week demand immediate attention.** BeyondTrust Remote Support is carrying a critical (CVSS 9.3) authentication bypass vulnerability — CVE-2026-102764 — that allows unauthenticated remote attackers to perform file operations on the appliance. If your organization uses BeyondTrust Remote Support, treat this as a fire drill: patch now, review your forensic triage posture per CISA's BOD 26-04 guidance, and verify no indicators of compromise exist on affected appliances. The 3-day remediation window (due 2026-10-19) is not aspirational — it's a federal mandate for agencies and a strong benchmark for everyone else.

The second addition, CVE-2025-61624, covers a path traversal vulnerability across Fortinet's FortiOS, FortiPAM, FortiProxy, and FortiSwitchManager product lines. While it requires authenticated admin access to exploit, CISA's decision to add a 2025 CVE to the KEV catalog in late 2026 signals confirmed active exploitation in the wild — likely by threat actors who already have admin credentials via prior compromise. Organizations running any of these Fortinet products should apply vendor patches immediately and audit admin-level CLI access logs for anomalous file write or delete activity.
