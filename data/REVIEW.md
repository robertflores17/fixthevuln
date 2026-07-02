# Daily KEV Review — 2026-07-02

**CVEs to review:** 1

---

## CVE-2026-45659: Microsoft SharePoint Server

**CVSS:** 8.8
**Description:** Microsoft SharePoint Server contains a deserialization of untrusted data vulnerability which allows an authorized attacker to execute code over a network.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-04
**CISA Notes:** https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-45659 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-45659

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-45659)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-45659)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-45659)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-45659)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-45659)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-45659)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```