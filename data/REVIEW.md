# KEV Review - Week of 2026-01-22

**CVEs to review:** 4

---

## CVE-2025-68645: Synacor  Zimbra Collaboration Suite (ZCS)

**Description:** Synacor Zimbra Collaboration Suite (ZCS) contains a PHP remote file inclusion vulnerability that could allow for remote attackers to craft requests to the /h/rest endpoint to influence internal request dispatching, allowing inclusion of arbitrary files from the WebRoot directory.
**Due Date:** 2026-02-12
**CISA Notes:** https://wiki.zimbra.com/wiki/Security_Center ; https://nvd.nist.gov/vuln/detail/CVE-2025-68645

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-68645)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-68645)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-68645)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-68645)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-68645)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-68645)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2025-68645",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2025-34026: Versa Concerto

**Description:** Versa Concerto SD-WAN orchestration platform contains an improper authentication vulnerability in the Traefik reverse proxy configuration, allowing at attacker to access administrative endpoints. The internal Actuator endpoint can be leveraged for access to heap dumps and trace logs.
**Due Date:** 2026-02-12
**CISA Notes:** https://security-portal.versa-networks.com/emailbulletins/6830f94328defa375486ff2e ; https://nvd.nist.gov/vuln/detail/CVE-2025-34026

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-34026)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-34026)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-34026)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-34026)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-34026)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-34026)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2025-34026",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2025-31125: Vite Vitejs

**Description:** Vite Vitejs contains an improper access control vulnerability that exposes content of non-allowed files using ?inline&import or ?raw?import. Only apps explicitly exposing the Vite dev server to the network (using --host or server.host config option) are affected.
**Due Date:** 2026-02-12
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://github.com/vitejs/vite/commit/59673137c45ac2bcfad1170d954347c1a17ab949 ; https://nvd.nist.gov/vuln/detail/CVE-2025-31125

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-31125)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-31125)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-31125)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-31125)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-31125)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-31125)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2025-31125",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2025-54313: Prettier eslint-config-prettier

**Description:** Prettier eslint-config-prettier contains an embedded malicious code vulnerability. Installing an affected package executes an install.js file that launches the node-gyp.dll malware on Windows.
**Due Date:** 2026-02-12
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://www.npmjs.com/package/eslint-config-prettier?activeTab=versions ; https://github.com/prettier/eslint-config-prettier/issues/339#issuecomment-3090304490 ; https://nvd.nist.gov/vuln/detail/CVE-2025-54313

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-54313)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-54313)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-54313)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-54313)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-54313)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-54313)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2025-54313",
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