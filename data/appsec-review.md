# AppSec Review

**Date:** 2026-06-13
**Reviewer:** Robert Flores, CISSP (FixTheVuln AppSec Reviewer)
**CVE Count:** 2

## Severity Breakdown

| Priority | Count |
|----------|-------|
| Critical | 2 |
| High     | 0 |
| Medium   | 0 |
| Low      | 0 |

## CVEs

- **CVE-2026-35273** — Oracle (PeopleSoft Enterprise PeopleTools) — Critical — Missing Authentication for Critical Function / Unauthenticated Takeover
- **CVE-2026-10520** — Ivanti (Sentry) — Critical — OS Command Injection / Unauthenticated Root RCE

## Trend Analysis

Both additions to today's KEV catalog represent unauthenticated, network-exploitable vulnerabilities in widely-deployed enterprise edge and ERP infrastructure — continuing a sustained pattern of attackers targeting internet-facing management and gateway appliances (Ivanti) and back-office business systems (Oracle PeopleSoft) for initial access and ransomware staging. The Oracle PeopleSoft flaw is explicitly tied to known ransomware activity, while the Ivanti Sentry command injection follows the well-established trajectory of prior MobileIron/Sentry RCE chains, reinforcing that unmanaged or externally-reachable mobile device management infrastructure remains a high-value target. Organizations running either product should treat these as emergency patch/mitigate actions given the 2-3 day CISA remediation deadlines (BOD 26-04).

## Blog Post Candidates

1. "Why Unauthenticated ERP Takeovers Matter: Lessons from CVE-2026-35273 (Oracle PeopleSoft)"
2. "Ivanti Sentry's Recurring RCE Problem: A History of OS Command Injection in MDM Gateways"
3. "BOD 26-04 in Practice: Triaging Critical CISA KEV Deadlines Under 72 Hours"

## Newsletter Snippet

This week CISA added two critical, actively-exploited vulnerabilities to the KEV catalog — both carrying tight 2-3 day remediation deadlines under BOD 26-04. CVE-2026-35273 is a missing-authentication flaw in Oracle PeopleSoft Enterprise PeopleTools that allows an unauthenticated attacker to fully take over the application, and CISA notes it has already been linked to ransomware operations. CVE-2026-10520 affects Ivanti Sentry (formerly MobileIron Sentry), where an OS command injection bug enables unauthenticated, root-level remote code execution on appliances left externally reachable in an unmanaged state.

If your organization runs either product, prioritize patching or applying vendor mitigations immediately — internet-exposed PeopleSoft and Sentry instances should be considered under active attack. For Sentry specifically, restricting external reachability via mTLS with EPMM or Neurons for MDM significantly reduces exposure if patching can't happen instantly. Full details and remediation guidance for both CVEs are now live on FixTheVuln.
