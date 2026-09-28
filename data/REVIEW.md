# Daily KEV Review — 2026-09-28

**CVEs to review:** 2

---

## CVE-2026-88772: Citrix NetScaler

**CVSS:** 8.1
**Description:** Citrix NetScaler ADC and NetScaler Gateway contain an improper restriction of operations within the bounds of a memory buffer vulnerability that could allow for remote code execution or denial of service
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-30
**CISA Notes:** Running the provided IOCs in the NetScaler console may help identify indicators of exploitation. Customers must conduct forensic triage as directed by BOD 26‑04 and follow Citrix’s published guidance for mitigations. For more information, please see: https://community.citrix.com/techzone-blogs/110_security-updates/netscaler-adc-and-netscaler-gateway-security-bulletin-for-cve-2026-88771-through-cve-2026-88778 ; https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096 ; https://support.citrix.com/external/article/CTX694799/steps-to-take-if-netscaler-adc-is-suspec.html ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-88772

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-88772)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-88772)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-88772)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-88772)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-88772)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-88772)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-88771: Citrix NetScaler

**CVSS:** 9.8
**Description:** Citrix NetScaler ADC and NetScaler Gateway contain an improper input validation vulnerability that could allow an unauthenticated attacker to execute arbitrary commands.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-30
**CISA Notes:** Running the provided IOCs in the NetScaler console may help identify indicators of exploitation. Customers must conduct forensic triage as directed by BOD 26‑04 and follow Citrix’s published guidance for mitigations. For more information, please see: https://community.citrix.com/techzone-blogs/110_security-updates/netscaler-adc-and-netscaler-gateway-security-bulletin-for-cve-2026-88771-through-cve-2026-88778 ; https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096 ; https://support.citrix.com/external/article/CTX694799/steps-to-take-if-netscaler-adc-is-suspec.html ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-88772

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-88771)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-88771)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-88771)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-88771)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-88771)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-88771)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```