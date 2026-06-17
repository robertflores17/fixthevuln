# Daily KEV Review — 2026-06-17

**CVEs to review:** 1

---

## CVE-2026-48907: Widget Factory Joomla Content Editor

**CVSS:** 
**Description:** Widget Factory Joomla Content Editor contains an improper access control vulnerability which could allow for upload and execution of PHP code via the creation of new editor profiles for unauthenticated users. 
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-06-19
**CISA Notes:** https://www.joomlacontenteditor.net/news/jce-security-update-and-a-free-patch-for-older-sites ; https://www.joomlacontenteditor.net/support/changelog/editor ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-48907

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-48907)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-48907)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-48907)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-48907)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-48907)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-48907)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```