# AppSec Review — 2026-09-20

**Reviewer:** Robert Flores, CISSP  
**Review Date:** 2026-09-20  
**CVEs Reviewed:** 3  
**Source:** CISA Known Exploited Vulnerabilities (KEV) — added 2026-09-18

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 0     | —    |
| High     | 3     | CVE-2025-39964, CVE-2026-53266, CVE-2025-39682 |
| Medium   | 0     | —    |
| Low      | 0     | —    |

---

## CVE Summary

| CVE ID | Vendor | Product | Priority | Vuln Class |
|--------|--------|---------|----------|------------|
| CVE-2025-39964 | Linux | Kernel | high | Race Condition (CWE-362) |
| CVE-2026-53266 | Linux | Kernel | high | Out-of-Bounds Write (CWE-787) |
| CVE-2025-39682 | Linux | Kernel | high | Improper Exceptional Condition Check (CWE-754) |

---

## Trend Analysis

All three KEV additions this cycle target the Linux Kernel across distinct subsystems — the cryptographic socket layer (AF_ALG), the netfilter ebtables SNAT target, and the TLS receive path — reflecting a sustained pattern of kernel-level exploitation that bypasses userspace mitigations. Two of the three CVEs (CVE-2025-39964, CVE-2025-39682) were disclosed in 2025 but added to KEV only now, indicating CISA's growing enforcement posture under BOD 26-04, where delayed confirmation of active exploitation drives retroactive additions for components that are already EoL or near-EoL. The out-of-bounds write in ebtables (CVE-2026-53266, CVSS 8.8) carries the highest risk for organizations running Linux-based network appliances or bridging infrastructure, as exploitation can occur from the network layer without local access; defenders should prioritize kernel patching for internet-facing hosts and evaluate exposure of older kernel versions still running in containerized or virtualized environments.

---

## Blog Post Candidates

1. **"When the Kernel Is the Attack Surface: Analyzing CVE-2026-53266 and the ebtables OOB Write"** — Deep dive into how splice-imported page fragmentation in the SNAT target creates a write primitive, suitable for defenders and kernel developers.

2. **"BOD 26-04 in Practice: Why CISA Is Adding 2025 Kernel CVEs Now"** — Explainer on CISA's updated enforcement timeline and what retroactive KEV additions mean for patching windows in government and critical infrastructure.

3. **"TLS in the Kernel Is Still Hard: CVE-2025-39682 and the Zero-Length Record Edge Case"** — Technical analysis of how subtle state-machine flaws in kernel TLS can lead to memory safety violations, with mitigations for organizations relying on kTLS offload.

---

## Newsletter Snippet

**Patch Tuesday Isn't Enough: Three Linux Kernel Vulnerabilities Hit the CISA KEV**

CISA added three Linux Kernel vulnerabilities to its Known Exploited Vulnerabilities catalog this week, all confirmed actively exploited in the wild. The most severe — CVE-2026-53266 (CVSS 8.8) — is an out-of-bounds write in the ebtables SNAT target that allows an attacker to corrupt kernel memory through a crafted ARP hardware address rewrite in a bridged network environment, potentially leading to kernel-level code execution. Alongside it, CVE-2025-39964 (a race condition in the AF_ALG cryptographic socket) and CVE-2025-39682 (an exceptional-condition bypass in the kernel TLS receive path) round out a batch that highlights how attackers are increasingly targeting kernel subsystems as userspace hardening matures.

Organizations running Linux hosts — particularly those on older or EoL kernel versions — should treat these as urgent patches under BOD 26-04's risk-based prioritization framework. The three-day due date (2026-09-21) signals CISA's elevated urgency classification. If patching is not immediately possible, consider isolating affected hosts, restricting network bridging configurations, and auditing kTLS offload usage. All three CVEs have upstream kernel fixes available; consult your distribution's advisory for backported patch availability.
