# Daily KEV Review — 2026-05-01

**CVEs to review:** 1

---

## CVE-2026-41940: WebPros cPanel & WHM and WP2 (WordPress Squared)

**CVSS:** 9.8
**Description:** WebPros cPanel & WHM (WebHost Manager) and WP2 (WordPress Squared) contain an authentication bypass vulnerability in the login flow that allows unauthenticated remote attackers to gain unauthorized access to the control panel.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-03
**CISA Notes:** https://support.cpanel.net/hc/en-us/articles/40073787579671-cPanel-WHM-Security-Update-04-28-2026 ; https://docs.cpanel.net/release-notes/release-notes/ ; https://docs.wpsquared.com/changelogs/versions/changelog/#13617 ; https://nvd.nist.gov/vuln/detail/CVE-2026-41940"

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-41940)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-41940)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-41940)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-41940)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-41940)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-41940)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```