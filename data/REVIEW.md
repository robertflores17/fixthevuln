# Daily KEV Review — 2026-05-15

**CVEs to review:** 1

---

## CVE-2026-20182: Cisco Catalyst SD-WAN

**CVSS:** 10.0
**Description:** Cisco Catalyst SD-WAN Controller & Manager contain an authentication bypass vulnerability that allows an unauthenticated, remote attacker to bypass authentication and obtain administrative privileges on an affected system.
**Fix:** Please adhere to CISA’s guidelines to assess exposure and mitigate risks associated with Cisco SD-WAN devices as outlined in CISA’s Emergency Directive 26-03 (URL listed below in Notes) and CISA’s Hunt & Hardening Guidance for Cisco SD-WAN Devices (URL listed below in Notes). Adhere to the applicable BOD 22-01 guidance for cloud services or discontinue use of the product if mitigations are not available.
**Due Date:** 2026-05-17
**CISA Notes:** CISA Mitigation Instructions: https://www.cisa.gov/news-events/directives/ed-26-03-mitigate-vulnerabilities-cisco-sd-wan-systems ; https://www.cisa.gov/news-events/directives/supplemental-direction-ed-26-03-hunt-and-hardening-guidance-cisco-sd-wan-systems ; https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-rpa2-v69WY2SW ; https://nvd.nist.gov/vuln/detail/CVE-2026-20182

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-20182)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-20182)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-20182)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-20182)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-20182)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-20182)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```