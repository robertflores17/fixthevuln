# AppSec Review — CISA KEV Batch

**Date:** 2026-09-03  
**Reviewer:** Robert Flores, CISSP  
**CVEs Reviewed:** 7  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog — dateAdded 2026-09-02

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 4 | CVE-2026-49869, CVE-2026-82329, CVE-2026-9586, CVE-2026-83548 |
| High | 2 | CVE-2026-59822, CVE-2026-83549 |
| Medium | 1 | CVE-2026-48710 |
| Low | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-59822 | BerriAI (LiteLLM) | high | Auth bypass (improper authentication) |
| CVE-2026-48710 | Kludex (Starlette) | medium | HTTP request/response smuggling |
| CVE-2026-49869 | Kestra (Kestra OSS) | critical | OS command injection / unauthenticated RCE |
| CVE-2026-82329 | JFrog (Artifactory) | critical | Auth bypass / unauth privilege escalation |
| CVE-2026-9586 | Sangoma (Switchvox) | critical | SQL injection / RCE |
| CVE-2026-83548 | SonicWall (SMA1000) | critical | SSRF (unauthenticated) |
| CVE-2026-83549 | SonicWall (SMA1000) | high | OS command injection (auth required) |

---

## Trend Analysis

This batch reflects a continuing trend of critical authentication failures and command injection vulnerabilities across both enterprise infrastructure and developer tooling. Four of the seven CVEs require zero authentication to exploit — including two CVSS 10.0 vulnerabilities — signaling that attackers are increasingly targeting default configurations and trust boundaries in DevOps and network edge products. The simultaneous addition of two SonicWall SMA1000 CVEs (SSRF + OS command injection) is notable: the SSRF likely serves as a stepping stone to internal network access, while the authenticated command injection closes the loop for post-compromise lateral movement. The inclusion of Kestra OSS and LiteLLM reflects a broader CISA focus on AI/ML and workflow orchestration platforms, which are increasingly deployed in sensitive pipeline positions but often lack mature security hardening.

---

## Blog Post Candidates

1. **"Zero Auth to Root: How Default Configurations Are Killing Enterprise Security"** — Use CVE-2026-82329 (JFrog Artifactory) and CVE-2026-83548 (SonicWall) as anchors for a practitioner guide on hardening default installs and segmenting admin interfaces.

2. **"AI Tools Are the New Attack Surface: LiteLLM and Kestra OSS Hit the CISA KEV"** — Explore the security implications of rapidly adopted AI/ML tooling (LiteLLM, Kestra) entering production pipelines without enterprise-grade authentication hardening.

3. **"Request Smuggling in 2026: Why HTTP Path Injection Still Works"** — Deep dive on CVE-2026-48710 (Starlette) and its chain with CVE-2026-42271, explaining how smuggling attacks defeat perimeter authentication.

---

## Newsletter Snippet

**CISA adds 7 new KEVs — 4 critical, including two CVSS 10.0 vulnerabilities.** This week's KEV additions hit hard across enterprise DevOps and network infrastructure. JFrog Artifactory (CVE-2026-82329, CVSS 9.8) and SonicWall SMA1000 (CVE-2026-83548, CVSS 10.0) both allow unauthenticated attackers to gain administrative or privileged access under default configurations — patch immediately if you're running either in an internet-accessible posture. Kestra OSS (CVE-2026-49869, CVSS 10.0) is a perfect 10: unauthenticated remote code execution via OS command injection with no prerequisites.

Two CVEs affecting developer and AI tooling — BerriAI LiteLLM and Kludex Starlette — underscore that supply chain and framework-layer vulnerabilities are now firmly in scope for CISA KEV. If your organization uses these libraries in any service-facing capacity, verify patched versions are deployed. All 7 CVEs carry BOD 26-04 compliance obligations for federal agencies, with three at the tightest remediation window (due 2026-09-05). Security teams should prioritize SonicWall SMA1000 and JFrog Artifactory patches this sprint.
