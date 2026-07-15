# AppSec Review — 2026-07-15

**Reviewer:** Robert Flores, CISSP  
**Pipeline Run:** 2026-07-15  
**CVEs Reviewed:** 4  
**Database Total After Publish:** 156 vulnerabilities  

---

## Severity Breakdown

| Priority | Count |
|----------|-------|
| Critical | 1 |
| High     | 3 |
| Medium   | 0 |
| Low      | 0 |
| **Total**| **4** |

---

## CVE Summary

| CVE ID | Vendor | Product | Priority | Vulnerability Class |
|--------|--------|---------|----------|---------------------|
| CVE-2026-56155 | Microsoft | Active Directory Federation Services | high | Privilege Escalation (Insufficient Access Control, CWE-1220) |
| CVE-2026-56164 | Microsoft | SharePoint Server | high | Auth Bypass / Missing Authentication (CWE-306) |
| CVE-2026-15409 | SonicWall | SMA1000 Appliances | critical | SSRF, Unauthenticated Remote (CWE-918) |
| CVE-2026-15410 | SonicWall | SMA1000 Appliances | high | Code Injection / OS Command Execution (CWE-94) |

---

## CVE Details

### CVE-2026-56155 — Microsoft Active Directory Federation Services (CVSS 7.8)
Insufficient access control (CWE-1220) allows a locally authenticated attacker to escalate privileges within AD FS. Because AD FS is a core identity brokering service, local privilege escalation here can translate to token manipulation and lateral movement across federated environments. 14-day remediation window per BOD 26-04.

### CVE-2026-56164 — Microsoft SharePoint Server (CVSS 5.3)
Missing authentication for a critical function (CWE-306) lets an unauthenticated remote attacker escalate privileges over the network. CISA assigned a 3-day remediation deadline — the shortest possible window under BOD 26-04 — indicating confirmed, urgent in-the-wild exploitation. SharePoint's enterprise ubiquity amplifies the blast radius considerably beyond what the CVSS score alone suggests.

### CVE-2026-15409 — SonicWall SMA1000 Appliances (CVSS 10.0)
Unauthenticated SSRF (CWE-918) on a remote access appliance earns a perfect 10.0 CVSS. An attacker can coerce the appliance into making arbitrary internal network requests, potentially pivoting to internal APIs, credential endpoints, or other services behind the perimeter. VPN/secure remote access appliances are prime initial access targets; this class of bug has repeatedly enabled nation-state intrusions. 3-day remediation window.

### CVE-2026-15410 — SonicWall SMA1000 Appliances (CVSS 7.2)
Code injection enabling OS command execution (CWE-94) on the same SMA1000 platform. Requires remote authentication as an administrator, but CVE-2026-15409 can facilitate credential theft, making these two a natural chain: unauthenticated SSRF to harvest creds → authenticated RCE for full appliance compromise. 3-day remediation window.

---

## Trend Analysis

This batch continues a pattern visible across recent CISA KEV additions: high-value enterprise perimeter infrastructure (identity providers, collaboration platforms, secure remote access appliances) is receiving the most urgent remediation timelines. Both SonicWall entries carry 3-day windows alongside Microsoft SharePoint, signaling that CISA's threat intelligence confirms active exploitation campaigns targeting these products simultaneously — consistent with threat actor interest in gaining network footholds via VPN appliances and then pivoting through identity infrastructure. The pairing of an unauthenticated SSRF (CVE-2026-15409, CVSS 10.0) with an authenticated RCE (CVE-2026-15410) on the same SonicWall product is particularly notable: chaining these two vulnerabilities requires no initial credentials and results in full appliance takeover, a pattern commonly exploited by ransomware affiliates and APT groups seeking persistent access to enterprise environments.

---

## Blog Post Candidates

1. **"SonicWall SMA1000 SSRF + RCE Chain: How Attackers Turn CVE-2026-15409 and CVE-2026-15410 into Full Appliance Takeover"** — A technical deep-dive on how SSRF can be leveraged to harvest credentials and chain into authenticated OS command execution, with detection and hunting guidance.

2. **"Why CVSS 5.3 Can Still Mean a 3-Day Patch Deadline: Unpacking CVE-2026-56164 (SharePoint Missing Auth)"** — Explores the gap between CVSS scoring and real-world exploit urgency, using this SharePoint auth bypass as a case study in why CISA's KEV context matters more than numeric scores.

3. **"Identity Infrastructure Under Fire: AD FS Privilege Escalation and What It Means for Federated Environments"** — Covers CVE-2026-56155 in the context of federated identity attack paths, including how local privesc in AD FS can cascade across trust relationships.

---

## Newsletter Snippet

**This week's CISA KEV additions put enterprise perimeter infrastructure squarely in the crosshairs.** Four new vulnerabilities were added on July 14, 2026, spanning Microsoft (Active Directory Federation Services and SharePoint) and SonicWall (SMA1000 remote access appliances). The standout entry is CVE-2026-15409 — a CVSS 10.0 unauthenticated SSRF on SonicWall SMA1000 — which pairs with a companion code injection bug (CVE-2026-15410) to create a no-credential-required path to full appliance takeover. Both SonicWall entries and Microsoft SharePoint carry emergency 3-day remediation deadlines, the most aggressive timeline CISA issues under BOD 26-04, confirming these are being actively exploited right now.

**What should you do this week?** If your organization runs SonicWall SMA1000 appliances, patch immediately — treat this as an incident response situation and verify no unauthorized access occurred before applying the fix. SharePoint Server administrators should do the same. For AD FS (CVE-2026-56155, 14-day window), prioritize patching any internet-exposed or externally-reachable AD FS infrastructure first and review federation trust configurations for anomalies. All four CVEs are confirmed in CISA's KEV catalog, meaning patch-or-mitigate is not optional for federal agencies and is strongly recommended for all organizations regardless of sector.
