#!/usr/bin/env python3
"""Generate SEO landing pages for all certifications in the store catalog.
Each page targets "[cert name] study guide" search queries and funnels
visitors to quizzes and planner purchases."""

import json
import re
from datetime import datetime
from pathlib import Path
from html import escape

REPO = Path(__file__).resolve().parent.parent
CERTS_DIR = REPO / 'certs'
ETSY_CERTS = Path(__file__).resolve().parent.parent.parent / 'Dropshipping' / 'Etsy-Claude' / 'certifications'

# ── Product catalog (from store.js) ──────────────────────────────────
PRODUCTS = [
    {'id': 'comptia-a-plus-1201',     'vendor': 'comptia',    'name': 'CompTIA A+ Core 1',            'meta': '220-1201 · 5 domains', 'config': 'comptia/a_plus_1201.json'},
    {'id': 'comptia-a-plus-1202',     'vendor': 'comptia',    'name': 'CompTIA A+ Core 2',            'meta': '220-1202 · 4 domains', 'config': 'comptia/a_plus_1202.json'},
    {'id': 'comptia-security-plus',   'vendor': 'comptia',    'name': 'CompTIA Security+',            'meta': 'SY0-701 · 5 domains',  'config': 'comptia/security_plus_701.json'},
    {'id': 'comptia-network-plus',    'vendor': 'comptia',    'name': 'CompTIA Network+',             'meta': 'N10-009 · 5 domains',  'config': 'comptia/network_plus_009.json'},
    {'id': 'comptia-linux-plus',      'vendor': 'comptia',    'name': 'CompTIA Linux+',               'meta': 'XK0-006 · 4 domains',  'config': 'comptia/linux_plus_006.json'},
    {'id': 'comptia-cloud-plus',      'vendor': 'comptia',    'name': 'CompTIA Cloud+',               'meta': 'CV0-004 · 4 domains',  'config': 'comptia/cloud_plus_004.json'},
    {'id': 'comptia-cysa-plus',       'vendor': 'comptia',    'name': 'CompTIA CySA+',                'meta': 'CS0-003 · 4 domains',  'config': 'comptia/cysa_plus_003.json'},
    {'id': 'comptia-pentest-plus',    'vendor': 'comptia',    'name': 'CompTIA PenTest+',             'meta': 'PT0-003 · 5 domains',  'config': 'comptia/pentest_plus_003.json'},
    {'id': 'comptia-casp-plus',       'vendor': 'comptia',    'name': 'CompTIA CASP+',                'meta': 'CAS-005 · 4 domains',  'config': 'comptia/casp_plus_005.json'},
    {'id': 'comptia-server-plus',     'vendor': 'comptia',    'name': 'CompTIA Server+',              'meta': 'SK0-005 · 4 domains',  'config': 'comptia/server_plus_005.json'},
    {'id': 'comptia-data-plus',       'vendor': 'comptia',    'name': 'CompTIA Data+',                'meta': 'DA0-001 · 5 domains',  'config': 'comptia/data_plus_001.json'},
    {'id': 'comptia-project-plus',    'vendor': 'comptia',    'name': 'CompTIA Project+',             'meta': 'PK0-005 · 5 domains',  'config': 'comptia/project_plus_005.json'},
    {'id': 'comptia-itf-plus',        'vendor': 'comptia',    'name': 'CompTIA ITF+',                 'meta': 'FC0-U71 · 6 domains',  'config': 'comptia/itf_plus_u71.json'},
    {'id': 'isc2-cc',                 'vendor': 'isc2',       'name': 'ISC2 CC',                      'meta': 'CC · 5 domains',        'config': 'isc2/cc.json'},
    {'id': 'isc2-sscp',               'vendor': 'isc2',       'name': 'ISC2 SSCP',                    'meta': 'SSCP · 7 domains',      'config': 'isc2/sscp.json'},
    {'id': 'isc2-cissp',              'vendor': 'isc2',       'name': 'ISC2 CISSP',                   'meta': 'CISSP 2026 · 8 domains','config': 'isc2/cissp_2026.json'},
    {'id': 'isc2-ccsp',               'vendor': 'isc2',       'name': 'ISC2 CCSP',                    'meta': 'CCSP · 6 domains',      'config': 'isc2/ccsp.json'},
    {'id': 'aws-cloud-practitioner',  'vendor': 'aws',        'name': 'AWS Cloud Practitioner',       'meta': 'CLF-C02 · 4 domains',   'config': 'aws/aws_cloud_practitioner_clf-c02.json'},
    {'id': 'aws-solutions-architect', 'vendor': 'aws',        'name': 'AWS Solutions Architect',       'meta': 'SAA-C03 · 4 domains',   'config': 'aws/aws_solutions_architect_saa-c03.json'},
    {'id': 'aws-developer',           'vendor': 'aws',        'name': 'AWS Developer Associate',       'meta': 'DVA-C02 · 4 domains',   'config': 'aws/developer_dva-c02.json'},
    {'id': 'aws-cloudops',            'vendor': 'aws',        'name': 'AWS CloudOps Engineer',         'meta': 'SOA-C03 · 6 domains',   'config': 'aws/cloudops_engineer_soa-c03.json'},
    {'id': 'aws-security-specialty',  'vendor': 'aws',        'name': 'AWS Security Specialty',        'meta': 'SCS-C03 · 6 domains',   'config': 'aws/security_specialty_scs-c03.json'},
    {'id': 'aws-database-specialty',  'vendor': 'aws',        'name': 'AWS Database Specialty',        'meta': 'DBS-C01 · 5 domains',   'config': 'aws/database_specialty_dbs-c01.json'},
    {'id': 'aws-machine-learning',    'vendor': 'aws',        'name': 'AWS Machine Learning',          'meta': 'MLS-C01 · 4 domains',   'config': 'aws/machine_learning_mls-c01.json'},
    {'id': 'aws-data-engineer',       'vendor': 'aws',        'name': 'AWS Data Engineer',             'meta': 'DEA-C01 · 4 domains',   'config': 'aws/data_engineer_dea-c01.json'},
    {'id': 'ms-az-900',               'vendor': 'microsoft',  'name': 'Microsoft Azure Fundamentals',  'meta': 'AZ-900 · 3 domains',    'config': 'microsoft/az-900.json'},
    {'id': 'ms-az-104',               'vendor': 'microsoft',  'name': 'Microsoft Azure Administrator', 'meta': 'AZ-104 · 5 domains',    'config': 'microsoft/az-104.json'},
    {'id': 'ms-az-305',               'vendor': 'microsoft',  'name': 'Azure Solutions Architect',     'meta': 'AZ-305 · 4 domains',    'config': 'microsoft/az-305.json'},
    {'id': 'ms-sc-900',               'vendor': 'microsoft',  'name': 'Security Fundamentals',         'meta': 'SC-900 · 4 domains',    'config': 'microsoft/sc-900.json'},
    {'id': 'ms-ai-900',               'vendor': 'microsoft',  'name': 'Azure AI Fundamentals',         'meta': 'AI-900 · 5 domains',    'config': 'microsoft/ai-900.json'},
    {'id': 'ms-az-500',               'vendor': 'microsoft',  'name': 'Azure Security Engineer',       'meta': 'AZ-500 · 4 domains',    'config': 'microsoft/az-500.json'},
    {'id': 'ms-az-204',               'vendor': 'microsoft',  'name': 'Azure Developer Associate',     'meta': 'AZ-204 · 5 domains',    'config': 'microsoft/az-204.json'},
    {'id': 'ms-az-400',               'vendor': 'microsoft',  'name': 'Azure DevOps Engineer',         'meta': 'AZ-400 · 8 domains',    'config': 'microsoft/az-400.json'},
    {'id': 'ms-dp-900',               'vendor': 'microsoft',  'name': 'Azure Data Fundamentals',       'meta': 'DP-900 · 3 domains',    'config': 'microsoft/dp-900.json'},
    {'id': 'ms-ms-900',               'vendor': 'microsoft',  'name': 'Microsoft 365 Fundamentals',    'meta': 'MS-900 · 4 domains',    'config': 'microsoft/ms-900.json'},
    {'id': 'ms-sc-300',               'vendor': 'microsoft',  'name': 'Identity & Access Admin',       'meta': 'SC-300 · 4 domains',    'config': 'microsoft/sc-300.json'},
    {'id': 'ms-ai-102',               'vendor': 'microsoft',  'name': 'Azure AI Engineer',             'meta': 'AI-102 · 5 domains',    'config': 'microsoft/ai-102.json'},
    {'id': 'cisco-ccna',              'vendor': 'cisco',      'name': 'Cisco CCNA',                    'meta': '200-301 · 6 domains',   'config': 'cisco/ccna_200-301.json'},
    {'id': 'cisco-ccnp-encor',        'vendor': 'cisco',      'name': 'Cisco CCNP ENCOR',              'meta': '350-401 · 6 domains',   'config': 'cisco/ccnp_enterprise_encor.json'},
    {'id': 'cisco-cyberops',          'vendor': 'cisco',      'name': 'Cisco CyberOps Associate',      'meta': '200-201 · 5 domains',   'config': 'cisco/cyberops_200-201.json'},
    {'id': 'cisco-ccnp-security',     'vendor': 'cisco',      'name': 'Cisco CCNP Security SCOR',      'meta': '350-701 · 5 domains',   'config': 'cisco/ccnp_security_scor_350-701.json'},
    {'id': 'cisco-devnet',            'vendor': 'cisco',      'name': 'Cisco DevNet Associate',         'meta': '200-901 · 6 domains',   'config': 'cisco/devnet_associate_200-901.json'},
    {'id': 'isaca-cisa',              'vendor': 'isaca',      'name': 'ISACA CISA',                    'meta': 'CISA · 5 domains',      'config': 'isaca/cisa.json'},
    {'id': 'isaca-cism',              'vendor': 'isaca',      'name': 'ISACA CISM',                    'meta': 'CISM 2026 · 4 domains', 'config': 'isaca/cism_2026.json'},
    {'id': 'isaca-crisc',             'vendor': 'isaca',      'name': 'ISACA CRISC',                   'meta': 'CRISC · 4 domains',     'config': 'isaca/crisc.json'},
    {'id': 'giac-gsec',               'vendor': 'giac',       'name': 'GIAC GSEC',                     'meta': 'GSEC · 7 domains',      'config': 'giac/giac_gsec.json'},
    {'id': 'giac-gcih',               'vendor': 'giac',       'name': 'GIAC GCIH',                     'meta': 'GCIH · 6 domains',      'config': 'giac/giac_gcih.json'},
    {'id': 'giac-gpen',               'vendor': 'giac',       'name': 'GIAC GPEN',                     'meta': 'GPEN · 6 domains',      'config': 'giac/giac_gpen.json'},
    {'id': 'giac-gcia',               'vendor': 'giac',       'name': 'GIAC GCIA',                     'meta': 'GCIA · 6 domains',      'config': 'giac/giac_gcia.json'},
    {'id': 'google-ace',              'vendor': 'google',     'name': 'Google Associate Cloud Engineer','meta': 'ACE · 5 domains',       'config': 'google/associate_cloud_engineer.json'},
    {'id': 'google-pca',              'vendor': 'google',     'name': 'Google Professional Cloud Architect','meta':'PCA · 6 domains',    'config': 'google/professional_cloud_architect.json'},
    {'id': 'google-cdl',              'vendor': 'google',     'name': 'Google Cloud Digital Leader',    'meta': 'CDL · 3 domains',       'config': 'google/cloud_digital_leader.json'},
    {'id': 'google-pde',              'vendor': 'google',     'name': 'Google Professional Data Engineer','meta':'PDE · 4 domains',      'config': 'google/professional_data_engineer.json'},
    {'id': 'google-pse',              'vendor': 'google',     'name': 'Google Cloud Security Engineer', 'meta': 'PSE · 6 domains',       'config': 'google/professional_security_engineer.json'},
    {'id': 'ec-ceh',                  'vendor': 'ec-council', 'name': 'EC-Council CEH v13',            'meta': 'CEH · 20 modules',      'config': 'ec-council/ceh_v13.json'},
    {'id': 'ec-chfi',                 'vendor': 'ec-council', 'name': 'EC-Council CHFI v11',           'meta': 'CHFI · 14 modules',     'config': 'ec-council/chfi_v11.json'},
    {'id': 'ec-cnd',                  'vendor': 'ec-council', 'name': 'EC-Council CND v3',             'meta': 'CND · 14 modules',      'config': 'ec-council/cnd_v3.json'},
    {'id': 'offsec-oscp',             'vendor': 'offsec',     'name': 'OffSec OSCP',                   'meta': 'PEN-200 · Practical',   'config': 'offsec/oscp_pen-200.json'},
    {'id': 'offsec-oswa',             'vendor': 'offsec',     'name': 'OffSec OSWA',                   'meta': 'WEB-200 · Practical',   'config': 'offsec/oswa_web-200.json'},
    {'id': 'offsec-oswe',             'vendor': 'offsec',     'name': 'OffSec OSWE',                   'meta': 'WEB-300 · Practical',   'config': 'offsec/oswe_web-300.json'},
    {'id': 'hashicorp-terraform',     'vendor': 'hashicorp',  'name': 'HashiCorp Terraform Associate', 'meta': 'TA-003 · 9 objectives', 'config': 'hashicorp/terraform_associate_003.json'},
    {'id': 'hashicorp-vault',         'vendor': 'hashicorp',  'name': 'HashiCorp Vault Associate',     'meta': 'VA-002 · 10 objectives','config': 'hashicorp/vault_associate_003.json'},
    {'id': 'k8s-cka',                 'vendor': 'k8s',        'name': 'Kubernetes CKA',                'meta': 'CKA · Performance-based','config': 'kubernetes/cka.json'},
    {'id': 'k8s-ckad',                'vendor': 'k8s',        'name': 'Kubernetes CKAD',               'meta': 'CKAD · Performance-based','config':'kubernetes/ckad.json'},
    {'id': 'k8s-cks',                 'vendor': 'k8s',        'name': 'Kubernetes CKS',                'meta': 'CKS · Performance-based','config': 'kubernetes/cks.json'},
]

# ── Quiz mapping ─────────────────────────────────────────────────────
QUIZ_MAP = {
    # CompTIA (13)
    'comptia-security-plus':   'security-quiz.html',
    'comptia-a-plus-1201':     'aplus-quiz.html',
    'comptia-a-plus-1202':     'aplus2-quiz.html',
    'comptia-network-plus':    'network-plus-quiz.html',
    'comptia-linux-plus':      'linux-plus-quiz.html',
    'comptia-cloud-plus':      'cloud-plus-quiz.html',
    'comptia-cysa-plus':       'cysa-plus-quiz.html',
    'comptia-pentest-plus':    'pentest-plus-quiz.html',
    'comptia-casp-plus':       'casp-plus-quiz.html',
    'comptia-server-plus':     'server-plus-quiz.html',
    'comptia-data-plus':       'data-plus-quiz.html',
    'comptia-project-plus':    'project-plus-quiz.html',
    'comptia-itf-plus':        'itf-plus-quiz.html',
    # ISC2 (4)
    'isc2-cc':                 'isc2-cc-quiz.html',
    'isc2-sscp':               'isc2-sscp-quiz.html',
    'isc2-cissp':              'cissp-quiz.html',
    'isc2-ccsp':               'isc2-ccsp-quiz.html',
    # AWS (8)
    'aws-cloud-practitioner':  'aws-clf-quiz.html',
    'aws-solutions-architect': 'aws-saa-quiz.html',
    'aws-developer':           'aws-dva-quiz.html',
    'aws-cloudops':            'aws-soa-quiz.html',
    'aws-security-specialty':  'aws-security-quiz.html',
    'aws-database-specialty':  'aws-dbs-quiz.html',
    'aws-machine-learning':    'aws-mls-quiz.html',
    'aws-data-engineer':       'aws-dea-quiz.html',
    # Microsoft (12)
    'ms-az-900':               'az900-quiz.html',
    'ms-az-104':               'az104-quiz.html',
    'ms-az-305':               'az305-quiz.html',
    'ms-sc-900':               'sc900-quiz.html',
    'ms-ai-900':               'ai900-quiz.html',
    'ms-az-500':               'az500-quiz.html',
    'ms-az-204':               'az204-quiz.html',
    'ms-az-400':               'az400-quiz.html',
    'ms-dp-900':               'dp900-quiz.html',
    'ms-ms-900':               'ms900-quiz.html',
    'ms-sc-300':               'sc300-quiz.html',
    'ms-ai-102':               'ai102-quiz.html',
    # Cisco (5)
    'cisco-ccna':              'ccna-quiz.html',
    'cisco-ccnp-encor':        'ccnp-quiz.html',
    'cisco-cyberops':          'cyberops-quiz.html',
    'cisco-ccnp-security':     'ccnp-security-quiz.html',
    'cisco-devnet':            'devnet-quiz.html',
    # ISACA (3)
    'isaca-cisa':              'cisa-quiz.html',
    'isaca-cism':              'cism-quiz.html',
    'isaca-crisc':             'crisc-quiz.html',
    # GIAC (4)
    'giac-gsec':               'gsec-quiz.html',
    'giac-gcih':               'gcih-quiz.html',
    'giac-gpen':               'gpen-quiz.html',
    'giac-gcia':               'gcia-quiz.html',
    # Google Cloud (5)
    'google-ace':              'gcp-ace-quiz.html',
    'google-pca':              'gcp-pca-quiz.html',
    'google-cdl':              'gcp-cdl-quiz.html',
    'google-pde':              'gcp-pde-quiz.html',
    'google-pse':              'gcp-pse-quiz.html',
    # EC-Council (3)
    'ec-ceh':                  'ceh-quiz.html',
    'ec-chfi':                 'chfi-quiz.html',
    'ec-cnd':                  'cnd-quiz.html',
    # OffSec (3)
    'offsec-oscp':             'oscp-quiz.html',
    'offsec-oswa':             'oswa-quiz.html',
    'offsec-oswe':             'oswe-quiz.html',
    # HashiCorp (2)
    'hashicorp-terraform':     'terraform-quiz.html',
    'hashicorp-vault':         'vault-quiz.html',
    # Kubernetes (3)
    'k8s-cka':                 'cka-quiz.html',
    'k8s-ckad':                'ckad-quiz.html',
    'k8s-cks':                 'cks-quiz.html',
}

VENDOR_NAMES = {
    'comptia': 'CompTIA', 'isc2': 'ISC2', 'aws': 'AWS', 'microsoft': 'Microsoft',
    'cisco': 'Cisco', 'isaca': 'ISACA', 'giac': 'GIAC', 'google': 'Google Cloud',
    'ec-council': 'EC-Council', 'offsec': 'OffSec', 'hashicorp': 'HashiCorp',
    'k8s': 'Kubernetes',
}

# Map vendor ID → store category page URL
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


def load_cert_config(config_path):
    """Load cert config JSON and extract domain data."""
    full_path = ETSY_CERTS / config_path
    if not full_path.exists():
        return None
    try:
        with open(full_path, encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def generate_heatmap_html(domains):
    """Generate a horizontal bar chart showing domain weight distribution."""
    if not domains:
        return ''
    # Color palette for bars (cycles if more than 6 domains)
    colors = ['#667eea', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6', '#06b6d4',
              '#ec4899', '#84cc16', '#f97316', '#6366f1']
    bars = ''
    for i, d in enumerate(domains):
        pct_label = d.get('percentage', '0%')
        pct_raw = pct_label.replace('%', '').strip().lstrip('~')
        try:
            if '-' in pct_raw:
                lo, hi = pct_raw.split('-', 1)
                pct = (float(lo) + float(hi)) / 2
            else:
                pct = float(pct_raw)
        except (ValueError, TypeError):
            pct = 0
        color = colors[i % len(colors)]
        name = d.get('name', f'Domain {d.get("number", i+1)}')
        bars += f'''
                <div class="heatmap-row">
                    <div class="heatmap-label">
                        <span class="heatmap-domain-num">D{d.get("number", i+1)}</span>
                        <span class="heatmap-domain-name">{name}</span>
                    </div>
                    <div class="heatmap-bar-track">
                        <div class="heatmap-bar" style="width: {pct}%; background: {color};">{pct_label}</div>
                    </div>
                </div>'''
    return f'''
            <div class="heatmap-container">
                <h3 class="heatmap-title">Where to Focus Your Study Time</h3>
                <p class="heatmap-subtitle">Domains with higher weight have more exam questions &mdash; allocate your study hours accordingly.</p>{bars}
            </div>'''


def generate_faq_schema(product):
    """Generate FAQ structured data for the cert page."""
    name = product['name']
    exam_code = product['meta'].split('·')[0].strip()
    faqs = [
        {
            'q': f'What is the {name} certification?',
            'a': f'The {name} ({exam_code}) is a professional IT certification that validates your knowledge and skills in the exam domains covered. It is recognized globally by employers and is a valuable credential for career advancement in cybersecurity and IT.'
        },
        {
            'q': f'What does the {name} certification syllabus cover?',
            'a': f'The {name} exam syllabus covers multiple weighted domains. Each domain is weighted differently, so focus your training on higher-weighted domains first. Review the complete domain breakdown for objectives and key concepts.'
        },
        {
            'q': f'How should I study for {name}?',
            'a': f'Create a structured study plan covering all exam domains, use practice tests to identify weak areas, and review key concepts regularly. A fillable study planner can help you organize your training with weekly schedules and progress tracking.'
        },
        {
            'q': f'How long does it take to prepare for {name}?',
            'a': f'Preparation time varies by experience level. Most candidates spend 8-12 weeks of dedicated training. Using a structured study planner with domain-by-domain breakdown helps ensure you cover all certification objectives efficiently.'
        },
    ]
    items = []
    for i, faq in enumerate(faqs):
        items.append(f'''    {{
      "@type": "Question",
      "name": "{escape(faq['q'])}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{escape(faq['a'])}"
      }}
    }}''')
    return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
''' + ',\n'.join(items) + '''
  ]
}
</script>'''


def generate_page(product):
    """Generate a full cert landing page HTML."""
    pid = product['id']
    name = product['name']
    vendor = VENDOR_NAMES.get(product['vendor'], product['vendor'])
    meta_parts = product['meta'].split('·')
    exam_code = meta_parts[0].strip()
    domain_info = meta_parts[1].strip() if len(meta_parts) > 1 else ''

    # Load cert config for domain details
    config = load_cert_config(product['config'])
    domains_html = ''
    heatmap_html = ''
    study_weeks = 12
    if config:
        domains = config.get('domains', [])
        study_weeks = config.get('planner_settings', {}).get('num_weeks', 12)
        for d in domains:
            objectives_html = ''.join(
                f'<li>{escape(obj)}</li>' for obj in d.get('objectives', [])
            )
            concepts = d.get('key_concepts', [])
            concepts_html = ''
            if concepts:
                concepts_html = '<div class="domain-concepts">' + ''.join(
                    f'<span class="concept-tag">{escape(c)}</span>' for c in concepts
                ) + '</div>'
            pct = d.get('percentage', '')
            domains_html += f'''
            <div class="domain-card">
                <div class="domain-header">
                    <span class="domain-number">Domain {d.get("number", "")}</span>
                    <span class="domain-weight">{pct}</span>
                </div>
                <h3 class="domain-name">{escape(d["name"])}</h3>
                <ul class="domain-objectives">{objectives_html}</ul>
                {concepts_html}
            </div>'''
        heatmap_html = generate_heatmap_html(domains)

    # Quiz link
    quiz_link = QUIZ_MAP.get(pid)
    quiz_section = ''
    if quiz_link:
        quiz_section = f'''
        <section class="cert-section">
            <h2>Practice Quiz</h2>
            <p>Test your knowledge before the exam with our free practice quiz.</p>
            <a href="/{quiz_link}" class="btn-primary">Take the {name} Practice Quiz</a>
        </section>'''

    # FAQ schema
    faq_schema = generate_faq_schema(product)

    store_page = VENDOR_STORE_PAGES.get(product['vendor'], '/store/store.html')

    # Related comparisons
    comparisons_html = ''
    comp_data_path = REPO / 'data' / 'cert-comparisons.json'
    if comp_data_path.exists():
        import json as _json
        comp_data = _json.loads(comp_data_path.read_text(encoding='utf-8'))
        # Map cert page IDs to comparison cert keys
        PAGE_TO_COMP_KEYS = {
            'comptia-security-plus': ['security-plus'], 'comptia-cysa-plus': ['cysa-plus'],
            'comptia-pentest-plus': ['pentest-plus'], 'comptia-network-plus': ['network-plus'],
            'comptia-a-plus-1201': ['a-plus'], 'comptia-a-plus-1202': ['a-plus'],
            'isc2-sscp': ['sscp'], 'isc2-cissp': ['cissp'], 'isc2-ccsp': ['ccsp'], 'isc2-cc': ['cc'],
            'isaca-cism': ['cism'], 'isaca-cisa': ['cisa'], 'isaca-crisc': ['crisc'],
            'aws-solutions-architect': ['aws-saa', 'aws-sap'], 'aws-security-specialty': ['aws-security-specialty'],
            'aws-cloud-practitioner': ['aws-ccp'],
            'ms-az-104': ['azure-az-104'], 'ms-az-500': ['azure-az-500'], 'ms-az-900': ['azure-az-900'],
            'cisco-ccna': ['ccna'], 'cisco-ccnp-encor': ['ccnp-encor'],
            'ec-ceh': ['ceh'], 'offsec-oscp': ['oscp'],
            'giac-gsec': ['gsec'], 'giac-gcih': ['gcih'], 'giac-gpen': ['gpen'],
            'comptia-casp-plus': ['casp-plus'], 'comptia-cloud-plus': ['cloud-plus'],
            'comptia-linux-plus': ['linux-plus'],
        }
        comp_keys = PAGE_TO_COMP_KEYS.get(pid, [])
        if comp_keys:
            related = []
            for c in comp_data.get('comparisons', []):
                if c['cert1'] in comp_keys or c['cert2'] in comp_keys:
                    related.append(c)
            if related:
                links = '\n                '.join(
                    f'<a href="/comparisons/{c["slug"]}.html" style="display:inline-block;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:6px;padding:0.5rem 1rem;text-decoration:none;color:var(--text-primary);font-size:0.9rem;">{escape(c["title"])}</a>'
                    for c in related
                )
                comparisons_html = f'''
        <section class="cert-section">
            <h2>Related Comparisons</h2>
            <p>Not sure if {name} is the right choice? Compare it with similar certifications:</p>
            <div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-top:0.75rem;">
                {links}
            </div>
        </section>'''

    # Cross-link sections
    roadmap_link = f'/roadmaps/{pid}.html'
    cross_links_html = f'''
        <section class="cert-section">
            <h2>Free Study Resources</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
                <a href="{roadmap_link}" style="display:block;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:1.25rem;text-decoration:none;color:inherit;transition:transform 0.2s;">
                    <span style="font-size:1.5rem;">📋</span>
                    <h4 style="margin:0.5rem 0 0.25rem;font-size:0.95rem;">Study Roadmap</h4>
                    <p style="font-size:0.8rem;color:var(--text-secondary);margin:0;">Week-by-week study plan with free resources</p>
                </a>
                <a href="/study-tracker.html" style="display:block;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:1.25rem;text-decoration:none;color:inherit;transition:transform 0.2s;">
                    <span style="font-size:1.5rem;">✅</span>
                    <h4 style="margin:0.5rem 0 0.25rem;font-size:0.95rem;">Study Tracker</h4>
                    <p style="font-size:0.8rem;color:var(--text-secondary);margin:0;">Track objective completion with progress dashboard</p>
                </a>
                <a href="/cert-cost-calculator.html" style="display:block;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:1.25rem;text-decoration:none;color:inherit;transition:transform 0.2s;">
                    <span style="font-size:1.5rem;">💰</span>
                    <h4 style="margin:0.5rem 0 0.25rem;font-size:0.95rem;">Cost Calculator</h4>
                    <p style="font-size:0.8rem;color:var(--text-secondary);margin:0;">Total cost breakdown and ROI analysis</p>
                </a>'''
    if quiz_link:
        cross_links_html += f'''
                <a href="/{quiz_link}" style="display:block;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:1.25rem;text-decoration:none;color:inherit;transition:transform 0.2s;">
                    <span style="font-size:1.5rem;">🧪</span>
                    <h4 style="margin:0.5rem 0 0.25rem;font-size:0.95rem;">Practice Quiz</h4>
                    <p style="font-size:0.8rem;color:var(--text-secondary);margin:0;">Test your knowledge with free practice questions</p>
                </a>'''
    cross_links_html += '''
            </div>
        </section>'''

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} Certification Study Guide & Exam Syllabus | FixTheVuln</title>
    <meta name="description" content="{name} ({exam_code}) certification study guide with complete exam syllabus, domain breakdown, training resources, and free practice quizzes. Study tips + fillable PDF planners.">
    <meta name="keywords" content="{name}, {exam_code}, {exam_code.replace('-', '').replace(' ', '')}, {name} certification, {name} exam, {name} syllabus, {name} domains, {name} training, cybersecurity certification">
    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <meta property="og:title" content="{name} Certification Study Guide | FixTheVuln">
    <meta property="og:description" content="Complete {name} certification exam syllabus with domain breakdown, training tips, and practice quizzes.">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://fixthevuln.com/certs/{pid}.html">
    <link rel="canonical" href="https://fixthevuln.com/certs/{pid}.html">
    <meta property="og:image" content="https://fixthevuln.com/og-image.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{name} Certification Study Guide | FixTheVuln">
    <meta name="twitter:description" content="Complete {name} certification exam syllabus with domain breakdown, training tips, and practice quizzes.">
    <meta name="twitter:image" content="https://fixthevuln.com/og-image.png">
    <link rel="stylesheet" href="/style.min.css?v=8">
    {faq_schema}
    <style>
        .cert-hero {{ text-align: center; padding: 3rem 1.5rem 2rem; }}
        .cert-hero h1 {{ font-size: 2.2rem; margin-bottom: 0.5rem; }}
        .cert-badge {{ display: inline-block; background: var(--accent-color); color: white; padding: 4px 14px; border-radius: 50px; font-size: 0.8rem; font-weight: 600; margin-bottom: 1rem; }}
        .cert-meta {{ color: var(--text-secondary); font-size: 1rem; }}
        .cert-section {{ max-width: 900px; margin: 0 auto 2rem; padding: 0 1.5rem; }}
        .cert-section h2 {{ font-size: 1.5rem; margin-bottom: 1rem; border-bottom: 2px solid var(--accent-color); padding-bottom: 0.5rem; }}
        .domain-card {{ background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 10px; padding: 1.5rem; margin-bottom: 1rem; }}
        .domain-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }}
        .domain-number {{ font-size: 0.8rem; font-weight: 700; color: var(--accent-color); text-transform: uppercase; letter-spacing: 1px; }}
        .domain-weight {{ background: var(--accent-color); color: white; padding: 2px 10px; border-radius: 50px; font-size: 0.8rem; font-weight: 700; }}
        .domain-name {{ font-size: 1.1rem; margin-bottom: 0.75rem; }}
        .domain-objectives {{ padding-left: 1.5rem; margin-bottom: 0.75rem; }}
        .domain-objectives li {{ font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.3rem; line-height: 1.5; }}
        .domain-concepts {{ display: flex; flex-wrap: wrap; gap: 6px; }}
        .concept-tag {{ background: var(--bg-tertiary, var(--bg-secondary)); border: 1px solid var(--border-color); border-radius: 50px; padding: 2px 10px; font-size: 0.75rem; color: var(--text-secondary); }}
        .study-tips {{ list-style: none; padding: 0; }}
        .study-tips li {{ padding: 0.75rem 1rem; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 8px; margin-bottom: 0.5rem; font-size: 0.95rem; line-height: 1.5; }}
        .study-tips li::before {{ content: "\\2713 "; color: var(--accent-color); font-weight: 700; margin-right: 0.5rem; }}
        .btn-primary {{ display: inline-block; background: var(--accent-color); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; transition: transform 0.2s; }}
        .btn-primary:hover {{ transform: translateY(-2px); }}
        .planner-cta-card {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 2rem; border-radius: 12px; color: white; text-align: center; margin-top: 2rem; }}
        .planner-cta-card h3 {{ color: white; margin-bottom: 0.5rem; font-size: 1.3rem; }}
        .planner-cta-card p {{ opacity: 0.9; margin-bottom: 1rem; }}
        .planner-cta-card .btn-cta {{ display: inline-block; background: #667eea; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; }}
        .cyberfolio-cta {{ border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 12px; text-align: center; margin-top: 1.5rem; }}
        .cyberfolio-cta p {{ color: var(--text-secondary); margin-bottom: 1rem; }}
        .cyberfolio-cta .btn-cyberfolio {{ display: inline-block; background: #06b6d4; color: white; padding: 10px 22px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.95rem; }}
        .cyberfolio-cta .btn-cyberfolio:hover {{ opacity: 0.9; }}
        .faq-item {{ background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 8px; margin-bottom: 0.5rem; overflow: hidden; }}
        .faq-item summary {{ padding: 1rem 1.25rem; font-weight: 600; cursor: pointer; list-style: none; }}
        .faq-item summary::-webkit-details-marker {{ display: none; }}
        .faq-item p {{ padding: 0 1.25rem 1rem; color: var(--text-secondary); line-height: 1.6; }}
        .heatmap-container {{ background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem; margin-top: 1.5rem; }}
        .heatmap-title {{ font-size: 1.1rem; margin-bottom: 0.25rem; }}
        .heatmap-subtitle {{ font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.25rem; line-height: 1.4; }}
        .heatmap-row {{ display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.6rem; }}
        .heatmap-label {{ min-width: 140px; display: flex; align-items: center; gap: 0.5rem; flex-shrink: 0; }}
        .heatmap-domain-num {{ font-size: 0.7rem; font-weight: 700; color: var(--accent-color); text-transform: uppercase; letter-spacing: 1px; white-space: nowrap; }}
        .heatmap-domain-name {{ font-size: 0.8rem; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .heatmap-bar-track {{ flex: 1; background: var(--bg-tertiary, rgba(128,128,128,0.15)); border-radius: 6px; height: 28px; overflow: hidden; }}
        .heatmap-bar {{ height: 100%; border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 0.75rem; font-weight: 700; color: white; min-width: 38px; transition: width 0.6s ease; }}
        @media (max-width: 600px) {{
            .heatmap-row {{ flex-direction: column; align-items: flex-start; gap: 0.25rem; }}
            .heatmap-label {{ min-width: unset; }}
        }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container nav-container">
            <a href="/" class="logo">FixTheVuln</a>
            <button class="nav-toggle" aria-label="Menu" onclick="this.classList.toggle('active');this.parentElement.querySelector('.nav-links').classList.toggle('open')"><span></span><span></span><span></span></button>
            <div class="nav-links">
                <a href="/guides.html">Guides</a>
                <a href="/tools.html">Tools</a>
                <a href="/practice-tests.html">Quizzes</a>
                <a href="/store/store.html">Store</a>
            </div>
            <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">
                <span class="theme-icon">&#9790;</span>
            </button>
        </div>
    </nav>

    <main class="container">
        <a href="/career-paths.html" class="back-link">&larr; All Certifications</a>

        <section class="cert-hero">
            <span class="cert-badge">{vendor}</span>
            <h1>{name} Certification</h1>
            <p class="cert-meta">{exam_code} &middot; {domain_info}</p>
            <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.5rem;">Last updated: {datetime.now().strftime('%B %-d, %Y')}</p>
        </section>

        <section class="cert-section">
            <h2>Exam Syllabus & Domains</h2>
            <p>The {name} certification exam covers the following domains. Focus your training time proportionally to each domain's weight.</p>
            {domains_html if domains_html else f'<p>Domain details for {name} are available in the official exam guide.</p>'}
            {heatmap_html}
        </section>

        <section class="cert-section">
            <h2>Study Tips</h2>
            <ul class="study-tips">
                <li>Create a {study_weeks}-week study schedule and assign specific domains to each week</li>
                <li>Focus more time on higher-weighted domains — they have more exam questions</li>
                <li>Use practice quizzes to identify weak areas early, then revisit those domains</li>
                <li>Study in focused 25-minute blocks (Pomodoro technique) with 5-minute breaks</li>
                <li>Create flashcards for key terms, acronyms, and port numbers</li>
                <li>Review domain objectives weekly to track your progress and adjust your plan</li>
            </ul>
        </section>
{cross_links_html}
{quiz_section}
{comparisons_html}
        <section class="cert-section">
            <div class="planner-cta-card">
                <h3>Get the {name} Study Planner</h3>
                <p>Fillable PDF with {study_weeks}-week schedule, domain trackers, flashcard templates, progress tracking, and quick reference sheets. Available in Standard, ADHD-Friendly, Dark Mode, and 4-Format Bundle.</p>
                <a href="{store_page}" class="btn-cta">Get the Study Planner &mdash; $5.99</a>
                <p style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.75rem;">Also available as a 4-Format Bundle for $15.99</p>
            </div>
        </section>

        <div class="cyberfolio-cta">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.5; margin-bottom: 0.3rem;">CyberFolio</p>
            <p style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">Earned your certs? Show employers.</p>
            <p>Build a shareable cybersecurity portfolio that highlights your certifications, projects, and skills &mdash; free.</p>
            <a href="https://cyberfolio.io" class="btn-cyberfolio" target="_blank" rel="noopener">Build Your Portfolio &rarr;</a>
        </div>

        <section class="cert-section">
            <h2>Free Training Resources</h2>
            <p>Use these free tools to support your {name} certification training:</p>
            <ul class="study-tips">
                <li><a href="/practice-tests.html">Cybersecurity Practice Tests</a> &mdash; 3,150+ free questions across 66 certifications</li>
                <li><a href="/roadmaps/{pid}.html">Study Roadmap</a> &mdash; Structured learning path for {name}</li>
                <li><a href="/study-tracker.html">Study Progress Tracker</a> &mdash; Track hours and domain coverage</li>
                <li><a href="/cvss-calculator.html">CVSS Calculator</a> &mdash; Practice scoring vulnerabilities</li>
            </ul>
        </section>

        <section class="cert-section">
            <h2>Frequently Asked Questions</h2>
            <details class="faq-item">
                <summary>What is the {name} certification?</summary>
                <p>The {name} ({exam_code}) is a professional IT certification that validates your knowledge and skills in the exam domains covered. It is recognized globally by employers and is a valuable credential for career advancement in cybersecurity and IT.</p>
            </details>
            <details class="faq-item">
                <summary>What does the {name} certification syllabus cover?</summary>
                <p>The {name} exam syllabus covers {domain_info}. Each domain is weighted differently, so focus your training on higher-weighted domains first. Review the complete domain breakdown above for objectives and key concepts.</p>
            </details>
            <details class="faq-item">
                <summary>How should I study for {name}?</summary>
                <p>Create a structured study plan covering all exam domains, use practice tests to identify weak areas, and review key concepts regularly. A fillable study planner can help you organize your training with weekly schedules and progress tracking.</p>
            </details>
            <details class="faq-item">
                <summary>How long does it take to prepare for {name}?</summary>
                <p>Preparation time varies by experience level. Most candidates spend 8-12 weeks of dedicated training. Using a structured study planner with domain-by-domain breakdown helps ensure you cover all certification objectives efficiently.</p>
            </details>
        </section>
    </main>

    <!-- Social Share Bar -->
    <div class="share-bar">
        <a class="share-linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url=" onclick="this.href+=encodeURIComponent(window.location.href)" target="_blank" rel="noopener" title="Share on LinkedIn">
            <svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
        </a>
        <a class="share-twitter" href="https://twitter.com/intent/tweet?url=" onclick="this.href='https://twitter.com/intent/tweet?url='+encodeURIComponent(window.location.href)+'&text='+encodeURIComponent(document.title)" target="_blank" rel="noopener" title="Share on X/Twitter">
            <svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
        </a>
        <a class="share-reddit" href="https://reddit.com/submit?url=" onclick="this.href='https://reddit.com/submit?url='+encodeURIComponent(window.location.href)+'&title='+encodeURIComponent(document.title)" target="_blank" rel="noopener" title="Share on Reddit">
            <svg viewBox="0 0 24 24"><path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 0-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z"/></svg>
        </a>
        <a class="share-copy" href="javascript:void(0)" onclick="navigator.clipboard.writeText(window.location.href).then(()=>{{this.title='Copied!';setTimeout(()=>this.title='Copy link',2000)}})" title="Copy link">
            <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
        </a>
    </div>

    <footer>
        <div class="container">
            <p>&copy; 2026 FixTheVuln. Practical Vulnerability Remediation.</p>
            <p>Study Planners: <a href="/store/store.html">FixTheVuln Store</a> | Career Tools: <a href="https://cyberfolio.io" target="_blank" rel="noopener">CyberFolio</a></p>
        </div>
    </footer>

    <script>
        const toggle = document.getElementById('themeToggle');
        const saved = localStorage.getItem('theme');
        if (saved === 'light') document.documentElement.setAttribute('data-theme', 'light');
        toggle.addEventListener('click', () => {{
            const isLight = document.documentElement.getAttribute('data-theme') === 'light';
            document.documentElement.setAttribute('data-theme', isLight ? '' : 'light');
            localStorage.setItem('theme', isLight ? 'dark' : 'light');
        }});
    </script>
<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "8304415b01684a00adedcbf6975458d7"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>'''
    return page


def main():
    CERTS_DIR.mkdir(exist_ok=True)
    generated = 0
    skipped = 0
    no_config = 0

    for product in PRODUCTS:
        pid = product['id']
        filepath = CERTS_DIR / f'{pid}.html'

        config = load_cert_config(product['config'])
        if not config:
            print(f"  NOCONFIG {pid} — generating with minimal info")
            no_config += 1

        page_html = generate_page(product)
        filepath.write_text(page_html, encoding='utf-8')
        has_quiz = '+ quiz' if pid in QUIZ_MAP else ''
        print(f"  OK   certs/{pid}.html {has_quiz}")
        generated += 1

    print(f"\nDone: {generated} pages generated ({no_config} without cert config)")
    print(f"Output: {CERTS_DIR}/")


if __name__ == '__main__':
    main()
