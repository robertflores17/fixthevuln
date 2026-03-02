#!/usr/bin/env python3
"""Generate per-cert study roadmap pages and hub page.
Each roadmap has a week-by-week study timeline, domain heatmap,
free resource links, and cross-links to quizzes/store/tracker."""

import json
from datetime import datetime
from pathlib import Path
from html import escape

REPO = Path(__file__).resolve().parent.parent
ETSY_CERTS = Path(__file__).resolve().parent.parent.parent / 'Dropshipping' / 'Etsy-Claude' / 'certifications'
ROADMAPS_DIR = REPO / 'roadmaps'

TODAY = datetime.now().strftime('%B %-d, %Y')
TODAY_ISO = datetime.now().strftime('%Y-%m-%d')

# ── Product catalog ──────────────────────────────────────────────────
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
    {'id': 'isc2-cc',                 'vendor': 'isc2',       'name': 'ISC2 CC',                      'config': 'isc2/cc.json'},
    {'id': 'isc2-sscp',               'vendor': 'isc2',       'name': 'ISC2 SSCP',                    'config': 'isc2/sscp.json'},
    {'id': 'isc2-cissp',              'vendor': 'isc2',       'name': 'ISC2 CISSP',                   'config': 'isc2/cissp_2026.json'},
    {'id': 'isc2-ccsp',               'vendor': 'isc2',       'name': 'ISC2 CCSP',                    'config': 'isc2/ccsp.json'},
    {'id': 'aws-cloud-practitioner',  'vendor': 'aws',        'name': 'AWS Cloud Practitioner',       'config': 'aws/aws_cloud_practitioner_clf-c02.json'},
    {'id': 'aws-solutions-architect', 'vendor': 'aws',        'name': 'AWS Solutions Architect',       'config': 'aws/aws_solutions_architect_saa-c03.json'},
    {'id': 'aws-developer',           'vendor': 'aws',        'name': 'AWS Developer Associate',       'config': 'aws/developer_dva-c02.json'},
    {'id': 'aws-cloudops',            'vendor': 'aws',        'name': 'AWS CloudOps Engineer',         'config': 'aws/cloudops_engineer_soa-c03.json'},
    {'id': 'aws-security-specialty',  'vendor': 'aws',        'name': 'AWS Security Specialty',        'config': 'aws/security_specialty_scs-c03.json'},
    {'id': 'aws-database-specialty',  'vendor': 'aws',        'name': 'AWS Database Specialty',        'config': 'aws/database_specialty_dbs-c01.json'},
    {'id': 'aws-machine-learning',    'vendor': 'aws',        'name': 'AWS Machine Learning',          'config': 'aws/machine_learning_mls-c01.json'},
    {'id': 'aws-data-engineer',       'vendor': 'aws',        'name': 'AWS Data Engineer',             'config': 'aws/data_engineer_dea-c01.json'},
    {'id': 'ms-az-900',               'vendor': 'microsoft',  'name': 'Microsoft Azure Fundamentals',  'config': 'microsoft/az-900.json'},
    {'id': 'ms-az-104',               'vendor': 'microsoft',  'name': 'Microsoft Azure Administrator', 'config': 'microsoft/az-104.json'},
    {'id': 'ms-az-305',               'vendor': 'microsoft',  'name': 'Azure Solutions Architect',     'config': 'microsoft/az-305.json'},
    {'id': 'ms-sc-900',               'vendor': 'microsoft',  'name': 'Security Fundamentals',         'config': 'microsoft/sc-900.json'},
    {'id': 'ms-ai-900',               'vendor': 'microsoft',  'name': 'Azure AI Fundamentals',         'config': 'microsoft/ai-900.json'},
    {'id': 'ms-az-500',               'vendor': 'microsoft',  'name': 'Azure Security Engineer',       'config': 'microsoft/az-500.json'},
    {'id': 'ms-az-204',               'vendor': 'microsoft',  'name': 'Azure Developer Associate',     'config': 'microsoft/az-204.json'},
    {'id': 'ms-az-400',               'vendor': 'microsoft',  'name': 'Azure DevOps Engineer',         'config': 'microsoft/az-400.json'},
    {'id': 'ms-dp-900',               'vendor': 'microsoft',  'name': 'Azure Data Fundamentals',       'config': 'microsoft/dp-900.json'},
    {'id': 'ms-ms-900',               'vendor': 'microsoft',  'name': 'Microsoft 365 Fundamentals',    'config': 'microsoft/ms-900.json'},
    {'id': 'ms-sc-300',               'vendor': 'microsoft',  'name': 'Identity & Access Admin',       'config': 'microsoft/sc-300.json'},
    {'id': 'ms-ai-102',               'vendor': 'microsoft',  'name': 'Azure AI Engineer',             'config': 'microsoft/ai-102.json'},
    {'id': 'cisco-ccna',              'vendor': 'cisco',      'name': 'Cisco CCNA',                    'config': 'cisco/ccna_200-301.json'},
    {'id': 'cisco-ccnp-encor',        'vendor': 'cisco',      'name': 'Cisco CCNP ENCOR',              'config': 'cisco/ccnp_enterprise_encor.json'},
    {'id': 'cisco-cyberops',          'vendor': 'cisco',      'name': 'Cisco CyberOps Associate',      'config': 'cisco/cyberops_200-201.json'},
    {'id': 'cisco-ccnp-security',     'vendor': 'cisco',      'name': 'Cisco CCNP Security SCOR',      'config': 'cisco/ccnp_security_scor_350-701.json'},
    {'id': 'cisco-devnet',            'vendor': 'cisco',      'name': 'Cisco DevNet Associate',         'config': 'cisco/devnet_associate_200-901.json'},
    {'id': 'isaca-cisa',              'vendor': 'isaca',      'name': 'ISACA CISA',                    'config': 'isaca/cisa.json'},
    {'id': 'isaca-cism',              'vendor': 'isaca',      'name': 'ISACA CISM',                    'config': 'isaca/cism_2026.json'},
    {'id': 'isaca-crisc',             'vendor': 'isaca',      'name': 'ISACA CRISC',                   'config': 'isaca/crisc.json'},
    {'id': 'giac-gsec',               'vendor': 'giac',       'name': 'GIAC GSEC',                     'config': 'giac/giac_gsec.json'},
    {'id': 'giac-gcih',               'vendor': 'giac',       'name': 'GIAC GCIH',                     'config': 'giac/giac_gcih.json'},
    {'id': 'giac-gpen',               'vendor': 'giac',       'name': 'GIAC GPEN',                     'config': 'giac/giac_gpen.json'},
    {'id': 'giac-gcia',               'vendor': 'giac',       'name': 'GIAC GCIA',                     'config': 'giac/giac_gcia.json'},
    {'id': 'google-ace',              'vendor': 'google',     'name': 'Google Associate Cloud Engineer','config': 'google/associate_cloud_engineer.json'},
    {'id': 'google-pca',              'vendor': 'google',     'name': 'Google Professional Cloud Architect','config': 'google/professional_cloud_architect.json'},
    {'id': 'google-cdl',              'vendor': 'google',     'name': 'Google Cloud Digital Leader',    'config': 'google/cloud_digital_leader.json'},
    {'id': 'google-pde',              'vendor': 'google',     'name': 'Google Professional Data Engineer','config': 'google/professional_data_engineer.json'},
    {'id': 'google-pse',              'vendor': 'google',     'name': 'Google Cloud Security Engineer', 'config': 'google/professional_security_engineer.json'},
    {'id': 'ec-ceh',                  'vendor': 'ec-council', 'name': 'EC-Council CEH v13',            'config': 'ec-council/ceh_v13.json'},
    {'id': 'ec-chfi',                 'vendor': 'ec-council', 'name': 'EC-Council CHFI v11',           'config': 'ec-council/chfi_v11.json'},
    {'id': 'ec-cnd',                  'vendor': 'ec-council', 'name': 'EC-Council CND v3',             'config': 'ec-council/cnd_v3.json'},
    {'id': 'offsec-oscp',             'vendor': 'offsec',     'name': 'OffSec OSCP',                   'config': 'offsec/oscp_pen-200.json'},
    {'id': 'offsec-oswa',             'vendor': 'offsec',     'name': 'OffSec OSWA',                   'config': 'offsec/oswa_web-200.json'},
    {'id': 'offsec-oswe',             'vendor': 'offsec',     'name': 'OffSec OSWE',                   'config': 'offsec/oswe_web-300.json'},
    {'id': 'hashicorp-terraform',     'vendor': 'hashicorp',  'name': 'HashiCorp Terraform Associate', 'config': 'hashicorp/terraform_associate_003.json'},
    {'id': 'hashicorp-vault',         'vendor': 'hashicorp',  'name': 'HashiCorp Vault Associate',     'config': 'hashicorp/vault_associate_003.json'},
    {'id': 'k8s-cka',                 'vendor': 'k8s',        'name': 'Kubernetes CKA',                'config': 'kubernetes/cka.json'},
    {'id': 'k8s-ckad',                'vendor': 'k8s',        'name': 'Kubernetes CKAD',               'config': 'kubernetes/ckad.json'},
    {'id': 'k8s-cks',                 'vendor': 'k8s',        'name': 'Kubernetes CKS',                'config': 'kubernetes/cks.json'},
]

VENDOR_NAMES = {
    'comptia': 'CompTIA', 'isc2': 'ISC2', 'aws': 'AWS', 'microsoft': 'Microsoft',
    'cisco': 'Cisco', 'isaca': 'ISACA', 'giac': 'GIAC', 'google': 'Google Cloud',
    'ec-council': 'EC-Council', 'offsec': 'OffSec', 'hashicorp': 'HashiCorp',
    'k8s': 'Kubernetes',
}

VENDOR_STORE_PAGES = {
    'comptia': '/store/comptia.html', 'isc2': '/store/security-governance.html',
    'aws': '/store/aws.html', 'microsoft': '/store/microsoft.html',
    'cisco': '/store/cisco.html', 'isaca': '/store/security-governance.html',
    'giac': '/store/security-governance.html', 'google': '/store/google-cloud.html',
    'ec-council': '/store/offensive-devops.html', 'offsec': '/store/offensive-devops.html',
    'hashicorp': '/store/offensive-devops.html', 'k8s': '/store/offensive-devops.html',
}

QUIZ_MAP = {
    'comptia-security-plus': 'security-quiz.html', 'comptia-a-plus-1201': 'aplus-quiz.html',
    'comptia-a-plus-1202': 'aplus2-quiz.html', 'comptia-network-plus': 'network-plus-quiz.html',
    'comptia-linux-plus': 'linux-plus-quiz.html', 'comptia-cloud-plus': 'cloud-plus-quiz.html',
    'comptia-cysa-plus': 'cysa-plus-quiz.html', 'comptia-pentest-plus': 'pentest-plus-quiz.html',
    'comptia-casp-plus': 'casp-plus-quiz.html', 'comptia-server-plus': 'server-plus-quiz.html',
    'comptia-data-plus': 'data-plus-quiz.html', 'comptia-project-plus': 'project-plus-quiz.html',
    'comptia-itf-plus': 'itf-plus-quiz.html', 'isc2-cc': 'isc2-cc-quiz.html',
    'isc2-sscp': 'isc2-sscp-quiz.html', 'isc2-cissp': 'cissp-quiz.html',
    'isc2-ccsp': 'isc2-ccsp-quiz.html', 'aws-cloud-practitioner': 'aws-clf-quiz.html',
    'aws-solutions-architect': 'aws-saa-quiz.html', 'aws-developer': 'aws-dva-quiz.html',
    'aws-cloudops': 'aws-soa-quiz.html', 'aws-security-specialty': 'aws-security-quiz.html',
    'aws-database-specialty': 'aws-dbs-quiz.html', 'aws-machine-learning': 'aws-mls-quiz.html',
    'aws-data-engineer': 'aws-dea-quiz.html', 'ms-az-900': 'az900-quiz.html',
    'ms-az-104': 'az104-quiz.html', 'ms-az-305': 'az305-quiz.html',
    'ms-sc-900': 'sc900-quiz.html', 'ms-ai-900': 'ai900-quiz.html',
    'ms-az-500': 'az500-quiz.html', 'ms-az-204': 'az204-quiz.html',
    'ms-az-400': 'az400-quiz.html', 'ms-dp-900': 'dp900-quiz.html',
    'ms-ms-900': 'ms900-quiz.html', 'ms-sc-300': 'sc300-quiz.html',
    'ms-ai-102': 'ai102-quiz.html', 'cisco-ccna': 'ccna-quiz.html',
    'cisco-ccnp-encor': 'ccnp-quiz.html', 'cisco-cyberops': 'cyberops-quiz.html',
    'cisco-ccnp-security': 'ccnp-security-quiz.html', 'cisco-devnet': 'devnet-quiz.html',
    'isaca-cisa': 'cisa-quiz.html', 'isaca-cism': 'cism-quiz.html',
    'isaca-crisc': 'crisc-quiz.html', 'giac-gsec': 'gsec-quiz.html',
    'giac-gcih': 'gcih-quiz.html', 'giac-gpen': 'gpen-quiz.html',
    'giac-gcia': 'gcia-quiz.html', 'google-ace': 'gcp-ace-quiz.html',
    'google-pca': 'gcp-pca-quiz.html', 'google-cdl': 'gcp-cdl-quiz.html',
    'google-pde': 'gcp-pde-quiz.html', 'google-pse': 'gcp-pse-quiz.html',
    'ec-ceh': 'ceh-quiz.html', 'ec-chfi': 'chfi-quiz.html', 'ec-cnd': 'cnd-quiz.html',
    'offsec-oscp': 'oscp-quiz.html', 'offsec-oswa': 'oswa-quiz.html',
    'offsec-oswe': 'oswe-quiz.html', 'hashicorp-terraform': 'terraform-quiz.html',
    'hashicorp-vault': 'vault-quiz.html', 'k8s-cka': 'cka-quiz.html',
    'k8s-ckad': 'ckad-quiz.html', 'k8s-cks': 'cks-quiz.html',
}

FREE_RESOURCES = {
    'comptia': '<a href="https://www.professormesser.com/" target="_blank" rel="noopener">Professor Messer</a>, <a href="https://www.comptia.org/training/certmaster-practice" target="_blank" rel="noopener">CertMaster Practice</a>',
    'aws': '<a href="https://explore.skillbuilder.aws/" target="_blank" rel="noopener">AWS Skill Builder</a>, <a href="https://docs.aws.amazon.com/" target="_blank" rel="noopener">AWS Docs</a>',
    'microsoft': '<a href="https://learn.microsoft.com/" target="_blank" rel="noopener">Microsoft Learn</a>, <a href="https://azure.microsoft.com/en-us/free/" target="_blank" rel="noopener">Azure Free Account</a>',
    'cisco': '<a href="https://www.netacad.com/" target="_blank" rel="noopener">Cisco NetAcad</a>, <a href="https://learningnetwork.cisco.com/" target="_blank" rel="noopener">Learning Network</a>',
    'isc2': '<a href="https://www.isc2.org/candidate" target="_blank" rel="noopener">ISC2 Candidate Resources</a>',
    'isaca': '<a href="https://www.isaca.org/resources" target="_blank" rel="noopener">ISACA Resources</a>',
    'giac': '<a href="https://www.sans.org/white-papers/" target="_blank" rel="noopener">SANS Reading Room</a>',
    'google': '<a href="https://www.cloudskillsboost.google/" target="_blank" rel="noopener">Cloud Skills Boost</a>, <a href="https://cloud.google.com/docs" target="_blank" rel="noopener">Google Cloud Docs</a>',
    'ec-council': '<a href="https://codered.eccouncil.org/" target="_blank" rel="noopener">EC-Council CodeRed</a>',
    'offsec': '<a href="https://www.offsec.com/labs/" target="_blank" rel="noopener">Proving Grounds</a>',
    'hashicorp': '<a href="https://developer.hashicorp.com/tutorials" target="_blank" rel="noopener">HashiCorp Tutorials</a>',
    'k8s': '<a href="https://kubernetes.io/docs/" target="_blank" rel="noopener">K8s Docs</a>, <a href="https://killer.sh/" target="_blank" rel="noopener">Killer.sh</a>',
}

# Heatmap colors (same as cert pages)
HEATMAP_COLORS = ['#667eea', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6', '#06b6d4',
                  '#ec4899', '#84cc16', '#f97316', '#6366f1']


def generate_heatmap(domains):
    """Generate domain weight heatmap bars."""
    if not domains:
        return ''
    bars = ''
    for i, d in enumerate(domains):
        pct_str = d.get('percentage', '0%').replace('%', '')
        try:
            pct = float(pct_str)
        except ValueError:
            pct = 0
        color = HEATMAP_COLORS[i % len(HEATMAP_COLORS)]
        name = escape(d.get('name', f'Domain {d.get("number", i+1)}'))
        bars += f'''
                <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;">
                    <span style="min-width:120px;font-size:0.8rem;color:var(--text-secondary);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">D{d.get("number",i+1)}: {name}</span>
                    <div style="flex:1;background:var(--bg-tertiary,rgba(128,128,128,0.15));border-radius:4px;height:22px;overflow:hidden;">
                        <div style="width:{pct}%;background:{color};height:100%;border-radius:4px;display:flex;align-items:center;justify-content:flex-end;padding-right:6px;font-size:0.7rem;font-weight:700;color:white;min-width:32px;">{pct_str}%</div>
                    </div>
                </div>'''
    return f'''
            <div style="background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:1.25rem;margin-bottom:2rem;">
                <h3 style="font-size:1rem;margin-bottom:0.75rem;">Domain Weight Distribution</h3>{bars}
            </div>'''


def generate_timeline(weekly_plan, num_weeks, pid):
    """Generate week-by-week timeline cards."""
    cards = ''
    for i in range(num_weeks):
        topic = escape(weekly_plan[i]) if i < len(weekly_plan) else f'Review and practice — Week {i+1}'
        week_num = i + 1
        cards += f'''
            <div class="timeline-card" data-week="{week_num}">
                <div class="timeline-marker">
                    <input type="checkbox" class="week-check" data-week="{week_num}" id="week-{week_num}" aria-label="Mark week {week_num} complete">
                    <div class="timeline-line"></div>
                </div>
                <div class="timeline-content">
                    <div class="timeline-week">Week {week_num}</div>
                    <p class="timeline-topic">{topic}</p>
                </div>
            </div>'''
    return cards


def generate_roadmap_page(product, config):
    pid = product['id']
    name = product['name']
    vendor_id = product['vendor']
    vendor = VENDOR_NAMES.get(vendor_id, vendor_id)

    domains = config.get('domains', [])
    weekly_plan = config.get('weekly_study_plan', [])
    num_weeks = config.get('planner_settings', {}).get('num_weeks', 12)
    exam_code = config.get('exam_details', {}).get('exam_code', product.get('meta', '').split('·')[0].strip() if 'meta' in product else '')

    heatmap = generate_heatmap(domains)
    timeline = generate_timeline(weekly_plan, num_weeks, pid)
    free_res = FREE_RESOURCES.get(vendor_id, '')
    store_page = VENDOR_STORE_PAGES.get(vendor_id, '/store/store.html')

    # Build FAQPage schema
    domain_list_str = ''
    if domains:
        parts = []
        for d in domains:
            pct = d.get('percentage', '')
            parts.append(f"{d['name']} ({pct})" if pct else d['name'])
        domain_list_str = ', '.join(parts)

    faq_a1 = (f"A structured study plan for {name} spans {num_weeks} weeks. "
              f"Each week focuses on specific exam domains with targeted objectives, "
              f"building knowledge progressively from foundational concepts to advanced topics.")
    if domain_list_str:
        faq_a2 = f"The {name} exam covers these domains: {domain_list_str}. Focus more study time on higher-weighted domains."
    else:
        faq_a2 = f"The {name} exam covers multiple domains. Check the official exam objectives for the complete domain breakdown and weight distribution."
    faq_a3 = (f"The best study approach for {name} is to follow a structured roadmap: "
              f"start with the domain heatmap to understand weight distribution, "
              f"then work through each week's objectives sequentially. "
              f"Use practice quizzes to test retention and track your progress with the built-in checklist.")

    faq_schema_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"How long should I study for {name}?",
             "acceptedAnswer": {"@type": "Answer", "text": faq_a1}},
            {"@type": "Question", "name": f"What domains does the {name} exam cover?",
             "acceptedAnswer": {"@type": "Answer", "text": faq_a2}},
            {"@type": "Question", "name": f"What's the best study approach for {name}?",
             "acceptedAnswer": {"@type": "Answer", "text": faq_a3}},
        ]
    }, indent=4, ensure_ascii=False)

    quiz_link = QUIZ_MAP.get(pid, '')
    quiz_html = ''
    if quiz_link:
        quiz_html = f'''
                <a href="/{quiz_link}" style="display:block;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:1rem;text-decoration:none;color:inherit;transition:transform 0.2s;">
                    <span style="font-size:1.3rem;">&#x1F9EA;</span>
                    <h4 style="margin:0.4rem 0 0.2rem;font-size:0.9rem;">Practice Quiz</h4>
                    <p style="font-size:0.8rem;color:var(--text-secondary);margin:0;">Test your knowledge with free practice questions</p>
                </a>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="dns-prefetch" href="https://static.cloudflareinsights.com">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} Study Roadmap — Free Week-by-Week Plan | FixTheVuln</title>
    <meta name="description" content="Free {name} study roadmap. {num_weeks}-week plan with domain weights, free resources, and progress tracking. Start your {name} journey today.">
    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <meta property="og:title" content="{name} Study Roadmap | FixTheVuln">
    <meta property="og:description" content="Free {num_weeks}-week study roadmap for {name} with domain weights and free resources.">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://fixthevuln.com/roadmaps/{pid}.html">
    <meta property="og:image" content="https://fixthevuln.com/og-image.png">
    <link rel="canonical" href="https://fixthevuln.com/roadmaps/{pid}.html">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{name} Study Roadmap | FixTheVuln">
    <meta name="twitter:description" content="Free {num_weeks}-week study roadmap for {name}.">
    <link rel="stylesheet" href="/style.min.css?v=7">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://fixthevuln.com/" }},
            {{ "@type": "ListItem", "position": 2, "name": "Roadmaps", "item": "https://fixthevuln.com/roadmaps/" }},
            {{ "@type": "ListItem", "position": 3, "name": "{escape(name)} Roadmap" }}
        ]
    }}
    </script>
    <script type="application/ld+json">
{faq_schema_json}
</script>
    <style>
        .roadmap-hero {{ text-align: center; padding: 2rem 1.5rem 1rem; }}
        .roadmap-hero h1 {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
        .roadmap-badge {{ display: inline-block; background: var(--accent-color); color: white; padding: 4px 14px; border-radius: 50px; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.75rem; }}
        .roadmap-meta {{ color: var(--text-secondary); font-size: 0.9rem; }}
        .roadmap-content {{ max-width: 800px; margin: 0 auto; padding: 0 1.5rem; }}
        .roadmap-content h2 {{ font-size: 1.3rem; margin: 2rem 0 1rem; border-bottom: 2px solid var(--accent-color); padding-bottom: 0.5rem; }}

        /* Timeline */
        .timeline {{ position: relative; padding-left: 0; }}
        .timeline-card {{ display: flex; gap: 1rem; margin-bottom: 0; }}
        .timeline-marker {{ display: flex; flex-direction: column; align-items: center; width: 28px; flex-shrink: 0; }}
        .timeline-marker input[type="checkbox"] {{ width: 20px; height: 20px; accent-color: var(--accent-color); cursor: pointer; margin: 0; z-index: 1; }}
        .timeline-line {{ flex: 1; width: 2px; background: var(--border-color); margin-top: 4px; }}
        .timeline-card:last-child .timeline-line {{ display: none; }}
        .timeline-content {{ flex: 1; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem; }}
        .timeline-card.completed .timeline-content {{ opacity: 0.6; }}
        .timeline-week {{ font-size: 0.75rem; font-weight: 700; color: var(--accent-color); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.25rem; }}
        .timeline-topic {{ font-size: 0.9rem; color: var(--text-secondary); margin: 0; line-height: 1.5; }}

        /* Progress bar */
        .roadmap-progress {{ background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 10px; padding: 1rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem; }}
        .roadmap-progress-track {{ flex: 1; height: 10px; background: var(--border-color); border-radius: 5px; overflow: hidden; }}
        .roadmap-progress-fill {{ height: 100%; background: var(--accent-color); border-radius: 5px; transition: width 0.3s; }}
        .roadmap-progress-text {{ font-size: 0.85rem; font-weight: 600; min-width: 50px; text-align: right; }}

        .cross-links {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem; margin-top: 1.5rem; }}
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
        <a href="/roadmaps/" class="back-link">&larr; All Roadmaps</a>

        <section class="roadmap-hero">
            <span class="roadmap-badge">{escape(vendor)}</span>
            <h1>{escape(name)} Study Roadmap</h1>
            <p class="roadmap-meta">{escape(exam_code)} &middot; {num_weeks}-week plan &middot; Free</p>
            <p style="font-size:0.85rem;color:var(--text-secondary);margin-top:0.5rem;">Last updated: {TODAY}</p>
        </section>

        <div class="roadmap-content">
            <div class="roadmap-progress">
                <span style="font-size:0.85rem;color:var(--text-secondary);">Progress:</span>
                <div class="roadmap-progress-track"><div class="roadmap-progress-fill" id="progressFill" style="width:0%"></div></div>
                <span class="roadmap-progress-text" id="progressText">0/{num_weeks}</span>
            </div>

            {heatmap}

            <h2>Week-by-Week Study Plan</h2>
            <div class="timeline" id="timeline">
                {timeline}
            </div>

            <h2>Free Resources</h2>
            <p style="color:var(--text-secondary);line-height:1.6;">
                {free_res if free_res else 'Check the official vendor website for free study resources.'}
            </p>

            <h2>Related Tools</h2>
            <div class="cross-links">
                <a href="/certs/{pid}.html" style="display:block;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:1rem;text-decoration:none;color:inherit;transition:transform 0.2s;">
                    <span style="font-size:1.3rem;">&#x1F4D6;</span>
                    <h4 style="margin:0.4rem 0 0.2rem;font-size:0.9rem;">{escape(name)} Study Guide</h4>
                    <p style="font-size:0.8rem;color:var(--text-secondary);margin:0;">Complete exam objectives and domain breakdown</p>
                </a>
                <a href="/study-tracker.html" style="display:block;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:1rem;text-decoration:none;color:inherit;transition:transform 0.2s;">
                    <span style="font-size:1.3rem;">&#x2705;</span>
                    <h4 style="margin:0.4rem 0 0.2rem;font-size:0.9rem;">Study Tracker</h4>
                    <p style="font-size:0.8rem;color:var(--text-secondary);margin:0;">Track objective completion with progress dashboard</p>
                </a>
                <a href="/cert-cost-calculator.html" style="display:block;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:1rem;text-decoration:none;color:inherit;transition:transform 0.2s;">
                    <span style="font-size:1.3rem;">&#x1F4B0;</span>
                    <h4 style="margin:0.4rem 0 0.2rem;font-size:0.9rem;">Cost Calculator</h4>
                    <p style="font-size:0.8rem;color:var(--text-secondary);margin:0;">Total cost breakdown and ROI analysis</p>
                </a>{quiz_html}
            </div>

            <div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);padding:1.5rem;border-radius:10px;color:white;margin-top:2rem;text-align:center;">
                <p style="text-transform:uppercase;letter-spacing:2px;font-size:0.65rem;opacity:0.6;margin-bottom:0.3rem;">FixTheVuln Store</p>
                <h3 style="color:white;margin-bottom:0.5rem;">Get the {escape(name)} Study Planner</h3>
                <p style="opacity:0.9;margin-bottom:1rem;">Fillable PDF with {num_weeks}-week schedule, domain trackers, flashcard templates, and progress tracking.</p>
                <a href="{store_page}" style="display:inline-block;background:#667eea;color:white;padding:0.75rem 1.5rem;border-radius:6px;text-decoration:none;font-weight:600;">Get the Study Planner &mdash; $5.99</a>
            </div>
        </div>
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

        // Roadmap progress persistence
        const ROADMAP_KEY = 'ftv-roadmap-{pid}';
        const NUM_WEEKS = {num_weeks};

        function loadRoadmapProgress() {{
            try {{ return JSON.parse(localStorage.getItem(ROADMAP_KEY)) || []; }} catch {{ return []; }}
        }}
        function saveRoadmapProgress(arr) {{
            try {{ localStorage.setItem(ROADMAP_KEY, JSON.stringify(arr)); }} catch {{}}
        }}

        function updateProgressBar() {{
            const checked = loadRoadmapProgress();
            const pct = Math.round((checked.length / NUM_WEEKS) * 100);
            document.getElementById('progressFill').style.width = pct + '%';
            document.getElementById('progressText').textContent = checked.length + '/' + NUM_WEEKS;
        }}

        // Init checkboxes from saved state
        const savedWeeks = loadRoadmapProgress();
        document.querySelectorAll('.week-check').forEach(cb => {{
            const week = parseInt(cb.dataset.week);
            if (savedWeeks.includes(week)) {{
                cb.checked = true;
                cb.closest('.timeline-card').classList.add('completed');
            }}
            cb.addEventListener('change', function() {{
                const w = parseInt(this.dataset.week);
                let progress = loadRoadmapProgress();
                if (this.checked) {{
                    if (!progress.includes(w)) progress.push(w);
                    this.closest('.timeline-card').classList.add('completed');
                }} else {{
                    progress = progress.filter(x => x !== w);
                    this.closest('.timeline-card').classList.remove('completed');
                }}
                saveRoadmapProgress(progress);
                updateProgressBar();
            }});
        }});
        updateProgressBar();
    </script>
<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "8304415b01684a00adedcbf6975458d7"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>'''


def generate_hub_page(generated_products):
    """Generate the roadmaps hub page listing all certs grouped by vendor."""
    vendors = {}
    for p in generated_products:
        v = VENDOR_NAMES.get(p['vendor'], p['vendor'])
        if v not in vendors:
            vendors[v] = []
        vendors[v].append(p)

    cards_html = ''
    for vendor_name in sorted(vendors.keys()):
        cards_html += f'\n            <h3 style="margin-top:1.5rem;margin-bottom:0.75rem;font-size:1.1rem;border-bottom:1px solid var(--border-color);padding-bottom:0.5rem;">{escape(vendor_name)}</h3>\n            <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:0.75rem;">'
        for p in vendors[vendor_name]:
            cards_html += f'''
                <a href="{p['id']}.html" style="display:block;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:8px;padding:1rem;text-decoration:none;color:inherit;transition:transform 0.2s;">
                    <h4 style="font-size:0.95rem;margin:0 0 0.25rem;">{escape(p['name'])}</h4>
                    <p style="font-size:0.8rem;color:var(--text-secondary);margin:0;">{p.get('weeks', 12)}-week roadmap</p>
                </a>'''
        cards_html += '\n            </div>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="dns-prefetch" href="https://static.cloudflareinsights.com">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Certification Study Roadmaps — 65+ IT Certs | FixTheVuln</title>
    <meta name="description" content="Free week-by-week study roadmaps for 65+ IT certifications. CompTIA, AWS, Azure, Cisco, CISSP, and more. Progress tracking included.">
    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <meta property="og:title" content="Certification Study Roadmaps | FixTheVuln">
    <meta property="og:description" content="Free study roadmaps for 65+ IT certifications with week-by-week plans.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://fixthevuln.com/roadmaps/">
    <meta property="og:image" content="https://fixthevuln.com/og-image.png">
    <link rel="canonical" href="https://fixthevuln.com/roadmaps/">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Certification Study Roadmaps | FixTheVuln">
    <meta name="twitter:description" content="Free study roadmaps for 65+ IT certifications.">
    <link rel="stylesheet" href="/style.min.css?v=7">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://fixthevuln.com/" }},
            {{ "@type": "ListItem", "position": 2, "name": "Study Roadmaps" }}
        ]
    }}
    </script>
</head>
<body>
    <nav class="site-nav">
        <div class="container">
            <a href="/index.html" class="site-nav-logo">FixTheVuln</a>
            <button class="nav-toggle" aria-label="Menu" onclick="this.classList.toggle('active');this.parentElement.querySelector('.site-nav-links').classList.toggle('open')"><span></span><span></span><span></span></button>
            <div class="site-nav-links">
                <a href="/guides.html">Guides</a>
                <a href="/tools.html">Tools</a>
                <a href="/compliance.html">Compliance</a>
                <a href="/resources.html">Resources</a>
                <a href="/practice-tests.html">Quizzes</a>
                <a href="/career-paths.html">Career Paths</a>
                <a href="/blog/">Blog</a>
                <a href="/store/store.html" style="background: linear-gradient(135deg, #2563eb, #7c3aed); color: white; padding: .35rem .75rem; border-radius: 6px; font-size: .85rem; font-weight: 600; text-decoration: none;">Store</a>
            </div>
        </div>
    </nav>

    <main class="container">
        <a href="/career-paths.html" class="back-link">&larr; Career Paths</a>

        <div style="text-align:center;padding:2rem 1.5rem 1rem;">
            <h1 style="font-size:2rem;margin-bottom:0.5rem;">Certification Study Roadmaps</h1>
            <p style="color:var(--text-secondary);max-width:600px;margin:0 auto;">Free week-by-week study plans for 65+ IT certifications. Each roadmap includes domain weights, free resources, and progress tracking that saves to your browser.</p>
            <p style="font-size:0.85rem;color:var(--text-secondary);margin-top:0.5rem;">Last updated: {TODAY}</p>
            <div style="display:flex;flex-wrap:wrap;gap:0.75rem;margin-top:1rem;justify-content:center;">
                <span style="background:#d4edda;color:#155724;padding:0.4rem 0.8rem;border-radius:15px;font-size:0.85rem;font-weight:500;">100% Free</span>
                <span style="background:#fff3cd;color:#856404;padding:0.4rem 0.8rem;border-radius:15px;font-size:0.85rem;font-weight:500;">No Sign-up Required</span>
                <span style="background:#d1ecf1;color:#0c5460;padding:0.4rem 0.8rem;border-radius:15px;font-size:0.85rem;font-weight:500;">Progress Saves Locally</span>
            </div>
        </div>

        <section style="max-width:900px;margin:0 auto;padding:0 1.5rem;">
            {cards_html}
        </section>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 FixTheVuln. Educational resources for security professionals.</p>
            <p><a href="/index.html">Home</a> | <a href="https://fixthevuln.com">FixTheVuln.com</a> | Study Planners: <a href="/store/store.html">FixTheVuln Store</a></p>
        </div>
    </footer>

    <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">
        <span id="theme-icon">&#9790;</span>
    </button>
    <script>
        function toggleTheme() {{
            const html = document.documentElement;
            const current = html.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            localStorage.setItem('fixthevuln-theme', next);
            document.getElementById('theme-icon').textContent = next === 'dark' ? '\\u2600\\uFE0F' : '\\uD83C\\uDF19';
        }}
        (function() {{
            const saved = localStorage.getItem('fixthevuln-theme');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const theme = saved || (prefersDark ? 'dark' : 'light');
            if (theme === 'dark') {{
                document.documentElement.setAttribute('data-theme', 'dark');
                document.getElementById('theme-icon').textContent = '\\u2600\\uFE0F';
            }}
        }})();
    </script>
<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "8304415b01684a00adedcbf6975458d7"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>'''


def main():
    ROADMAPS_DIR.mkdir(exist_ok=True)
    generated = 0
    no_config = 0
    generated_products = []

    for product in PRODUCTS:
        pid = product['id']
        config_path = ETSY_CERTS / product['config']
        if not config_path.exists():
            print(f"  NOCONFIG {pid}")
            no_config += 1
            continue
        try:
            config = json.loads(config_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            print(f"  ERROR {pid} — bad config")
            continue

        html = generate_roadmap_page(product, config)
        filepath = ROADMAPS_DIR / f'{pid}.html'
        filepath.write_text(html, encoding='utf-8')

        num_weeks = config.get('planner_settings', {}).get('num_weeks', 12)
        generated_products.append({**product, 'weeks': num_weeks})
        print(f"  OK   roadmaps/{pid}.html ({num_weeks} weeks)")
        generated += 1

    # Generate hub page
    hub_html = generate_hub_page(generated_products)
    hub_path = ROADMAPS_DIR / 'index.html'
    hub_path.write_text(hub_html, encoding='utf-8')
    print(f"  OK   roadmaps/index.html (hub)")

    print(f"\nDone: {generated} roadmap pages + 1 hub ({no_config} skipped without config)")


if __name__ == '__main__':
    main()
