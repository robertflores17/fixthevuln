# Daily KEV Review — 2026-04-25

**CVEs to review:** 4

---

## CVE-2025-29635: D-Link DIR-823X

**CVSS:** 7.2
**Description:** D-Link DIR-823X contains a command injection vulnerability that allows an authorized attacker to execute arbitrary commands on remote devices by sending a POST request to /goform/set_prohibiting via the corresponding function. The impacted product could be end-of-life (EoL) and/or end-of-service (EoS). Users should discontinue product utilization.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-08
**CISA Notes:** https://supportannouncement.us.dlink.com/security/publication.aspx?name=SAP10469 ; https://nvd.nist.gov/vuln/detail/CVE-2025-29635

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-29635)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-29635)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-29635)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-29635)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-29635)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-29635)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2024-7399: Samsung MagicINFO 9 Server

**CVSS:** 8.8
**Description:** Samsung MagicINFO 9 Server contains a path traversal vulnerability that could allow an attacker to write arbitrary files as system authority.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-08
**CISA Notes:** https://security.samsungtv.com/securityUpdates ; https://nvd.nist.gov/vuln/detail/CVE-2024-7399

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2024-7399)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2024-7399)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2024-7399)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2024-7399)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2024-7399)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2024-7399)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2024-57728: SimpleHelp  SimpleHelp

**CVSS:** 7.2
**Description:** SimpleHelp contains a path traversal vulnerability that allows admin users to upload arbitrary files anywhere on the file system by uploading a crafted zip file (i.e. zip slip). This can be exploited to execute arbitrary code on the host in the context of the SimpleHelp server user.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-08
**CISA Notes:** https://simple-help.com/kb---security-vulnerabilities-01-2025#security-vulnerabilities-in-simplehelp-5-5-7-and-earlier ; https://nvd.nist.gov/vuln/detail/CVE-2024-57728

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2024-57728)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2024-57728)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2024-57728)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2024-57728)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2024-57728)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2024-57728)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2024-57726: SimpleHelp  SimpleHelp

**CVSS:** 9.9
**Description:** SimpleHelp contains a missing authorization vulnerability that could allow low-privileged technicians to create API keys with excessive permissions. These API keys can be used to escalate privileges to the server admin role.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-08
**CISA Notes:** https://simple-help.com/kb---security-vulnerabilities-01-2025#security-vulnerabilities-in-simplehelp-5-5-7-and-earlier ; https://nvd.nist.gov/vuln/detail/CVE-2024-57726

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2024-57726)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2024-57726)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2024-57726)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2024-57726)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2024-57726)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2024-57726)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```