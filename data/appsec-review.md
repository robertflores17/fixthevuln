# AppSec Review — 2026-05-07

**Reviewer:** Robert Flores, CISSP  
**Review Date:** 2026-05-07  
**CVEs Reviewed:** 2  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 1 | CVE-2026-0300 |
| High     | 1 | CVE-2026-6973 |
| Medium   | 0 | — |
| Low      | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-6973 | Ivanti | high | RCE via Improper Input Validation (CWE-20) |
| CVE-2026-0300 | Palo Alto Networks | critical | Unauthenticated RCE via Out-of-Bounds Write (CWE-787) |

---

## CVE Analysis

**CVE-2026-6973 — Ivanti Endpoint Manager Mobile (EPMM) (CVSS 7.2)**  
Improper input validation (CWE-20) enabling remote code execution by an authenticated admin-level user. Exploitation requires valid credentials, limiting the immediate attack surface compared to unauthenticated variants, but Ivanti EPMM has a persistent history of KEV-listed flaws making rapid patch adoption critical. CISA's 3-day remediation deadline signals active exploitation despite the authentication requirement.

**CVE-2026-0300 — Palo Alto Networks PAN-OS (CVSS 9.3)**  
Out-of-bounds write (CWE-787) in the User-ID Authentication Portal (Captive Portal) service enabling an unauthenticated attacker to execute arbitrary code with root privileges on PA-Series and VM-Series firewalls. Zero authentication barrier combined with root-level code execution on perimeter network security hardware represents maximum-severity enterprise risk. CISA recommends restricting or disabling the portal as an immediate workaround until vendor patches are applied.

---

## Trend Analysis

This batch reinforces two persistent themes in the current KEV landscape. First, Mobile Device Management and endpoint security platforms — particularly Ivanti — continue to be high-value attack targets, with exploitation chains frequently escalating from authenticated admin access to full system compromise through a series of chained vulnerabilities. Second, unauthenticated memory corruption vulnerabilities (CWE-787, out-of-bounds write) in network perimeter devices remain a critical threat; threat actors prioritize these because a single successful exploit grants persistent root-level access at the network boundary before any endpoint or EDR controls can respond. The combination of a 3-day and 4-day remediation deadline from CISA signals both are seeing active in-the-wild exploitation, likely by sophisticated adversaries including nation-state actors who have historically targeted both Ivanti and Palo Alto Networks infrastructure for initial access operations.

---

## Blog Post Candidates

1. **"Ivanti EPMM Again: Why MDM Platforms Are a Persistent Attack Surface"** — Examines the pattern of Ivanti KEV additions, covering why MDM platforms are high-value targets and what a defense-in-depth strategy looks like for organizations that can't immediately patch.

2. **"Firewall on Fire: Unauthenticated Root RCE in PAN-OS and What It Means for Your Perimeter"** — Deep dive into CWE-787 out-of-bounds write exploitation in network appliances, covering the CVE-2026-0300 attack surface, Palo Alto's workaround guidance, and detection strategies.

3. **"CISA's 72-Hour Clock: How to Operationalize KEV Remediation Deadlines"** — Practical guide on building a KEV-driven patching workflow, prioritizing critical/high findings, and meeting BOD 22-01 obligations for federal and compliance-adjacent organizations.

---

## Newsletter Snippet

**This week CISA added two new actively exploited vulnerabilities to the Known Exploited Vulnerabilities catalog, including a critical unauthenticated RCE in Palo Alto Networks PAN-OS (CVE-2026-0300, CVSS 9.3) affecting PA-Series and VM-Series firewalls, and a high-severity authenticated RCE in Ivanti Endpoint Manager Mobile (CVE-2026-6973, CVSS 7.2).** The PAN-OS vulnerability is particularly alarming — it requires no credentials and delivers root-level code execution on perimeter firewall hardware, meaning an attacker who reaches the Captive Portal service can own the network gateway entirely. CISA's remediation deadline of May 9th for the PAN-OS flaw underscores the urgency; if you operate Palo Alto firewalls with the User-ID Authentication Portal exposed, disabling the service is the recommended interim workaround until patches are applied.

For Ivanti EPMM, while exploitation requires administrative credentials, the platform's history as a repeat KEV target means organizations should treat this with the same urgency as unauthenticated flaws — credential theft and admin account compromise are frequently precursors to this class of attack. Both vulnerabilities reinforce the need for mature KEV tracking programs: organizations without a formal process to map CISA KEV additions to their asset inventory and patch within mandated windows are leaving confirmed, actively-exploited attack paths open. If you are a federal agency or BOD 22-01-bound organization, the May 9-10 deadlines are non-negotiable — prioritize now.
