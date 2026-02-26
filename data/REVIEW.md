# Daily KEV Review — 2026-02-26

**CVEs to review:** 3

---

## CVE-2022-20775: Cisco SD-WAN

**CVSS:** 7.8
**Description:** Cisco SD-WAN CLI contains a path traversal vulnerability that could allow an authenticated local attacker to gain elevated privileges via improper access controls on commands within the application CLI. A successful exploit could allow the attacker to execute arbitrary commands as the root user.
**Fix:** Please adhere to CISA’s guidelines to assess exposure and mitigate risks associated with Cisco SD-WAN devices as outlines in CISA’s Emergency Directive 26-03 (URL listed below in Notes) and CISA’s “Hunt & Hardening Guidance for Cisco SD-WAN Devices (URL listed below in Notes). Adhere to the applicable BOD 22-01 guidance for cloud services or discontinue use of the product if mitigations are not available.
**Due Date:** 2026-02-27
**CISA Notes:** CISA Mitigation Instructions: https://www.cisa.gov/news-events/directives/ed-26-03-mitigate-vulnerabilities-cisco-sd-wan-systems ; https://www.cisa.gov/news-events/directives/supplemental-direction-ed-26-03-hunt-and-hardening-guidance-cisco-sd-wan-systems ; https://www.cisco.com/c/en/us/support/docs/csa/cisco-sa-sd-wan-priv-E6e8tEdF.html ; https://nvd.nist.gov/vuln/detail/CVE-2022-20775

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2022-20775)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2022-20775)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2022-20775)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2022-20775)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2022-20775)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2022-20775)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-20127: Cisco Catalyst SD-WAN Controller and Manager

**CVSS:** 10.0
**Description:** Cisco Catalyst SD-WAN Controller, formerly SD-WAN vSmart, and Cisco Catalyst SD-WAN Manager, formerly SD-WAN vManage, contain an authentication bypass vulnerability could allow an unauthenticated, remote attacker to bypass authentication and obtain administrative privileges on an affected system. This vulnerability exists because the peering authentication mechanism in an affected system is not working properly. An attacker could exploit this vulnerability by sending crafted requests to an affected system. A successful exploit could allow the attacker to log in to an affected Cisco Catalyst SD-WAN Controller as an internal, high-privileged, non-root user account. Using this account, the attacker could access NETCONF, which would then allow the attacker to manipulate network configuration for the SD-WAN fabric.
**Fix:** Please adhere to CISA’s guidelines to assess exposure and mitigate risks associated with Cisco SD-WAN devices as outlines in CISA’s Emergency Directive 26-03 (URL listed below in Notes) and CISA’s “Hunt & Hardening Guidance for Cisco SD-WAN Devices (URL listed below in Notes). Adhere to the applicable BOD 22-01 guidance for cloud services or discontinue use of the product if mitigations are not available.
**Due Date:** 2026-02-27
**CISA Notes:** CISA Mitigation Instructions: https://www.cisa.gov/news-events/directives/ed-26-03-mitigate-vulnerabilities-cisco-sd-wan-systems ; https://www.cisa.gov/news-events/directives/supplemental-direction-ed-26-03-hunt-and-hardening-guidance-cisco-sd-wan-systems ; https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-rpa-EHchtZk ; https://nvd.nist.gov/vuln/detail/CVE-2026-20127

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-20127)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-20127)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-20127)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-20127)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-20127)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-20127)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-25108: Soliton Systems K.K FileZen

**CVSS:** 8.8
**Description:** Soliton Systems K.K FileZen contains an OS command injection vulnerability when an user logs-in to the affected product and sends a specially crafted HTTP request.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-17
**CISA Notes:** https://jvn.jp/en/jp/JVN84622767/ ; https://nvd.nist.gov/vuln/detail/CVE-2026-25108

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-25108)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-25108)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-25108)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-25108)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-25108)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-25108)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```