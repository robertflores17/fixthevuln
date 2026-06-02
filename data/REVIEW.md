# Daily KEV Review — 2026-06-02

**CVEs to review:** 2

---

## CVE-2022-0492: Linux Kernel

**CVSS:** 7.8
**Description:** Linux Kernel contains an improper authentication vulnerability which could allow for privilege escalation via the cgroups v1 release_agent feature.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-05
**CISA Notes:** This vulnerability affects a common open-source component, third-party library, or a protocol used by different products. Please check with specific vendors for information on patching status. For more information, please see: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=24f6008564183aa120d07c03d9289519c2fe02af ; https://www.kernel.org/ ; https://nvd.nist.gov/vuln/detail/CVE-2022-0492

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2022-0492)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2022-0492)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2022-0492)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2022-0492)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2022-0492)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2022-0492)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2025-48595: Android Framework

**CVSS:** 8.4
**Description:** Android Framework contains an integer overflow vulnerability that allows for code execution that could allow for local privilege escalation.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-05
**CISA Notes:** https://source.android.com/docs/security/bulletin/2026/2026-06-01 ; https://nvd.nist.gov/vuln/detail/CVE-2025-48595

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-48595)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-48595)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-48595)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-48595)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-48595)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-48595)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```