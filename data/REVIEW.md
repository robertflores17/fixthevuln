# Daily KEV Review — 2026-10-13

**CVEs to review:** 2

---

## CVE-2026-104935: Ivanti Connect Secure

**CVSS:** 8.6
**Description:** Ivanti Connect Secure contains an authentication bypass by spoofing vulnerability that allows a remote unauthenticated attacker to execute arbitrary commands.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-16
**CISA Notes:** https:/forums.ivanti.com/s/article/Security-Advisory-Ivanti-Connect-Secure-CVE-2026-104935 ; https://nvd.nist.gov/vuln/detail/CVE-2026-104935

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-104935)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-104935)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-104935)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-104935)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-104935)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-104935)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-96951: Microsoft Windows

**CVSS:** 8.8
**Description:** Microsoft Windows Shell contains a command injection vulnerability that allows an unauthorized attacker to bypass a security feature over a network.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-16
**CISA Notes:** https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-96951 ; BOD 26-04: BOD 26-04: Prioritizing Security Updates Based on Risk | CISA ; Forensics Triage Requirements: BOD 26-04: Implementation Guidance for Prioritizing Security Updates Based on Risk | CISA ;  https://nvd.nist.gov/vuln/detail/CVE-2026-96951

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-96951)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-96951)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-96951)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-96951)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-96951)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-96951)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```