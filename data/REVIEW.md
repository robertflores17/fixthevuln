# Daily KEV Review — 2026-05-30

**CVEs to review:** 1

---

## CVE-2026-0257: Palo Alto Networks PAN-OS

**CVSS:** 9.1
**Description:** Palo Alto Networks PAN-OS contains an authentication bypass vulnerability that allows attackers to bypass security restrictions and establish an unauthorized VPN connection.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-01
**CISA Notes:** https://security.paloaltonetworks.com/CVE-2026-0257 ; https://nvd.nist.gov/vuln/detail/CVE-2026-0257

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-0257)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-0257)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-0257)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-0257)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-0257)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-0257)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```