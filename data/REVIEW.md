# Daily KEV Review — 2026-06-06

**CVEs to review:** 1

---

## CVE-2026-28318: SolarWinds Serv-U

**CVSS:** 7.5
**Description:** SolarWinds Serv-U contains an uncontrolled resource consumption vulnerability that allows specially crafted POST requests using the Content-Encoding: deflate header to crash the Serv-U service without authentication.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-19
**CISA Notes:** https://www.solarwinds.com/trust-center/security-advisories/cve-2026-28318 ; https://documentation.solarwinds.com/en/success_center/servu/content/release_notes/servu_15-5-4-hotfix-1_release_notes.htm#link7 ; https://nvd.nist.gov/vuln/detail/CVE-2026-28318

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-28318)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-28318)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-28318)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-28318)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-28318)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-28318)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```