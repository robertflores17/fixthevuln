# Daily KEV Review — 2026-04-29

**CVEs to review:** 2

---

## CVE-2024-1708: ConnectWise ScreenConnect

**CVSS:** 8.4
**Description:** ConnectWise ScreenConnect contains a path traversal vulnerability which could allow an attacker to execute remote code or directly impact confidential data and critical systems.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-12
**CISA Notes:** https://www.connectwise.com/company/trust/security-bulletins/connectwise-screenconnect-23.9.8 ; https://nvd.nist.gov/vuln/detail/CVE-2024-1708

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2024-1708)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2024-1708)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2024-1708)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2024-1708)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2024-1708)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2024-1708)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-32202: Microsoft Windows

**CVSS:** 4.3
**Description:** Microsoft Windows Shell contains a protection mechanism failure vulnerability that allows an unauthorized attacker to perform spoofing over a network.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-12
**CISA Notes:** https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-32202 ; https://nvd.nist.gov/vuln/detail/CVE-2026-32202

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-32202)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-32202)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-32202)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-32202)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-32202)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-32202)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```