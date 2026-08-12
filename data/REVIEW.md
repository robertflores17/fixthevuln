# Daily KEV Review — 2026-08-12

**CVEs to review:** 3

---

## CVE-2026-20349: Cisco Secure Firewall Adaptive Security Appliance (ASA) and Secure Firewall Threat Defense (FTD)

**CVSS:** 8.6
**Description:** Cisco Secure Firewall Adaptive Security Appliance (ASA) and Secure Firewall Threat Defense (FTD) contain a heap inspection vulnerability that could allow an unauthenticated, remote attacker to cause the device to reload unexpectedly, resulting in a denial of service (DoS) condition.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-14
**CISA Notes:** https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-asaftd-vpn-dos-dzv4mQFF ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-20349

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-20349)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-20349)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-20349)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-20349)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-20349)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-20349)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-68820: Microsoft Windows Ancillary Function Driver for WinSock

**CVSS:** 7.0
**Description:** Microsoft Windows Ancillary Function Driver for WinSock contains a use-after-free vulnerability that allows an authorized attacker to elevate privileges locally.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-25
**CISA Notes:** https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2026-68820 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-68820

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-68820)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-68820)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-68820)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-68820)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-68820)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-68820)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-72898: Metabase Metabase

**CVSS:** 10.0
**Description:** Metabase contains a SQL Injection vulnerability that allows an unauthenticated remote attacker to inject arbitrary SQL into the Metabase application database, which can give them administrator access to the instance. From there, the attacker could change the application configuration, steal stored credentials for the connected databases, read any data accessible through those connections, and export data.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-14
**CISA Notes:** https://www.metabase.com/blog/security-update ; https://github.com/metabase/metabase/security/advisories/GHSA-vwf4-m7j8-wcjf ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-72898

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-72898)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-72898)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-72898)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-72898)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-72898)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-72898)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```