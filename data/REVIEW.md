# Daily KEV Review — 2026-10-24

**CVEs to review:** 1

---

## CVE-2026-110447: Collabora Collabora Online – Built-in CODE Server

**CVSS:** 9.2
**Description:** Collabora Collabora Online – Built-in CODE Server when used within the NextCloud platform contains an OS command injection vulnerability that allows for remote code execution when the CODE server isn't running.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-26
**CISA Notes:** https://help.nextcloud.com/t/to-collabora-built-in-user-update-asap/250516 ; https://github.com/CollaboraOnline/online/security/advisories/GHSA-g3vx-3m76-fghh ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-110447

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-110447)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-110447)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-110447)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-110447)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-110447)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-110447)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```