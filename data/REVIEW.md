# Daily KEV Review — 2026-09-18

**CVEs to review:** 2

---

## CVE-2025-39964: Linux Kernel

**CVSS:** 7.8
**Description:** Linux Kernel contains a race condition vulnerability which allows concurrent writes to the same AF_ALG socket causing data to be unpredictably interleaved and creating inconsistencies in the socket's internal state.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-21
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: ; https://git.kernel.org/stable/c/0f28c4adbc4a97437874c9b669fd7958a8c6d6ce; https://git.kernel.org/stable/c/e4c1ec11132ec466f7362a95f36a506ce4dc08c9; https://git.kernel.org/stable/c/1f323a48e9b5ebfe6dc7d130fdf5c3c0e92a07c8; https://git.kernel.org/stable/c/7c4491b5644e3a3708f3dbd7591be0a570135b84; https://git.kernel.org/stable/c/9aee87da5572b3a14075f501752e209801160d3d; https://git.kernel.org/stable/c/45bcf60fe49b37daab1acee57b27211ad1574042; https://git.kernel.org/stable/c/1b34cbbf4f011a121ef7b2d7d6e6920a036d5285 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2025-39964

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-39964)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-39964)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-39964)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-39964)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-39964)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-39964)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-53266: Linux Kernel

**CVSS:** 8.8
**Description:** Linux Kernel contains an out-of-bounds write vulnerability in the ebtables SNAT target which allows an ARP sender hardware address rewrite to write directly into a nonlinear socket-buffer fragment backed by a splice-imported file page. The impacted product(s) could be end-of-life (EoL) and/or end-of-service (EoS). Users are advised to discontinue use and/or transition to a supported version.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-21
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: ; https://git.kernel.org/stable/c/bf84ad7c7a9ede46e31afaa41a1ba06a159e8c87; https://git.kernel.org/stable/c/76280b78cc9f23bdc6438e10ad6dff148ef8375b; https://git.kernel.org/stable/c/b7e91939ba9be805a62a257fa4e227dffbb88fa0; https://git.kernel.org/stable/c/afd64b59c3de9bbbdd3759e834fdc55cda716e0b; https://git.kernel.org/stable/c/153ea96c806aea395daba907a4f88480b6ad5093; https://git.kernel.org/stable/c/b18675263db1147c8e1cab625400c13a0d87bd2d; https://git.kernel.org/stable/c/c9b5ff59feffb92a147a84a5aa28acd2cb8ff4c5; https://git.kernel.org/stable/c/67ba971ae02514d85818fe0c32549ab4bfa3bf49 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-53266

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-53266)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-53266)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-53266)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-53266)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-53266)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-53266)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```