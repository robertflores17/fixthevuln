# Daily KEV Review — 2026-09-19

**CVEs to review:** 1

---

## CVE-2025-39682: Linux Kernel

**CVSS:** 7.1
**Description:** Linux Kernel contains an improper check for unusual or exceptional conditions vulnerability in the TLS receive path which allows a zero-length record retrieved from the rx_list to bypass the intended recvmsg() record-type handling, potentially causing subsequent TLS records to be processed using incorrect zero-copy and queuing assumptions. The impacted product(s) could be end-of-life (EoL) and/or end-of-service (EoS). Users are advised to discontinue use and/or transition to a supported version.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-21
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: ; https://git.kernel.org/stable/c/2902c3ebcca52ca845c03182000e8d71d3a5196f; https://git.kernel.org/stable/c/c09dd3773b5950e9cfb6c9b9a5f6e36d06c62677; https://git.kernel.org/stable/c/3439c15ae91a517cf3c650ea15a8987699416ad9; https://git.kernel.org/stable/c/29c0ce3c8cdb6dc5d61139c937f34cb888a6f42e; https://git.kernel.org/stable/c/62708b9452f8eb77513115b17c4f8d1a22ebf843 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2025-39682

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-39682)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-39682)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-39682)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-39682)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-39682)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-39682)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```