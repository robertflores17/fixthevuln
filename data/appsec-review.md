# AppSec Review — 2026-05-22

**Reviewer:** Robert Flores, CISSP  
**Review Date:** 2026-05-22  
**CVEs Reviewed:** 2  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog  
**Pipeline Status:** All scripts completed (IndexNow 403 — host allowlist, non-blocking)

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 0     | —    |
| High     | 1     | CVE-2025-34291 |
| Medium   | 1     | CVE-2026-34926 |
| Low      | 0     | —    |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2025-34291 | Langflow | high | CORS Origin Validation / Credential Theft → RCE |
| CVE-2026-34926 | Trend Micro | medium | Directory Traversal / Code Injection |

---

## CVE Analysis

**CVE-2025-34291 — Langflow Origin Validation Error (CVSS 8.8, High)**  
Overly permissive CORS policy combined with a SameSite=None refresh token cookie lets a malicious web page silently exfiltrate authenticated session tokens cross-origin. Captured tokens grant access to Langflow's code-execution endpoints, enabling full system compromise. Widely adopted in enterprise AI pipelines, making this a high-value target for supply-chain-adjacent attacks; patch to v1.9.3 or later immediately.

**CVE-2026-34926 — Trend Micro Apex One Directory Traversal (CVSS 6.7, Medium)**  
A relative path traversal in Apex One's on-premise server allows a local pre-authenticated attacker to overwrite a key configuration table, injecting malicious code that propagates to every managed endpoint agent. The local attack vector constrains initial access, but the blast radius — code execution across an entire managed-endpoint fleet — makes patching urgent for any enterprise running Apex One on-prem; apply Trend Micro patch KA-0023430 immediately.

---

## Trend Analysis

This batch highlights two converging trends in 2026 KEV additions. First, AI/ML infrastructure (Langflow) is increasingly treated as a high-value exploit target: CORS misconfigurations that were once dismissed as low-severity nuisances are now chained directly to RCE in platforms where code execution is a first-class feature. Second, security tooling itself continues to surface as an attacker priority — Trend Micro Apex One follows a well-worn pattern of endpoint security products being leveraged to pivot laterally, because compromise of the management plane equals compromise of the entire agent fleet. Defenders should treat security-tool patching cadence with at least the same urgency as OS-level patches, and organizations adopting AI-builder platforms should audit CORS policies and cookie security attributes before any public or internal deployment.

---

## Blog Post Candidates

1. **"CORS Is Not a Low-Severity Issue Anymore: How CVE-2025-34291 Turns Langflow Into an RCE Gateway"** — Deep dive into how CORS + SameSite=None token cookies form an attack chain in AI-builder platforms; includes remediation checklist for similar architectures.
2. **"Attacking the Attacker's Tools: Why Endpoint Security Platforms Are Prime KEV Targets"** — Analysis of the recurring pattern of security product vulnerabilities (Apex One, SentinelOne, CrowdStrike) in the KEV catalog and what it means for enterprise patch prioritization.
3. **"AI Pipeline Security in 2026: KEV Entries You Can't Ignore"** — Broader look at how LLM/AI tooling (Langflow, Ollama, etc.) is accumulating CVEs and how organizations can build secure-by-default AI infrastructure.

---

## Newsletter Snippet

**This week CISA added two new entries to the Known Exploited Vulnerabilities catalog that demand immediate attention.** CVE-2025-34291 affects Langflow — the popular open-source AI application builder — where a CORS misconfiguration paired with an insecure SameSite=None cookie configuration allows any malicious website to silently steal authenticated session tokens and use them to execute arbitrary code on the server. With Langflow widely deployed in enterprise AI pipelines, this is an urgent patch: upgrade to v1.9.3 or later and audit your CORS policies across all AI tooling today.

**The second entry, CVE-2026-34926, targets Trend Micro Apex One on-premise deployments.** A directory traversal flaw lets a local attacker inject malicious code into the server's agent-deployment table, effectively weaponizing your endpoint security platform to push malware fleet-wide. While local access is required to trigger the vulnerability, it represents a critical lateral-movement escalator in any environment where an attacker has already gained a foothold — and given Apex One's role as a trusted distribution channel to every managed endpoint, the downstream blast radius is severe. Apply Trend Micro's patch (KA-0023430) immediately and verify agent integrity across your fleet.
