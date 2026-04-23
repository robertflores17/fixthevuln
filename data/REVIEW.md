# Daily KEV Review — 2026-04-23

**CVEs to review:** 1

---

## CVE-2026-33825: Microsoft Defender

**CVSS:** 7.8
**Description:** Microsoft Defender contains an insufficient granularity of access control vulnerability that could allow an authorized attacker to escalate privileges locally.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-06
**CISA Notes:** https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-33825 ; https://nvd.nist.gov/vuln/detail/CVE-2026-33825

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-33825)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-33825)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-33825)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-33825)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-33825)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-33825)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```