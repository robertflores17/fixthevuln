# KEV Review - Week of 2026-01-21

**CVEs to review:** 1

---

## CVE-2026-20045: Cisco Unified Communications Manager

**Description:** Cisco Unified Communications Manager (Unified CM), Cisco Unified Communications Manager Session Management Edition (Unified CM SME), Cisco Unified Communications Manager IM & Presence Service (Unified CM IM&P), Cisco Unity Connection, and Cisco Webex Calling Dedicated Instance contain a code injection vulnerability that could allow the attacker to obtain user-level access to the underlying operating system and then elevate privileges to root.
**Due Date:** 2026-02-11
**CISA Notes:** https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-voice-rce-mORhqY4b ; https://nvd.nist.gov/vuln/detail/CVE-2026-20045

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-20045)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-20045)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-20045)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-20045)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-20045)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-20045)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2026-20045",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## Ready-to-Paste HTML

After filling in the fields above, run:
```bash
python scripts/generate_html.py
```

Or manually create cards in this format:
```html
<div class="kev-card">
    <h4>Vendor Product</h4>
    <div class="cve-id">CVE-XXXX-XXXXX | CVSS X.X</div>
    <p>Your short description.</p>
    <div class="kev-fix"><strong>Fix:</strong> Your remediation.</div>
</div>
```