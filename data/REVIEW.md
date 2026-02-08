# KEV Review - Week of 2026-02-08

**CVEs to review:** 2

---

## [RANSOMWARE] CVE-2026-24423: SmarterTools SmarterMail

**CVSS:** 9.8
**Description:** SmarterTools SmarterMail contains a missing authentication for critical function vulnerability in the ConnectToHub API method. This could allow the attacker to point the SmarterMail instance to a malicious HTTP server which serves the malicious OS command and could lead to command execution. 
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-02-26
**CISA Notes:** https://www.smartertools.com/smartermail/release-notes/current ; https://www.cve.org/CVERecord?id=CVE-2026-24423 ; https://nvd.nist.gov/vuln/detail/CVE-2026-24423

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-24423)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-24423)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-24423)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-24423)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-24423)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-24423)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2025-11953: React Native Community CLI

**CVSS:** 9.8
**Description:** React Native Community CLI contains an OS command injection vulnerability which could allow unauthenticated network attackers to send POST requests to the Metro Development Server and run arbitrary executables via a vulnerable endpoint exposed by the server. On Windows, attackers can also execute arbitrary shell commands with fully controlled arguments.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-02-26
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://github.com/react-native-community/cli/commit/15089907d1f1301b22c72d7f68846a2ef20df547 ; https://github.com/react-native-community/cli/pull/2735 ; https://nvd.nist.gov/vuln/detail/CVE-2025-11953

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-11953)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-11953)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-11953)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-11953)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-11953)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-11953)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```