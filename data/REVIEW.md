# Daily KEV Review — 2026-03-05

**CVEs to review:** 2

---

## CVE-2026-22719: Broadcom VMware Aria Operations

**CVSS:** 8.1
**Description:** Broadcom VMware Aria Operations formerly known as vRealize Operations (vROps) contains a command injection vulnerability that allows an unauthenticated attacker to execute arbitrary commands, potentially leading to remote code execution during support‑assisted product migration.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-24
**CISA Notes:** https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/36947 ; https://knowledge.broadcom.com/external/article/430349 ; https://nvd.nist.gov/vuln/detail/CVE-2026-22719

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-22719)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-22719)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-22719)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-22719)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-22719)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-22719)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-21385: Qualcomm Multiple Chipsets

**CVSS:** 7.8
**Description:** Multiple Qualcomm chipsets contain a memory corruption vulnerability while using alignments for memory allocation. 
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-24
**CISA Notes:** https://source.android.com/docs/security/bulletin/2026/2026-03-01 ; https://nvd.nist.gov/vuln/detail/CVE-2026-21385

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-21385)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-21385)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-21385)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-21385)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-21385)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-21385)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```