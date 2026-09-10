# Daily KEV Review — 2026-09-10

**CVEs to review:** 4

---

## CVE-2026-19490: Citrix NetScaler

**CVSS:** 9.8
**Description:** Citrix NetScaler ADC and NetScaler Gateway contain an authentication-bypass vulnerability involving an alternate path or channel. When the NetScaler appliance is configured as an AAA virtual server or as a Gateway (SSL VPN, ICA Proxy, CVPN, or RDP Proxy), an unauthenticated remote threat actor may be able to bypass authentication.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-12
**CISA Notes:** https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-19490

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-19490)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-19490)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-19490)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-19490)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-19490)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-19490)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2025-25249: Fortinet Multiple Products

**CVSS:** 8.1
**Description:** Fortinet FortiOS, FortiSwitchManager, and FortiSASE contain a heap-based buffer overflow vulnerability that allows an attacker to execute unauthorized code or commands via specially crafted packets.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-12
**CISA Notes:** https://fortiguard.fortinet.com/psirt/FG-IR-25-084 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2025-25249

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-25249)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-25249)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-25249)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-25249)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-25249)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-25249)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-87491: Google Chromium V8

**CVSS:** 8.8
**Description:** Google Chromium V8 contains an out of bounds write vulnerability that allows a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. This vulnerability could affect multiple web browsers that utilize Chromium, including, but not limited to, Google Chrome, Microsoft Edge, and Opera.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-23
**CISA Notes:** https://chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_0808145027.html ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-87491 

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-87491)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-87491)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-87491)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-87491)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-87491)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-87491)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-20079: Cisco Secure Firewall Management Center (FMC) and Security Cloud Control (SCC) Firewall Management

**CVSS:** 10.0
**Description:** Cisco Secure Firewall Management Center (FMC) Software and Cisco Security Cloud Control (SCC) Firewall Management contain an authentication Bypass using an alternate path or channel vulnerability that could allow an unauthenticated, remote attacker to bypass authentication and execute script files on an affected device to obtain root access to the underlying operating system.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-12
**CISA Notes:** https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-20079

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-20079)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-20079)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-20079)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-20079)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-20079)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-20079)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```