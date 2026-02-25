# Daily KEV Review — 2026-02-25

**CVEs to review:** 1

---

## CVE-2026-25108: Soliton Systems K.K FileZen

**CVSS:** 8.8
**Description:** Soliton Systems K.K FileZen contains an OS command injection vulnerability when an user logs-in to the affected product and sends a specially crafted HTTP request.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-17
**CISA Notes:** https://jvn.jp/en/jp/JVN84622767/ ; https://nvd.nist.gov/vuln/detail/CVE-2026-25108

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-25108)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-25108)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-25108)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-25108)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-25108)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-25108)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```