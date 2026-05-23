# Daily KEV Review — 2026-05-23

**CVEs to review:** 1

---

## CVE-2026-9082: Drupal Core

**CVSS:** 6.5
**Description:** Drupal Core contains a SQL injection vulnerability that could allow for privilege escalation and remote code execution via specially crafted requests sent with the database abstraction API.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-27
**CISA Notes:** https://www.drupal.org/sa-core-2026-004 ; https://nvd.nist.gov/vuln/detail/CVE-2026-9082

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-9082)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-9082)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-9082)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-9082)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-9082)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-9082)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```