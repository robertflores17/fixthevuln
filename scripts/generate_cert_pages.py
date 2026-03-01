#!/usr/bin/env python3
"""Generate SEO landing pages for all certifications in the store catalog.
Each page targets "[cert name] study guide" search queries and funnels
visitors to quizzes and planner purchases."""

import json
import re
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
    {'id': 'isc2-cissp',              'vendor': 'isc2',       'name': 'ISC2 CISSP',                   'meta': 'CISSP 2026 · 8 domains','config': 'isc2/cissp.json'},
    {'id': 'isc2-ccsp',               'vendor': 'isc2',       'name': 'ISC2 CCSP',                    'meta': 'CCSP · 6 domains',      'config': 'isc2/ccsp.json'},
    {'id': 'aws-cloud-practitioner',  'vendor': 'aws',        'name': 'AWS Cloud Practitioner',       'meta': 'CLF-C02 · 4 domains',   'config': 'aws/cloud_practitioner_c02.json'},
    {'id': 'aws-solutions-architect', 'vendor': 'aws',        'name': 'AWS Solutions Architect',       'meta': 'SAA-C03 · 4 domains',   'config': 'aws/solutions_architect_c03.json'},
    {'id': 'aws-developer',           'vendor': 'aws',        'name': 'AWS Developer Associate',       'meta': 'DVA-C02 · 4 domains',   'config': 'aws/developer_c02.json'},
    {'id': 'aws-cloudops',            'vendor': 'aws',        'name': 'AWS CloudOps Engineer',         'meta': 'SOA-C03 · 6 domains',   'config': 'aws/sysops_c03.json'},
    {'id': 'aws-security-specialty',  'vendor': 'aws',        'name': 'AWS Security Specialty',        'meta': 'SCS-C03 · 6 domains',   'config': 'aws/security_specialty_c03.json'},
    {'id': 'aws-database-specialty',  'vendor': 'aws',        'name': 'AWS Database Specialty',        'meta': 'DBS-C01 · 5 domains',   'config': 'aws/database_specialty_c01.json'},
    {'id': 'aws-machine-learning',    'vendor': 'aws',        'name': 'AWS Machine Learning',          'meta': 'MLS-C01 · 4 domains',   'config': 'aws/machine_learning_c01.json'},
    {'id': 'aws-data-engineer',       'vendor': 'aws',        'name': 'AWS Data Engineer',             'meta': 'DEA-C01 · 4 domains',   'config': 'aws/data_engineer_c01.json'},
    {'id': 'ms-az-900',               'vendor': 'microsoft',  'name': 'Microsoft Azure Fundamentals',  'meta': 'AZ-900 · 3 domains',    'config': 'microsoft/az_900.json'},
    {'id': 'ms-az-104',               'vendor': 'microsoft',  'name': 'Microsoft Azure Administrator', 'meta': 'AZ-104 · 5 domains',    'config': 'microsoft/az_104.json'},
    {'id': 'ms-az-305',               'vendor': 'microsoft',  'name': 'Azure Solutions Architect',     'meta': 'AZ-305 · 4 domains',    'config': 'microsoft/az_305.json'},
    {'id': 'ms-sc-900',               'vendor': 'microsoft',  'name': 'Security Fundamentals',         'meta': 'SC-900 · 4 domains',    'config': 'microsoft/sc_900.json'},
    {'id': 'ms-ai-900',               'vendor': 'microsoft',  'name': 'Azure AI Fundamentals',         'meta': 'AI-900 · 5 domains',    'config': 'microsoft/ai_900.json'},
    {'id': 'ms-az-500',               'vendor': 'microsoft',  'name': 'Azure Security Engineer',       'meta': 'AZ-500 · 4 domains',    'config': 'microsoft/az_500.json'},
    {'id': 'ms-az-204',               'vendor': 'microsoft',  'name': 'Azure Developer Associate',     'meta': 'AZ-204 · 5 domains',    'config': 'microsoft/az_204.json'},
    {'id': 'ms-az-400',               'vendor': 'microsoft',  'name': 'Azure DevOps Engineer',         'meta': 'AZ-400 · 8 domains',    'config': 'microsoft/az_400.json'},
    {'id': 'ms-dp-900',               'vendor': 'microsoft',  'name': 'Azure Data Fundamentals',       'meta': 'DP-900 · 3 domains',    'config': 'microsoft/dp_900.json'},
    {'id': 'ms-ms-900',               'vendor': 'microsoft',  'name': 'Microsoft 365 Fundamentals',    'meta': 'MS-900 · 4 domains',    'config': 'microsoft/ms_900.json'},
    {'id': 'ms-sc-300',               'vendor': 'microsoft',  'name': 'Identity & Access Admin',       'meta': 'SC-300 · 4 domains',    'config': 'microsoft/sc_300.json'},
    {'id': 'ms-ai-102',               'vendor': 'microsoft',  'name': 'Azure AI Engineer',             'meta': 'AI-102 · 5 domains',    'config': 'microsoft/ai_102.json'},
    {'id': 'cisco-ccna',              'vendor': 'cisco',      'name': 'Cisco CCNA',                    'meta': '200-301 · 6 domains',   'config': 'cisco/ccna_200_301.json'},
    {'id': 'cisco-ccnp-encor',        'vendor': 'cisco',      'name': 'Cisco CCNP ENCOR',              'meta': '350-401 · 6 domains',   'config': 'cisco/ccnp_encor_350_401.json'},
    {'id': 'cisco-cyberops',          'vendor': 'cisco',      'name': 'Cisco CyberOps Associate',      'meta': '200-201 · 5 domains',   'config': 'cisco/cyberops_200_201.json'},
    {'id': 'cisco-ccnp-security',     'vendor': 'cisco',      'name': 'Cisco CCNP Security SCOR',      'meta': '350-701 · 5 domains',   'config': 'cisco/ccnp_security_350_701.json'},
    {'id': 'cisco-devnet',            'vendor': 'cisco',      'name': 'Cisco DevNet Associate',         'meta': '200-901 · 6 domains',   'config': 'cisco/devnet_200_901.json'},
    {'id': 'isaca-cisa',              'vendor': 'isaca',      'name': 'ISACA CISA',                    'meta': 'CISA · 5 domains',      'config': 'isaca/cisa.json'},
    {'id': 'isaca-cism',              'vendor': 'isaca',      'name': 'ISACA CISM',                    'meta': 'CISM 2026 · 4 domains', 'config': 'isaca/cism.json'},
    {'id': 'isaca-crisc',             'vendor': 'isaca',      'name': 'ISACA CRISC',                   'meta': 'CRISC · 4 domains',     'config': 'isaca/crisc.json'},
    {'id': 'giac-gsec',               'vendor': 'giac',       'name': 'GIAC GSEC',                     'meta': 'GSEC · 7 domains',      'config': 'giac/gsec.json'},
    {'id': 'giac-gcih',               'vendor': 'giac',       'name': 'GIAC GCIH',                     'meta': 'GCIH · 6 domains',      'config': 'giac/gcih.json'},
    {'id': 'giac-gpen',               'vendor': 'giac',       'name': 'GIAC GPEN',                     'meta': 'GPEN · 6 domains',      'config': 'giac/gpen.json'},
    {'id': 'giac-gcia',               'vendor': 'giac',       'name': 'GIAC GCIA',                     'meta': 'GCIA · 6 domains',      'config': 'giac/gcia.json'},
    {'id': 'google-ace',              'vendor': 'google',     'name': 'Google Associate Cloud Engineer','meta': 'ACE · 5 domains',       'config': 'google/ace.json'},
    {'id': 'google-pca',              'vendor': 'google',     'name': 'Google Professional Cloud Architect','meta':'PCA · 6 domains',    'config': 'google/pca.json'},
    {'id': 'google-cdl',              'vendor': 'google',     'name': 'Google Cloud Digital Leader',    'meta': 'CDL · 3 domains',       'config': 'google/cdl.json'},
    {'id': 'google-pde',              'vendor': 'google',     'name': 'Google Professional Data Engineer','meta':'PDE · 4 domains',      'config': 'google/pde.json'},
    {'id': 'google-pse',              'vendor': 'google',     'name': 'Google Cloud Security Engineer', 'meta': 'PSE · 6 domains',       'config': 'google/pse.json'},
    {'id': 'ec-ceh',                  'vendor': 'ec-council', 'name': 'EC-Council CEH v13',            'meta': 'CEH · 20 modules',      'config': 'ec-council/ceh_v13.json'},
    {'id': 'ec-chfi',                 'vendor': 'ec-council', 'name': 'EC-Council CHFI v11',           'meta': 'CHFI · 14 modules',     'config': 'ec-council/chfi_v11.json'},
    {'id': 'ec-cnd',                  'vendor': 'ec-council', 'name': 'EC-Council CND v3',             'meta': 'CND · 14 modules',      'config': 'ec-council/cnd_v3.json'},
    {'id': 'offsec-oscp',             'vendor': 'offsec',     'name': 'OffSec OSCP',                   'meta': 'PEN-200 · Practical',   'config': 'offsec/oscp.json'},
    {'id': 'offsec-oswa',             'vendor': 'offsec',     'name': 'OffSec OSWA',                   'meta': 'WEB-200 · Practical',   'config': 'offsec/oswa.json'},
    {'id': 'offsec-oswe',             'vendor': 'offsec',     'name': 'OffSec OSWE',                   'meta': 'WEB-300 · Practical',   'config': 'offsec/oswe.json'},
    {'id': 'hashicorp-terraform',     'vendor': 'hashicorp',  'name': 'HashiCorp Terraform Associate', 'meta': 'TA-003 · 9 objectives', 'config': 'hashicorp/terraform_003.json'},
    {'id': 'hashicorp-vault',         'vendor': 'hashicorp',  'name': 'HashiCorp Vault Associate',     'meta': 'VA-002 · 10 objectives','config': 'hashicorp/vault_002.json'},
    {'id': 'k8s-cka',                 'vendor': 'k8s',        'name': 'Kubernetes CKA',                'meta': 'CKA · Performance-based','config': 'kubernetes/cka.json'},
    {'id': 'k8s-ckad',                'vendor': 'k8s',        'name': 'Kubernetes CKAD',               'meta': 'CKAD · Performance-based','config':'kubernetes/ckad.json'},
    {'id': 'k8s-cks',                 'vendor': 'k8s',        'name': 'Kubernetes CKS',                'meta': 'CKS · Performance-based','config': 'kubernetes/cks.json'},
]

# ── Quiz mapping ─────────────────────────────────────────────────────
QUIZ_MAP = {
    'comptia-security-plus':   'security-quiz.html',
    'comptia-a-plus-1201':     'aplus-quiz.html',
    'comptia-network-plus':    'network-plus-quiz.html',
    'comptia-linux-plus':      'linux-plus-quiz.html',
    'comptia-cysa-plus':       'cysa-plus-quiz.html',
    'comptia-pentest-plus':    'pentest-plus-quiz.html',
    'comptia-casp-plus':       'casp-plus-quiz.html',
    'isc2-cissp':              'cissp-quiz.html',
    'cisco-ccna':              'ccna-quiz.html',
    'cisco-ccnp-encor':        'ccnp-quiz.html',
    'ec-ceh':                  'ceh-quiz.html',
    'isaca-cism':              'cism-quiz.html',
    'offsec-oscp':             'oscp-quiz.html',
    'aws-cloud-practitioner':  'aws-clf-quiz.html',
    'aws-solutions-architect': 'aws-saa-quiz.html',
    'aws-security-specialty':  'aws-security-quiz.html',
    'ms-az-900':               'az900-quiz.html',
    'ms-sc-900':               'sc900-quiz.html',
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


def generate_faq_schema(product):
    """Generate FAQ structured data for the cert page."""
    name = product['name']
    exam_code = product['meta'].split('·')[0].strip()
    faqs = [
        {
            'q': f'What is the {name} certification?',
            'a': f'The {name} ({exam_code}) is a professional IT certification that validates your knowledge and skills in the exam domains covered. It is recognized globally by employers and is a valuable credential for career advancement.'
        },
        {
            'q': f'How should I study for {name}?',
            'a': f'Create a structured study plan covering all exam domains, use practice tests to identify weak areas, and review key concepts regularly. A fillable study planner can help you organize your preparation with weekly schedules and progress tracking.'
        },
        {
            'q': f'How long does it take to prepare for {name}?',
            'a': f'Preparation time varies by experience level. Most candidates spend 8-12 weeks of dedicated study. Using a structured study planner with domain-by-domain breakdown helps ensure you cover all objectives efficiently.'
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

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} Study Guide & Exam Objectives | FixTheVuln</title>
    <meta name="description" content="{name} ({exam_code}) study guide with complete exam objectives, domain breakdown, study tips, and practice quizzes. Free resources + fillable PDF study planners.">
    <link rel="icon" href="/favicon.ico" sizes="any">
    <meta property="og:title" content="{name} Study Guide | FixTheVuln">
    <meta property="og:description" content="Complete {name} exam guide with domain breakdown, study tips, and practice quizzes.">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://fixthevuln.com/certs/{pid}.html">
    <link rel="canonical" href="https://fixthevuln.com/certs/{pid}.html">
    <meta property="og:image" content="https://fixthevuln.com/og-image.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{name} Study Guide | FixTheVuln">
    <meta name="twitter:description" content="Complete {name} exam guide with domain breakdown, study tips, and practice quizzes.">
    <link rel="stylesheet" href="/style.min.css">
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
        .faq-item {{ background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 8px; margin-bottom: 0.5rem; overflow: hidden; }}
        .faq-item summary {{ padding: 1rem 1.25rem; font-weight: 600; cursor: pointer; list-style: none; }}
        .faq-item summary::-webkit-details-marker {{ display: none; }}
        .faq-item p {{ padding: 0 1.25rem 1rem; color: var(--text-secondary); line-height: 1.6; }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container nav-container">
            <a href="/" class="logo">FixTheVuln</a>
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
            <h1>{name}</h1>
            <p class="cert-meta">{exam_code} &middot; {domain_info}</p>
        </section>

        <section class="cert-section">
            <h2>Exam Domains</h2>
            <p>The {name} exam covers the following domains. Focus your study time proportionally to each domain's weight.</p>
            {domains_html if domains_html else f'<p>Domain details for {name} are available in the official exam guide.</p>'}
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
{quiz_section}
        <section class="cert-section">
            <div class="planner-cta-card">
                <h3>Get the {name} Study Planner</h3>
                <p>Fillable PDF with {study_weeks}-week schedule, domain trackers, flashcard templates, progress tracking, and quick reference sheets. Available in Standard, ADHD-Friendly, Dark Mode, and 4-Format Bundle.</p>
                <a href="{store_page}" class="btn-cta">Get the Study Planner &mdash; $5.99</a>
                <p style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.75rem;">Also available as a 4-Format Bundle for $15.99</p>
            </div>
        </section>

        <section class="cert-section">
            <h2>Frequently Asked Questions</h2>
            <details class="faq-item">
                <summary>What is the {name} certification?</summary>
                <p>The {name} ({exam_code}) is a professional IT certification that validates your knowledge and skills in the exam domains covered. It is recognized globally by employers and is a valuable credential for career advancement.</p>
            </details>
            <details class="faq-item">
                <summary>How should I study for {name}?</summary>
                <p>Create a structured study plan covering all exam domains, use practice tests to identify weak areas, and review key concepts regularly. A fillable study planner can help you organize your preparation with weekly schedules and progress tracking.</p>
            </details>
            <details class="faq-item">
                <summary>How long does it take to prepare for {name}?</summary>
                <p>Preparation time varies by experience level. Most candidates spend 8-12 weeks of dedicated study. Using a structured study planner with domain-by-domain breakdown helps ensure you cover all objectives efficiently.</p>
            </details>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 FixTheVuln. Practical Vulnerability Remediation.</p>
            <p>For detailed guides: <a href="https://fixthevuln.com">FixTheVuln.com</a></p>
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
