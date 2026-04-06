# Daily KEV Review — 2026-04-06

**CVEs to review:** 7

---

## CVE-2026-35616: Fortinet FortiClient EMS

**CVSS:** 9.8
**Description:** Fortinet FortiClient EMS contains an improper access control vulnerability that may allow an unauthenticated attacker to execute unauthorized code or commands via crafted requests.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-04-09
**CISA Notes:** Please adhere to Fortinet's guidelines to assess exposure and mitigate risks. Check for signs of potential compromise on all internet accessible Fortinet products affected by this vulnerability. Apply any final mitigations provided by the vendor as soon as they become available. For more information please see: https://fortiguard.fortinet.com/psirt/FG-IR-26-099 ; https://nvd.nist.gov/vuln/detail/CVE-2026-35616

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-35616)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-35616)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-35616)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-35616)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-35616)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-35616)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-3502: TrueConf Client

**CVSS:** 7.8
**Description:** TrueConf Client contains a download of code without integrity check vulnerability. An attacker who is able to influence the update delivery path can substitute a tampered update payload. If the payload is executed or installed by the updater, this may result in arbitrary code execution in the context of the updating process or user.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-04-16
**CISA Notes:** https://trueconf.com/blog/update/trueconf-8-5 ; https://trueconf.com/downloads/windows.html ; https://nvd.nist.gov/vuln/detail/CVE-2026-3502

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-3502)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-3502)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-3502)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-3502)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-3502)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-3502)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-5281: Google Dawn

**CVSS:** 8.8
**Description:** Google Dawn contains an use-after-free vulnerability that could allow a remote attacker who had compromised the renderer process to execute arbitrary code via a crafted HTML page. This vulnerability could affect multiple Chromium-based products including, but not limited to, Google Chrome, Microsoft Edge, and Opera.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-04-15
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://chromereleases.googleblog.com/2026/03/stable-channel-update-for-desktop_31.html ; https://nvd.nist.gov/vuln/detail/CVE-2026-5281 

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-5281)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-5281)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-5281)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-5281)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-5281)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-5281)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-3055: Citrix NetScaler

**CVSS:** 9.8
**Description:** Citrix NetScaler ADC (formerly Citrix ADC), NetScaler Gateway (formerly Citrix Gateway) and NetScaler ADC FIPS and NDcPP contain an out-of-bounds reads vulnerability when configured as a SAML IDP leading to memory overread.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-04-02
**CISA Notes:** https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696300&articleURL=NetScaler_ADC_and_NetScaler_Gateway_Security_Bulletin_for_CVE_2026_3055_and_CVE_2026_4368 ; https://nvd.nist.gov/vuln/detail/CVE-2026-3055

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-3055)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-3055)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-3055)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-3055)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-3055)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-3055)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2025-53521: F5 BIG-IP

**CVSS:** 9.8
**Description:** F5 BIG-IP APM contains a stack-based buffer overflow vulnerability that could allow a threat actor to achieve remote code execution.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-30
**CISA Notes:** Please adhere to F5’s guidelines to assess exposure and mitigate risks. Check for signs of potential compromise on all internet accessible F5 products affected by this vulnerability. For more information please see: https://my.f5.com/manage/s/article/K000156741 ; https://my.f5.com/manage/s/article/K000160486 ; https://my.f5.com/manage/s/article/K11438344 ; https://nvd.nist.gov/vuln/detail/CVE-2025-53521

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-53521)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-53521)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-53521)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-53521)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-53521)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-53521)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-33634: Aquasecurity Trivy

**CVSS:** 8.8
**Description:** Aquasecurity Trivy contains an embedded malicious code vulnerability that could allow an attacker to gain access to everything in the CI/CD environment, including all tokens, SSH keys, cloud credentials, database passwords, and any sensitive configuration in memory.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-04-09
**CISA Notes:** This vulnerability involves a supply‑chain compromise in a product that may be used across multiple products and environments. Additional vendor‑provided guidance must be followed to ensure full remediation. For more information, please see: https://github.com/advisories/GHSA-69fq-xp46-6x23 ; https://nvd.nist.gov/vuln/detail/CVE-2026-33634

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-33634)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-33634)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-33634)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-33634)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-33634)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-33634)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-33017: Langflow Langflow

**CVSS:** 9.8
**Description:** Langflow contains a code injection vulnerability that could allow building public flows without requiring authentication.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-04-08
**CISA Notes:** https://github.com/langflow-ai/langflow/security/advisories/GHSA-vwmf-pq79-vjvx ; https://nvd.nist.gov/vuln/detail/CVE-2026-33017

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-33017)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-33017)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-33017)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-33017)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-33017)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-33017)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```