# Daily KEV Review — 2026-04-17

**CVEs to review:** 1

---

## CVE-2026-34197: Apache ActiveMQ

**CVSS:** 8.8
**Description:** Apache ActiveMQ contains an improper input validation vulnerability that allows for code injection.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-04-30
**CISA Notes:** https://activemq.apache.org/security-advisories.data/CVE-2026-34197-announcement.txt ; https://nvd.nist.gov/vuln/detail/CVE-2026-34197

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-34197)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-34197)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-34197)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-34197)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-34197)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-34197)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```