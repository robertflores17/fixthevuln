# AppSec Review — 2026-11-26

**Reviewer:** Robert Flores, CISSP  
**Review Date:** 2026-11-26  
**CVEs Reviewed:** 10  
**Source:** CISA KEV (dateAdded: 2026-11-25)

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 5 | CVE-2026-103406, CVE-2026-133469, CVE-2026-133303, CVE-2026-133323, CVE-2026-133303 |
| High | 3 | CVE-2025-41450, CVE-2023-25914, CVE-2023-25915 |
| Medium | 3 | CVE-2026-133324, CVE-2026-133275, CVE-2026-133311 |
| Low | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-103406 | Hewlett Packard Enterprise (HPE) / Juniper | critical | OS Command Injection (RCE as root) |
| CVE-2026-133469 | Vates | critical | Authentication Bypass (empty JSON token → admin) |
| CVE-2026-133303 | Mitel | critical | XML Injection → Arbitrary Command Execution |
| CVE-2026-133323 | Mitel | critical | OS Command Injection (Unauthenticated RCE) |
| CVE-2025-41450 | Danfoss | high | Improper Authentication (OT/ICS info disclosure) |
| CVE-2023-25914 | Danfoss | high | Path Traversal (legacy CVE, OT/ICS exploitation) |
| CVE-2023-25915 | Danfoss | high | Improper Input Validation (remote command execution) |
| CVE-2026-133324 | Mitel | medium | Authentication Bypass (conferencing AWV component) |
| CVE-2026-133275 | Mitel | medium | Unrestricted File Upload (unauthenticated) |
| CVE-2026-133311 | Mitel | medium | Weak Authentication (sensitive info disclosure) |

---

## Trend Analysis

This batch highlights two converging attack surfaces that defenders should treat as priority patches. First, enterprise unified communications and collaboration platforms remain a persistent target: five of the ten CVEs are in Mitel MiCollab's Audio, Web and Video Conferencing (AWV) component, spanning the full exploit chain from unauthenticated information disclosure through file upload to outright OS command injection. The two critical-severity Mitel entries (CVE-2026-133303 and CVE-2026-133323) together provide an unauthenticated pre-auth RCE pathway, making unpatched MiCollab deployments internet-facing attack surface requiring immediate action. Second, the three legacy Danfoss AK-SM 800A entries (two from 2023, one from 2025) underscore CISA's renewed focus on OT/ICS equipment: CISA adding 2023-era CVEs to the KEV in late 2026 signals active, ongoing exploitation in industrial and retail/HVAC control environments — organizations running this hardware in refrigeration, HVAC, or food retail settings should treat the 3-day due dates seriously even for the 2023 entries.

---

## Blog Post Candidates

1. **"The MiCollab AWV Attack Chain: Five CVEs, One Pre-Auth RCE Path"** — Walk through how CVE-2026-133303 (XML injection) and CVE-2026-133323 (OS command injection) combine with the auth bypass and file upload flaws to create a complete unauthenticated compromise chain in Mitel's conferencing stack.

2. **"Why CISA Is Adding 2023 CVEs to KEV in 2026: The Danfoss ICS Story"** — Explain the lag between CVE assignment and KEV listing for OT/ICS devices, and what it means for critical infrastructure operators running AK-SM 800A controllers in food retail and HVAC environments.

3. **"Hypervisor Management Platform Auth Bypass: CVE-2026-133469 in Vates Xen Orchestra"** — Deep dive on the empty JSON object authentication bypass, how it maps to CWE-287/1287, and what it means for organizations running Xen-based virtualization without network segmentation on the management plane.

---

## Newsletter Snippet

This week's CISA KEV batch is dominated by two vendors — Mitel and Danfoss — with a combined eight entries across collaboration and industrial control systems. The standout is Mitel MiCollab, where five vulnerabilities in a single product's conferencing component (AWV) form a layered attack chain: unauthenticated attackers can bypass authentication, upload arbitrary files, and ultimately execute OS commands without credentials. With CVSS scores ranging from 5.3 to 9.8, the full severity of this cluster is only apparent when the chain is viewed together — any MiCollab deployment exposed to the internet should be patched or taken offline until mitigations are applied.

Also notable this week: CISA added two 2023-era Danfoss AK-SM 800A vulnerabilities (path traversal and remote command execution) with the same 3-day remediation deadline as the newer entries. This signals active, ongoing exploitation in operational technology environments — likely refrigeration and HVAC controllers in food retail and industrial facilities — where patching cycles are notoriously slow. If your organization operates this equipment, treat the legacy CVE dates as irrelevant: the active exploitation is happening now.
