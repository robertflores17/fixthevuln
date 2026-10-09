# Daily KEV Review — 2026-10-08

**CVEs to review:** 5

---

## CVE-2015-5477: ISC BIND

**CVSS:** 7.5
**Description:** ISC BIND contains a data processing errors vulnerability that could allow remote attackers to cause a denial of service via TKEY queries.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-11
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://web.archive.org/web/20150729014733/https://kb.isc.org/article/AA-01272 ; https://access.redhat.com/errata/RHSA-2015:1513.html; https://supportportal.juniper.net/s/article/2016-01-Security-Bulletin-Junos-Vulnerability-in-ISC-BIND-named-CVE-2015-5477 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2015-5477

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2015-5477)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2015-5477)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2015-5477)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2015-5477)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2015-5477)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2015-5477)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2016-3081: Apache Struts

**CVSS:** 8.1
**Description:** Apache Struts contains a command injection vulnerability that could allow remote attackers to execute arbitrary code via method:prefix when Dynamic Method Invocation is enabled.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-11
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://cwiki.apache.org/confluence/display/WW/S2-032 ; ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2016-3081

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2016-3081)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2016-3081)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2016-3081)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2016-3081)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2016-3081)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2016-3081)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2023-22894: Strapi Strapi

**CVSS:** 4.9
**Description:** Strapi contains a cleartext storage of sensitive information vulnerability that could allow attackers with access to the admin panel to discover sensitive user details via the query filter. The impacted product(s) could be end-of-life (EoL) and/or end-of-service (EoS). Users are advised to discontinue use and/or transition to a supported version. This vulnerability can be chained with CVE-2023-22621 to achieve remote code execution. 
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-11
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://strapi.io/blog/security-disclosure-of-vulnerabilities-cve ; https://github.com/strapi/strapi/releases ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2023-22894

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2023-22894)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2023-22894)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2023-22894)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2023-22894)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2023-22894)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2023-22894)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2021-3199: ONLYOFFICE Docs

**CVSS:** 9.8
**Description:** ONLYOFFICE Docs contains a path traversal vulnerability that can occur when JWT is used, via a /.. sequence in an image upload parameter and could allow for remote code execution.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-11
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: ; https://github.com/ONLYOFFICE/DocumentServer/blob/903fe5ab7a275bd69c3c3346af2d21cf87ebeabf/CHANGELOG.md#563 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2021-3199

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2021-3199)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2021-3199)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2021-3199)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2021-3199)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2021-3199)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2021-3199)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2015-3306: ProFTPD ProFTPD

**CVSS:** 10.0
**Description:** ProFTPD contains an improper access control vulnerability that could allow remote attackers to read and write to arbitrary files via the site cpfr and site cpto commands.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-11
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: http://www.proftpd.org/ ; https://lists.debian.org/debian-security-announce/2015/msg00154.html ; https://lists.opensuse.org/archives/list/updates@lists.opensuse.org/message/WE6YZRG5UVXMGQ7IVDRYBPIWV4M6UUGM/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2015-3306

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2015-3306)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2015-3306)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2015-3306)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2015-3306)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2015-3306)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2015-3306)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```