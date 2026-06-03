# Daily KEV Review — 2026-06-03

**CVEs to review:** 1

---

## CVE-2026-45247: Mirasvit Mirasvit Full Page Cache Warmer

**CVSS:** 9.8
**Description:** Mirasvit Full Page Cache Warmer contains a deserialization of untrusted data vulnerability that could allow unauthenticated attackers to achieve remote code execution by supplying a crafted serialized PHP object in the CacheWarmer cookie.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-06
**CISA Notes:** https://mirasvit.com/package/changelog/?package=mirasvit/module-cache-warmer ; https://nvd.nist.gov/vuln/detail/CVE-2026-45247

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-45247)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-45247)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-45247)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-45247)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-45247)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-45247)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```