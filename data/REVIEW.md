# Daily KEV Review — 2026-05-22

**CVEs to review:** 2

---

## CVE-2025-34291: Langflow Langflow

**CVSS:** 8.8
**Description:** Langflow contains an origin validation error vulnerability in which an overly permissive CORS configuration combined with a refresh token cookie configured as SameSite=None allows a malicious webpage to perform cross-origin requests that include credentials and successfully call the refresh endpoint. This could allow the attacker to execute arbitrary code and achieve full system compromise via obtained tokens that permit access to authenticated endpoints.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-04
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://github.com/langflow-ai/langflow ; https://github.com/langflow-ai/langflow/releases/tag/v1.9.3; https://github.com/langflow-ai/langflow/issues/11465#event-25774545848 ; https://nvd.nist.gov/vuln/detail/CVE-2025-34291

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-34291)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-34291)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-34291)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-34291)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-34291)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-34291)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-34926: Trend Micro Apex One

**CVSS:** 6.7
**Description:** Trend Micro Apex One (on-premise) contains a directory traversal vulnerability that could allow a pre-authenticated local attacker to modify a key table on the server to inject malicious code to deploy to agents on affected installations.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-04
**CISA Notes:** https://success.trendmicro.com/en-US/solution/KA-0023430 ; https://nvd.nist.gov/vuln/detail/CVE-2026-34926

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-34926)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-34926)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-34926)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-34926)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-34926)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-34926)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```