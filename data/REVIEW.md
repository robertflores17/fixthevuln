# Daily KEV Review — 2026-07-14

**CVEs to review:** 1

---

## CVE-2008-4128: Cisco IOS

**CVSS:** 4.3
**Description:** Cisco IOS 12.4 contains multiple cross-site forgery vulnerabilities that allows remote attackers to execute arbitrary commands via (1) a certain "show privilege" command to the /level/15/exec/- URI, and (2) a certain "alias exec" command to the /level/15/exec/-/configure/http URI.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-16
**CISA Notes:** https://www.cisco.com/c/en/us/obsolete/ios-nx-os-software/cisco-ios-software-releases-12-4-mainline.html ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2008-4128

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2008-4128)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2008-4128)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2008-4128)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2008-4128)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2008-4128)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2008-4128)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```