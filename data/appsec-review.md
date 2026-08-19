# AppSec Review — CISA KEV Batch

**Date:** 2026-08-19  
**Reviewer:** Robert Flores, CISSP  
**CVEs Reviewed:** 4  
**Source:** CISA Known Exploited Vulnerabilities Catalog (dateAdded: 2026-08-18)

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 4     | CVE-2026-33824, CVE-2026-59310, CVE-2026-55040, CVE-2026-65400 |
| High     | 0     | — |
| Medium   | 0     | — |
| Low      | 0     | — |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vuln Class |
|--------|--------|----------|------------|
| CVE-2026-33824 | Microsoft | Critical | Memory Corruption / Double Free → RCE |
| CVE-2026-59310 | Broadcom | Critical | Path Traversal → RCE |
| CVE-2026-55040 | Microsoft | Critical | Authentication Bypass |
| CVE-2026-65400 | Apple | Critical | Improper Authentication / Auth Bypass |

---

## CVE Details

**CVE-2026-33824 — Microsoft IKE Service Extensions (CVSS 9.8)**  
Double free vulnerability (CWE-415) in the Windows Internet Key Exchange service enables unauthenticated remote code execution. IKE is a network-facing service used in VPN and IPsec implementations, making this broadly exploitable against Windows endpoints and servers with IKE exposed. Patch immediately per BOD 26-04.

**CVE-2026-59310 — Broadcom VMware vCenter (CVSS 9.8)**  
Path traversal vulnerability (CWE-22) in vCenter Server allows any attacker with network access to vCenter to execute arbitrary code. vCenter is a hypervisor management plane and a crown-jewel target — compromise leads to full virtualization infrastructure takeover. Threat actors targeting VMware infrastructure should be expected to weaponize this rapidly.

**CVE-2026-55040 — Microsoft SharePoint (CVSS 9.1)**  
Weak authentication vulnerability (CWE-1390) allows unauthenticated attackers to bypass security features in SharePoint over the network. SharePoint is widely deployed across enterprise and government environments for document collaboration; auth bypass at this scope enables data exfiltration and lateral movement without valid credentials.

**CVE-2026-65400 — Apple macOS Screen Sharing (CVSS 9.8)**  
Improper authentication (CWE-287) in macOS allows a network-adjacent attacker to authenticate to Screen Sharing without valid credentials, gaining full remote desktop access. This is particularly dangerous in environments where macOS Screen Sharing is exposed on corporate networks or VPNs, as it grants interactive access with no credential requirement.

---

## Trend Analysis

This batch is dominated by authentication and access control failures across high-value enterprise infrastructure: Microsoft's IKE and SharePoint, Broadcom's vCenter, and Apple's macOS Screen Sharing. The pattern reflects a continued threat actor focus on authentication bypass and memory corruption primitives that enable unauthenticated remote code execution — the highest-impact attack class. Notably, all four CVEs are 2026-year identifiers added within days of discovery, suggesting CISA is tracking active in-the-wild exploitation faster than in prior years. The inclusion of VMware vCenter continues a multi-year trend of hypervisor management planes being actively targeted, likely driven by the high value of mass virtualization infrastructure takeover. Organizations should treat this batch as a unified campaign signal: attackers who compromise any one of these may use it as a pivot to reach the others.

---

## Blog Post Candidates

1. **"Why IKE Double-Free Vulnerabilities Are Uniquely Dangerous"** — Deep dive into CWE-415 in Windows IKE, how double-free primitives become RCE, and defender mitigations beyond just patching (network segmentation, VPN gateway hardening).

2. **"vCenter in the Crosshairs: Defending VMware Infrastructure Against CVE-2026-59310"** — Explores the blast radius of vCenter compromise, attacker playbooks post-exploitation, and architecture-level controls to limit impact even when patching is delayed.

3. **"Authentication Bypass at Scale: SharePoint and macOS Screen Sharing Weaknesses"** — Pairs CVE-2026-55040 and CVE-2026-65400 to discuss the systemic problem of auth bypass in enterprise software, detection strategies, and zero-trust controls that reduce reliance on authentication as a single control.

---

## Newsletter Snippet

This week's CISA KEV additions should trigger immediate patch prioritization across Windows, macOS, and VMware environments. Four critical vulnerabilities — all confirmed actively exploited — span Microsoft's IKE service (double-free RCE, CVSS 9.8), VMware vCenter (path traversal to RCE, CVSS 9.8), Microsoft SharePoint (auth bypass, CVSS 9.1), and Apple macOS Screen Sharing (improper auth, CVSS 9.8). Every one of these is unauthenticated and network-exploitable, meaning attackers need no foothold to begin exploitation. BOD 26-04 due dates are 2026-08-21 — three days from the date of this review.

If your team is triaging which to patch first, start with vCenter: hypervisor management plane compromise gives adversaries the keys to your entire virtualized infrastructure. SharePoint and IKE should follow immediately, particularly for internet-exposed deployments. The macOS Screen Sharing vulnerability is especially critical for organizations allowing remote work access via VPN — an attacker on the same network segment can gain full desktop control on any unpatched Mac. Verify exposure for each product and treat any delay in patching as accepted risk requiring compensating controls.
