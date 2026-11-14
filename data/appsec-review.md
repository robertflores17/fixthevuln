# AppSec Review — 2026-11-14

**Reviewer:** Robert Flores, CISSP  
**Review Date:** 2026-11-14  
**CVEs Reviewed:** 2  
**CVEs Approved:** 2  

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 0     | —    |
| High     | 2     | CVE-2026-114713, CVE-2026-123039 |
| Medium   | 0     | —    |
| Low      | 0     | —    |

---

## CVE Summary

| CVE ID | Vendor | Priority | Vulnerability Class |
|--------|--------|----------|---------------------|
| CVE-2026-114713 | UnrealIRCd | High | Command Injection / Delimiter Injection (CWE-140) |
| CVE-2026-123039 | Check Point | High | Incorrect Permission Assignment / Local Privilege Escalation (CWE-732, CWE-862) |

---

## Individual Assessments

**CVE-2026-114713 — UnrealIRCd Delimiter Injection (CVSS 8.6)**  
Any authenticated user on a network with two or more linked UnrealIRCd servers can inject server-to-server commands executed with server authority via improper neutralization of delimiters (CWE-140). This is remotely exploitable by any IRC user and effectively allows unauthorized privilege escalation to server-level command execution.

**CVE-2026-123039 — Check Point Local Privilege Escalation (CVSS 7.8)**  
Check Point's DynamicCLI daemon runs as root and listens on a world-writable local socket without authenticating connecting processes (CWE-732, CWE-862). Any authenticated local user can send commands to the socket and execute them as root, impacting Firewall, Multi-Domain Security Management Server, Scalable Platforms, Security Gateway, and Security Management Server.

---

## Trend Analysis

This batch continues a pattern of privilege escalation vulnerabilities in security-adjacent infrastructure. Both CVEs affect components that are trusted deeply within their respective environments — an IRC server's inter-server trust model and a firewall management daemon running as root — making exploitation especially impactful when it occurs. The UnrealIRCd finding is consistent with ongoing CISA interest in network protocol injection flaws, while the Check Point LPE reflects a persistent class of UNIX daemon hardening failures (unauthenticated local sockets owned by root) that remain common in mature commercial security products. Organizations running either product should treat the November 16 due date as firm given CISA BOD 26-04 requirements.

---

## Blog Post Candidates

1. **"Server-to-Server Trust Abuse: How IRC Delimiter Injection Grants Root Authority"** — Deep dive on the UnrealIRCd multi-server injection path, explaining how delimiter mishandling in legacy protocol parsers creates escalation opportunities even without RCE.

2. **"The Root Socket Problem: Why Unix Daemons Running as Root Are a Persistent LPE Vector"** — Using CVE-2026-123039 as a case study on CWE-732/CWE-862, covering world-writable sockets, missing process authentication, and how to audit for similar patterns in enterprise security tooling.

3. **"CISA BOD 26-04: What 3-Day Patch Deadlines Mean for Security Operations Teams"** — Both CVEs carry a November 16 due date, making this a good hook to explain the accelerated patching cadence now required under BOD 26-04 and what orgs should have in place to meet it.

---

## Newsletter Snippet

CISA added two vulnerabilities to the Known Exploited Vulnerabilities catalog this week, both carrying a 3-day remediation deadline under BOD 26-04. The first, CVE-2026-114713, affects UnrealIRCd and allows any user on a multi-server IRC network to inject server-to-server commands with full server authority — a command injection flaw (CVSS 8.6) that is remotely exploitable by any authenticated IRC user. The second, CVE-2026-123039, is a local privilege escalation in several Check Point products (Firewall, Security Gateway, Security Management Server, and others), where the DynamicCLI daemon runs as root with an unauthenticated world-writable socket, letting any local user gain root-level code execution (CVSS 7.8).

Both vulnerabilities are classified **High** severity and reflect two persistent problem classes — protocol injection in legacy network daemons and insecure UNIX socket permissions in security tooling. If your environment includes UnrealIRCd or any Check Point security product, the patch deadline is **November 16, 2026**. Refer to the UnrealIRCd forums advisory and Check Point sk1000362 for vendor-specific remediation guidance.
