# Daily KEV Review — 2026-07-23

**CVEs to review:** 2

---

## CVE-2026-16232: Check Point SmartConsole

**CVSS:** 9.1
**Description:** Check Point SmartConsole contains an improper authentication vulnerability which could allow an unauthenticated remote attacker to obtain an application login token and use it to authenticate with full administrative privileges.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-25
**CISA Notes:** https://support.checkpoint.com/results/sk/sk185169/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-16232

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-16232)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-16232)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-16232)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-16232)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-16232)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-16232)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-50522: Microsoft SharePoint

**CVSS:** 9.8
**Description:** Microsoft SharePoint contains a deserialization of untrusted data vulnerability which could allow an unauthorized attacker to execute code over a network.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-25
**CISA Notes:** https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-50522 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-50522

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-50522)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-50522)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-50522)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-50522)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-50522)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-50522)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```