#!/usr/bin/env python3
"""Replace old Etsy CTAs with FixTheVuln store CTAs on comparison, CVE, and guide pages.
- Comparison pages → store planner CTA for both certs
- CVE pages → Sprint Kit CTA
- Guide pages → contextual planner CTA + Sprint Kit where relevant
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# ── Comparison page cert mapping ─────────────────────────────────────
COMPARISON_MAP = {
    'a-plus-vs-network-plus.html':              [('comptia-a-plus-1201', 'CompTIA A+'), ('comptia-network-plus', 'CompTIA Network+')],
    'aws-saa-vs-aws-sap.html':                  [('aws-solutions-architect', 'AWS Solutions Architect')],
    'aws-saa-vs-aws-security-specialty.html':    [('aws-solutions-architect', 'AWS Solutions Architect'), ('aws-security-specialty', 'AWS Security Specialty')],
    'aws-saa-vs-azure-az-104.html':             [('aws-solutions-architect', 'AWS Solutions Architect'), ('ms-az-104', 'Microsoft Azure Administrator')],
    'azure-az-500-vs-security-plus.html':       [('ms-az-500', 'Azure Security Engineer'), ('comptia-security-plus', 'CompTIA Security+')],
    'casp-plus-vs-cissp.html':                  [('comptia-casp-plus', 'CompTIA CASP+'), ('isc2-cissp', 'ISC2 CISSP')],
    'ccna-vs-network-plus.html':                [('cisco-ccna', 'Cisco CCNA'), ('comptia-network-plus', 'CompTIA Network+')],
    'ceh-vs-pentest-plus.html':                 [('ec-ceh', 'EC-Council CEH'), ('comptia-pentest-plus', 'CompTIA PenTest+')],
    'cissp-vs-cism.html':                       [('isc2-cissp', 'ISC2 CISSP'), ('isaca-cism', 'ISACA CISM')],
    'cissp-vs-security-plus.html':              [('isc2-cissp', 'ISC2 CISSP'), ('comptia-security-plus', 'CompTIA Security+')],
    'cysa-plus-vs-ceh.html':                    [('comptia-cysa-plus', 'CompTIA CySA+'), ('ec-ceh', 'EC-Council CEH')],
    'network-plus-vs-security-plus.html':       [('comptia-network-plus', 'CompTIA Network+'), ('comptia-security-plus', 'CompTIA Security+')],
    'security-plus-vs-cysa-plus.html':          [('comptia-security-plus', 'CompTIA Security+'), ('comptia-cysa-plus', 'CompTIA CySA+')],
    'security-plus-vs-pentest-plus.html':       [('comptia-security-plus', 'CompTIA Security+'), ('comptia-pentest-plus', 'CompTIA PenTest+')],
    'security-plus-vs-sscp.html':               [('comptia-security-plus', 'CompTIA Security+'), ('isc2-sscp', 'ISC2 SSCP')],
}

# ── Guide page cert mapping ──────────────────────────────────────────
GUIDE_MAP = {
    'owasp-top10.html':          [('comptia-pentest-plus', 'CompTIA PenTest+'), ('ec-ceh', 'EC-Council CEH')],
    'incident-response.html':    [('comptia-cysa-plus', 'CompTIA CySA+'), ('giac-gcih', 'GIAC GCIH')],
    'cloud-security.html':       [('aws-security-specialty', 'AWS Security Specialty'), ('ms-az-500', 'Azure Security Engineer')],
    'encryption-cheatsheet.html':[('comptia-security-plus', 'CompTIA Security+')],
    'linux-hardening.html':      [('comptia-linux-plus', 'CompTIA Linux+')],
    'windows-hardening.html':    [('comptia-security-plus', 'CompTIA Security+')],
    'ssl-tls.html':              [('comptia-security-plus', 'CompTIA Security+')],
    'security-headers.html':     [('comptia-security-plus', 'CompTIA Security+')],
    'api-security.html':         [('offsec-oswa', 'OffSec OSWA')],
    'container-security.html':   [('k8s-cks', 'Kubernetes CKS')],
    'secrets-management.html':   [('hashicorp-vault', 'HashiCorp Vault')],
    'database-security.html':    [('comptia-security-plus', 'CompTIA Security+')],
    'log-management.html':       [('comptia-cysa-plus', 'CompTIA CySA+')],
    'password-policy.html':      [('comptia-security-plus', 'CompTIA Security+')],
    'port-security.html':        [('cisco-ccna', 'Cisco CCNA')],
    'quick-fixes.html':          [('comptia-security-plus', 'CompTIA Security+')],
    'network-plus-quiz.html':    [],  # skip — quiz page, handled separately
    'wordpress-security.html':   [('comptia-security-plus', 'CompTIA Security+')],
    'security-analyst-roadmap.html': [('comptia-security-plus', 'CompTIA Security+'), ('isc2-cissp', 'ISC2 CISSP')],
}


# Map vendor ID → store category page path (relative to site root)
VENDOR_STORE_PAGES = {
    'comptia': '/store/comptia.html',
    'isc2': '/store/security-governance.html',
    'aws': '/store/aws.html',
    'microsoft': '/store/microsoft.html',
    'cisco': '/store/cisco.html',
    'isaca': '/store/security-governance.html',
    'giac': '/store/security-governance.html',
    'google': '/store/google-cloud.html',
    'ec-council': '/store/offensive-devops.html',
    'offsec': '/store/offensive-devops.html',
    'hashicorp': '/store/offensive-devops.html',
    'k8s': '/store/offensive-devops.html',
}

# Reverse lookup: product ID prefix → vendor
def _vendor_for_pid(pid):
    """Determine vendor from product ID."""
    vendor_prefixes = {
        'comptia-': 'comptia', 'isc2-': 'isc2', 'aws-': 'aws', 'ms-': 'microsoft',
        'cisco-': 'cisco', 'isaca-': 'isaca', 'giac-': 'giac', 'google-': 'google',
        'ec-': 'ec-council', 'offsec-': 'offsec', 'hashicorp-': 'hashicorp', 'k8s-': 'k8s',
    }
    for prefix, vendor in vendor_prefixes.items():
        if pid.startswith(prefix):
            return vendor
    return None


def store_cta_html(certs, prefix=''):
    """Generate a FixTheVuln store CTA section for given certs."""
    if len(certs) == 1:
        _, name = certs[0]
        heading = f'Get the {name} Study Planner'
    elif len(certs) == 2:
        heading = f'Study Planners Available for Both Certs'
    else:
        heading = 'Get Your Study Planner'

    cert_buttons = ''
    for pid, name in certs:
        vendor = _vendor_for_pid(pid)
        store_url = VENDOR_STORE_PAGES.get(vendor, '/store/store.html')
        cert_buttons += f'            <a href="{prefix}{store_url}" style="display:inline-block;background:#667eea;color:white;padding:0.75rem 1.5rem;border-radius:6px;text-decoration:none;font-weight:600;margin:0.25rem;">{name} Planner</a>\n'

    return f'''        <!-- Store CTA -->
        <section style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem; text-align: center;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.6; margin-bottom: 0.3rem;">FixTheVuln Store</p>
            <h3 style="color: white; margin-bottom: 0.5rem;">{heading}</h3>
            <p style="opacity: 0.9; margin-bottom: 1rem;">Fillable PDF study planners with domain trackers, weekly schedules, and progress tracking. Available in Standard, ADHD-Friendly, Dark Mode, and 4-Format Bundle.</p>
{cert_buttons}            <p style="font-size: 0.8rem; opacity: 0.85; margin-top: 0.75rem;">60+ certifications available &mdash; from $5.99</p>
        </section>
'''


def sprint_kit_cta_html(prefix=''):
    """Generate a Sprint Kit CTA for CVE and vulnerability-focused pages."""
    return f'''        <!-- Sprint Kit CTA -->
        <section style="background: linear-gradient(135deg, #0a2e1a 0%, #1a3a2e 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem; text-align: center;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.6; margin-bottom: 0.3rem;">FixTheVuln Store</p>
            <h3 style="color: white; margin-bottom: 0.5rem;">Patch Tuesday Sprint Kit</h3>
            <p style="opacity: 0.9; margin-bottom: 1rem;">5 fillable templates for vulnerability triage, sprint planning, testing, SLA tracking, and executive reporting. Free blank templates or $4.99/mo for pre-filled intelligence with real CISA KEV data.</p>
            <a href="{prefix}/store/patch-tuesday-kit.html" style="display:inline-block;background:#10b981;color:white;padding:0.75rem 1.5rem;border-radius:6px;text-decoration:none;font-weight:600;margin:0.25rem;">Try Free Templates</a>
            <a href="https://buy.stripe.com/fZudRa2L8dCz73c7Kc1oI00" style="display:inline-block;background:#667eea;color:white;padding:0.75rem 1.5rem;border-radius:6px;text-decoration:none;font-weight:600;margin:0.25rem;">Subscribe &mdash; $4.99/mo</a>
        </section>
'''


def replace_etsy_cta(text, new_cta):
    """Replace the <!-- Etsy CTA --> section with new CTA HTML."""
    pattern = r'        <!-- Etsy CTA -->\n        <section style="background: linear-gradient\(135deg.*?</section>\n'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return text[:match.start()] + new_cta + text[match.end():]
    return None


def replace_planner_cta(text, new_cta):
    """Replace the <!-- Certification Study Planner --> section with new CTA HTML."""
    pattern = r'        <!-- Certification Study Planner -->\n        <section style="background: linear-gradient\(135deg.*?</section>\n'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return text[:match.start()] + new_cta + text[match.end():]
    return None


def process_comparisons():
    """Update comparison pages: Etsy CTA → store planner CTA."""
    comp_dir = REPO / 'comparisons'
    updated = 0
    for filename, certs in COMPARISON_MAP.items():
        filepath = comp_dir / filename
        if not filepath.exists():
            print(f"  MISS {filename}")
            continue
        text = filepath.read_text(encoding='utf-8')
        if '<!-- Store CTA -->' in text:
            print(f"  SKIP {filename} — already updated")
            continue
        new_cta = store_cta_html(certs, prefix='..')
        result = replace_etsy_cta(text, new_cta)
        if result:
            filepath.write_text(result, encoding='utf-8')
            print(f"  OK   comparisons/{filename}")
            updated += 1
        else:
            print(f"  WARN {filename} — could not find Etsy CTA section")
    return updated


def process_cve_pages():
    """Update CVE pages: Etsy CTA → Sprint Kit CTA."""
    cve_dir = REPO / 'cve'
    if not cve_dir.exists():
        print("  CVE directory not found")
        return 0
    updated = 0
    for filepath in sorted(cve_dir.glob('CVE-*.html')):
        text = filepath.read_text(encoding='utf-8')
        if '<!-- Sprint Kit CTA -->' in text:
            print(f"  SKIP {filepath.name} — already updated")
            continue
        new_cta = sprint_kit_cta_html(prefix='..')
        result = replace_etsy_cta(text, new_cta)
        if result:
            filepath.write_text(result, encoding='utf-8')
            print(f"  OK   cve/{filepath.name}")
            updated += 1
        else:
            print(f"  WARN {filepath.name} — could not find Etsy CTA section")
    return updated


def process_guides():
    """Update guide pages: replace planner CTA with store CTA + Sprint Kit."""
    updated = 0
    for filename, certs in GUIDE_MAP.items():
        if not certs:
            continue
        filepath = REPO / filename
        if not filepath.exists():
            print(f"  MISS {filename}")
            continue
        text = filepath.read_text(encoding='utf-8')
        if '<!-- Store CTA -->' in text:
            print(f"  SKIP {filename} — already updated")
            continue

        new_cta = store_cta_html(certs, prefix='')
        # Also add Sprint Kit CTA for security-focused guides
        security_guides = ['incident-response.html', 'owasp-top10.html', 'security-headers.html',
                          'quick-fixes.html', 'log-management.html', 'security-analyst-roadmap.html']
        if filename in security_guides:
            new_cta += sprint_kit_cta_html(prefix='')

        # Try replacing existing planner CTA first
        result = replace_planner_cta(text, new_cta)
        if result:
            filepath.write_text(result, encoding='utf-8')
            print(f"  OK   {filename} (replaced planner CTA)")
            updated += 1
            continue

        # Try replacing Etsy CTA
        result = replace_etsy_cta(text, new_cta)
        if result:
            filepath.write_text(result, encoding='utf-8')
            print(f"  OK   {filename} (replaced Etsy CTA)")
            updated += 1
            continue

        # Inject before </main> as fallback
        main_close = text.rfind('    </main>')
        if main_close > 0:
            text = text[:main_close] + '\n' + new_cta + '\n' + text[main_close:]
            filepath.write_text(text, encoding='utf-8')
            print(f"  OK   {filename} (injected before </main>)")
            updated += 1
        else:
            print(f"  WARN {filename} — no injection point found")

    return updated


def main():
    print("=== Updating Comparison Pages ===")
    c1 = process_comparisons()
    print(f"\n=== Updating CVE Pages ===")
    c2 = process_cve_pages()
    print(f"\n=== Updating Guide Pages ===")
    c3 = process_guides()
    print(f"\nDone: {c1} comparisons, {c2} CVE pages, {c3} guides updated")


if __name__ == '__main__':
    main()
