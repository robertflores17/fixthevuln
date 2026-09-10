# AppSec Review — CISA KEV Batch

**Date:** 2026-09-10  
**Reviewer:** Robert Flores, CISSP  
**CVE Count:** 4  
**CISA KEV dateAdded:** 2026-09-08  

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 2 | CVE-2026-75650, CVE-2026-86218 |
| High | 2 | CVE-2026-81963, CVE-2026-85880 |
| Medium | 0 | — |
| Low | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Product | Priority | Vuln Class | CVSS |
|--------|--------|---------|----------|------------|------|
| CVE-2026-75650 | Adobe | Commerce / Magento | Critical | Template Engine Injection / RCE | 10.0 |
| CVE-2026-86218 | N-able | N-central | Critical | Static Code Injection / Pre-auth RCE | 9.8 |
| CVE-2026-81963 | Microsoft | Windows Update Stack | High | Link Following / LPE to SYSTEM | 7.8 |
| CVE-2026-85880 | Microsoft | Windows ALPC | High | Heap Buffer Overflow / LPE | 7.8 |

---

## Trend Analysis

This batch reflects two converging attack surface trends. First, high-value platform targets: Adobe Commerce (Magento) and N-able N-central are both infrastructure-critical systems with broad deployment — Magento powers a significant slice of global e-commerce, while N-able N-central is an MSP platform whose compromise gives attackers supply-chain reach into downstream customer environments. Both carry pre-authentication RCE, making them prime targets for initial access brokers and ransomware operators seeking fast, scalable entry. Second, Windows local privilege escalation via memory-corruption and symlink primitives continues to trend as a post-exploitation staple, with two separate ALPC/Update-Stack LPE bugs added in the same KEV batch — suggesting active chaining with existing initial-access vectors, likely in ransomware or targeted intrusion campaigns where attackers already have limited foothold and need SYSTEM.

---

## Blog Post Candidates

1. **"Supply Chain at Risk: Why CVE-2026-86218 in N-able N-central Is a Five-Alarm Fire"** — Deep-dive on MSP platform exploitation, how a single N-central compromise cascades to managed customer networks, and what MSPs need to do right now.

2. **"Template Injection to CVSS 10: Dissecting the Adobe Commerce/Magento RCE Chain"** — Technical walkthrough of CWE-1336 (improper neutralization in template engines), why Magento's server-side rendering surface is persistently dangerous, and hardening recommendations for e-commerce operators.

3. **"The LPE Treadmill: Two Windows Privilege Escalation Bugs in One KEV Batch"** — Pattern analysis of Windows ALPC and Update Stack as recurring exploit targets, attacker post-exploitation playbooks, and the case for aggressive Patch Tuesday SLA enforcement.

---

## Newsletter Snippet

**September 10, 2026 — KEV Watch**

CISA added four actively exploited vulnerabilities to the Known Exploited Vulnerabilities catalog this week, with two reaching critical severity. Adobe Commerce and Magento are affected by a template engine injection flaw (CVE-2026-75650, CVSS 10.0) that enables unauthenticated remote code execution — if you run Magento, patch immediately with no exceptions. N-able N-central carries an equally alarming pre-authentication RCE via static code injection (CVE-2026-86218, CVSS 9.8); given N-central's role as an MSP management hub, exploitation of this vulnerability can provide attackers with direct pathways into managed customer environments at scale. Federal agencies face a September 11 remediation deadline for both.

Rounding out the batch, two Microsoft Windows local privilege escalation vulnerabilities — a link-following flaw in the Windows Update Stack (CVE-2026-81963) and a heap buffer overflow in the Advanced Local Procedure Call subsystem (CVE-2026-85880), both CVSS 7.8 — underscore the continued value of Windows LPE exploits as post-exploitation tools. Attackers routinely chain these with commodity initial-access techniques to reach SYSTEM-level control, making timely Windows patching a critical control even for organizations with strong perimeter defenses. Apply the relevant Microsoft security updates from the September 2026 Patch Tuesday cycle promptly.
