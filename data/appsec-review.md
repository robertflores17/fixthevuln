# AppSec Review

**Date:** 2026-06-11
**Reviewer:** Robert Flores, CISSP (FixTheVuln AppSec Reviewer)
**CVE Count:** 3

## Severity Breakdown

| Priority | Count |
|----------|-------|
| Critical | 0 |
| High     | 2 |
| Medium   | 1 |
| Low      | 0 |

## CVEs

- **CVE-2026-11645** — Google (Chromium V8) — High — Memory Corruption / OOB Read-Write (CWE-125/787)
- **CVE-2026-7473** — Arista (EOS) — Medium — Improper Comparison / Logic Flaw in Packet Decapsulation (CWE-1023)
- **CVE-2026-20245** — Cisco (Catalyst SD-WAN Manager) — High — Improper Output Encoding leading to Local Privilege Escalation (CWE-116)

## Trend Analysis

This batch spans the full stack — browser engine, network OS, and SD-WAN management plane — but shares a common thread: attackers chaining lower-severity primitives into full compromise. The Chromium V8 OOB read/write (CVE-2026-11645) is a classic sandbox-escape building block; on its own it grants sandboxed code execution via a malicious page, but combined with a sandbox-escape bug it becomes full host compromise, and its CVSS 8.8 reflects the broad reach across Chrome, Edge, and Opera. The Arista EOS issue (CVE-2026-7473) is a quieter but structurally interesting flaw — an incomplete comparison in tunnel decapsulation logic that lets unexpected tunneled traffic slip past intended IP-matching boundaries, a reminder that network OS packet-handling edge cases remain an underappreciated attack surface for traffic injection or filter bypass. The Cisco SD-WAN Manager bug (CVE-2026-20245) follows a now-familiar Cisco pattern: an authenticated, low-privilege foothold escalating to root via a crafted file due to improper output encoding, which is especially dangerous on SD-WAN management infrastructure that controls routing across an entire enterprise WAN. Together, these reinforce that defense-in-depth — patching browsers promptly, auditing tunnel/overlay configurations, and tightly restricting access to network management consoles — remains essential even when individual bugs look "only" exploitable with prerequisites.

## Blog Post Candidates

1. "Inside a Chromium Sandbox Escape Chain: What CVE-2026-11645 Teaches About Browser Memory Safety"
2. "When Tunnels Lie: How an Incomplete Comparison in Arista EOS Lets Unexpected Packets Through"
3. "Authenticated Doesn't Mean Safe: Cisco SD-WAN Manager's Path from Local User to Root"

## Newsletter Snippet

CISA added three new vulnerabilities to its Known Exploited Vulnerabilities catalog this week, spanning browsers, network operating systems, and SD-WAN management platforms. The most far-reaching is CVE-2026-11645 (CVSS 8.8), an out-of-bounds read/write in Google Chromium's V8 JavaScript engine that lets attackers execute code inside the browser sandbox via a crafted webpage — affecting Chrome, Edge, Opera, and any other Chromium-based browser. Update your browsers immediately, as this is a prime ingredient in drive-by exploit chains.

On the network infrastructure side, Cisco disclosed CVE-2026-20245 (CVSS 7.8) in Catalyst SD-WAN Manager, where an authenticated local attacker can supply a crafted file to escalate to root — a serious risk for any organization where SD-WAN console access isn't tightly restricted. Arista also patched CVE-2026-7473 (CVSS 5.8), a logic flaw in EOS where switches can incorrectly decapsulate and forward unexpected tunneled traffic. All three carry a June 23, 2026 remediation deadline — prioritize the Chromium and Cisco fixes given their higher exploitability.
