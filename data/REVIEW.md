# Daily KEV Review — 2026-10-02

**CVEs to review:** 2

---

## CVE-2026-102490: Zammad GmbH Zammad

**CVSS:** 9.8
**Description:** Zammad GmbH Zammad contains an improper privilege management vulnerability that can allow the local zammad user to escalate privileges to root. This vulnerability can be chained with CVE-2026-102489.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-05
**CISA Notes:** https://zammad.com/en/product/releases/ ; https://community.zammad.org/t/take-care-local-privilege-escalation-cve-2026-102490-is-reported-as-being-actively-exploited/21297/2 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-102490

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-102490)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-102490)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-102490)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-102490)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-102490)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-102490)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-102489: Zammad GmbH Zammad

**CVSS:** 9.8
**Description:** Zammad GmbH Zammad contains a session fixation vulnerability that can lead to remote code execution as the zammad user. This vulnerability can be chained with CVE-2026-102490.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-05
**CISA Notes:** https://zammad.com/en/product/releases/ ; https://community.zammad.org/t/take-care-local-privilege-escalation-cve-2026-102490-is-reported-as-being-actively-exploited/21297/2 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-102489

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-102489)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-102489)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-102489)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-102489)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-102489)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-102489)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```