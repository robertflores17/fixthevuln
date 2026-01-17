# FixTheVuln

**Learn Security. Master Remediation.**

A free, open educational platform for vulnerability remediation. Quick reference guides, interactive tools, and curated resources for security professionals and students.

**Live site:** [https://fixthevuln.com](https://fixthevuln.com)

---

## Features

- **Quick Reference Guides** - 19 security cheat sheets (OWASP Top 10, SSL/TLS hardening, incident response, etc.)
- **Interactive Tools** - 20 browser-based tools (CVSS calculator, hash generator, JWT decoder, etc.)
- **Compliance Frameworks** - NIST, CIS Controls, PCI DSS, GDPR, SOC 2 guides
- **KEV Tracking** - Automated CISA Known Exploited Vulnerabilities updates
- **Learning Path** - Structured journey from fundamentals to advanced topics

---

## Project Structure

```
├── index.html              # Homepage
├── guides.html             # Quick Reference Guides
├── tools.html              # Interactive Tools
├── compliance.html         # Compliance & Frameworks
├── start-here.html         # Learning Path
├── resources.html          # Recommended Resources
├── style.css               # Main stylesheet
│
├── scripts/
│   ├── fetch_kev.py        # Fetches CISA KEV catalog
│   └── generate_html.py    # Generates HTML cards from reviewed CVEs
│
├── data/
│   ├── pending_review.json # CVEs awaiting review
│   ├── seen_cves.json      # Tracks already-seen CVEs
│   ├── kev.json            # Full CISA catalog (reference)
│   └── REVIEW.md           # Review guide with expert links
│
└── .github/workflows/
    ├── fetch-vulnerabilities.yml  # Daily KEV fetch → creates PR
    └── friday-reminder.yml        # Weekly review reminder
```

---

## KEV Automation Workflow

The site automatically tracks CISA's Known Exploited Vulnerabilities catalog:

1. **Daily fetch** (6 AM UTC) - GitHub Action fetches new CVEs
2. **PR created** - New vulnerabilities added to `pending_review.json`
3. **Friday reminder** - Issue created with pending items
4. **Weekend review** - Manual review using expert links
5. **Publish** - Generate HTML cards and update site

### Manual Review Process

```bash
# 1. Check data/REVIEW.md for expert links (NVD, AttackerKB, BleepingComputer, etc.)

# 2. Edit data/pending_review.json
{
  "cvss": "CVSS 9.8",
  "short_description": "Your summary",
  "fix": "Your remediation",
  "include_on_site": true
}

# 3. Generate HTML cards
python scripts/generate_html.py

# 4. Paste into index.html KEV section
```

---

## Local Development

```bash
# Clone the repo
git clone https://github.com/robertflores17/fixthevuln.git
cd fixthevuln

# Serve locally (Python)
python -m http.server 8000

# Open http://localhost:8000
```

---

## Contributing

Suggestions, corrections, and contributions welcome! Open an issue or submit a PR.

---

## License

Content is provided for educational purposes.

---

## Contact

- **Website:** [fixthevuln.com](https://fixthevuln.com)
- **Email:** hello@fixthevuln.com
