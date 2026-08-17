# AppSec Review — 2026-08-17

**Reviewer:** Robert Flores, CISSP  
**Pipeline run:** 2026-08-17  
**CVEs reviewed:** 1  
**Source:** CISA Known Exploited Vulnerabilities (KEV) Catalog

---

## Severity Breakdown

| Priority  | Count |
|-----------|-------|
| Critical  | 1     |
| High      | 0     |
| Medium    | 0     |
| Low       | 0     |
| **Total** | **1** |

---

## CVE Summary

| CVE ID          | Vendor      | Product | Priority | Vuln Class                         |
|-----------------|-------------|---------|----------|------------------------------------|
| CVE-2025-62593  | Ray-Project | Ray     | critical | Code Injection / CSRF → RCE        |

---

## Trend Analysis

This batch centers on the growing attack surface created by the rapid adoption of ML/AI infrastructure tooling. Ray is a widely-deployed distributed computing framework heavily used in ML training and inference pipelines, making CVE-2025-62593 a high-value target: a browser-triggered CSRF (CWE-352) combined with a server-side code injection (CWE-94) allows an unauthenticated attacker to achieve remote code execution simply by tricking a developer with an open Ray dashboard into visiting a malicious page. CISA's decision to add this 2025 CVE to KEV in August 2026 reflects confirmed in-the-wild exploitation, consistent with the pattern of attackers targeting ML infrastructure once broader organizational adoption creates a large enough attack surface. Organizations running Ray clusters — particularly those exposed beyond localhost or with weak network segmentation — should treat this as an emergency patch or compensating control item, especially as BOD 26-04 mandates remediation within three days of KEV listing.

---

## Blog Post Candidates

1. **"Ray of Danger: Why ML Infrastructure Is the New Perimeter"** — Explores how AI/ML tooling (Ray, Jupyter, MLflow) is becoming a primary attack vector as organizations scale model training, with CVE-2025-62593 as the centerpiece case study.

2. **"Browser-Based RCE: How CSRF Supercharges Code Injection"** — Deep-dive on CWE-94 + CWE-352 chaining, using this Ray vulnerability to illustrate how an innocuous-looking cross-site request can escalate to full server-side code execution.

3. **"BOD 26-04 in Practice: Three-Day Patching for High-Risk KEV Entries"** — A practitioner's guide to operationalizing the new CISA binding operational directive, using this week's Ray KEV addition as a real-world drill scenario.

---

## Newsletter Snippet

**This week on CISA KEV:** One new vulnerability was added to the Known Exploited Vulnerabilities catalog this cycle — and it's one ML/AI teams need to take seriously. CVE-2025-62593 affects Ray-Project Ray, the popular distributed computing framework backing many ML training and inference workloads. Rated CVSS 9.4 (Critical), the flaw chains a cross-site request forgery with a server-side code injection, giving attackers a browser-based path to unauthenticated remote code execution on any Ray cluster reachable by a developer's browser session. CISA's confirmation of active exploitation means this is no longer theoretical.

Under BOD 26-04, federal agencies and covered entities have until 2026-08-21 to apply vendor mitigations or discontinue use. For everyone else, the practical advice is the same: patch immediately, review Ray dashboard exposure (default port 8265), and ensure Ray clusters are not accessible from the public internet or untrusted network segments. This class of attack — browser-delivered RCE against developer tooling — is increasingly common as AI infrastructure matures, and it won't be the last ML framework on the KEV list.
