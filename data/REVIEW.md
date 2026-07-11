# Daily KEV Review — 2026-07-11

**CVEs to review:** 2

---

## CVE-2026-56291: Balbooa Forms

**CVSS:** 9.8
**Description:** Balbooa Forms contains an unrestricted upload of file with dangerous type vulnerability that allows an unauthenticated arbitrary file upload which could allow uploading of executable files leading to full RCE.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-13
**CISA Notes:** https://www.balbooa.com/joomla-forms ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-56291

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-56291)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-56291)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-56291)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-56291)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-56291)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-56291)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-48939: iCagenda iCagenda

**CVSS:** 9.8
**Description:** iCagenda contains an unrestricted upload of file with dangerous type vulnerability that allows the upload of arbitrary files in the file attachment feature, ultimately resulting in PHP code upload and execution.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-13
**CISA Notes:** https://www.icagenda.com/#download ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-48939

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-48939)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-48939)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-48939)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-48939)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-48939)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-48939)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```