# Daily KEV Review — 2026-05-07

**CVEs to review:** 2

---

## CVE-2026-6973: Ivanti Endpoint Manager Mobile (EPMM)

**CVSS:** 7.2
**Description:** Ivanti Endpoint Manager Mobile (EPMM) contains an improper input validation vulnerability that allows a remotely authenticated user with administrative access to achieve remote code execution.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-10
**CISA Notes:** https://hub.ivanti.com/s/article/May-2026-Security-Advisory-Ivanti-Endpoint-Manager-Mobile-EPMM-Multiple-CVEs?language=en_US ; https://nvd.nist.gov/vuln/detail/CVE-2026-6973

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-6973)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-6973)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-6973)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-6973)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-6973)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-6973)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-0300: Palo Alto Networks PAN-OS

**CVSS:** 9.3
**Description:** Palo Alto Networks PAN-OS contains an out-of-bounds write vulnerability in the User-ID Authentication Portal (aka Captive Portal) service that can allow an unauthenticated attacker to execute arbitrary code with root privileges on the PA-Series and VM-Series firewalls by sending specially crafted packets.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.    Until the vendor releases an official fix, the following workaround should be implemented:  - Restrict User-ID Authentication Portal access to only trusted zones.  - Disable User-ID Authentication Portal if not required.
**Due Date:** 2026-05-09
**CISA Notes:** https://security.paloaltonetworks.com/CVE-2026-0300 ; https://nvd.nist.gov/vuln/detail/CVE-2026-0300

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-0300)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-0300)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-0300)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-0300)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-0300)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-0300)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```