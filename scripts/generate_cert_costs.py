#!/usr/bin/env python3
"""Generate cert-costs.json from cert configs and comparison data.
Consolidates exam fees, retake info, study weeks, salary ranges,
and resource links for the Cert Cost Calculator tool page."""

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ETSY_CERTS = Path(__file__).resolve().parent.parent.parent / 'Dropshipping' / 'Etsy-Claude' / 'certifications'

# Product catalog (mirrors generate_cert_pages.py)
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

VENDOR_NAMES = {
    'comptia': 'CompTIA', 'isc2': 'ISC2', 'aws': 'AWS', 'microsoft': 'Microsoft',
    'cisco': 'Cisco', 'isaca': 'ISACA', 'giac': 'GIAC', 'google': 'Google Cloud',
    'ec-council': 'EC-Council', 'offsec': 'OffSec', 'hashicorp': 'HashiCorp',
    'k8s': 'Kubernetes',
}

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

# Free study resources by vendor
FREE_RESOURCES = {
    'comptia': [
        {'name': 'Professor Messer Videos', 'url': 'https://www.professormesser.com/'},
        {'name': 'CompTIA CertMaster Practice', 'url': 'https://www.comptia.org/training/certmaster-practice'},
    ],
    'aws': [
        {'name': 'AWS Skill Builder', 'url': 'https://explore.skillbuilder.aws/'},
        {'name': 'AWS Documentation', 'url': 'https://docs.aws.amazon.com/'},
    ],
    'microsoft': [
        {'name': 'Microsoft Learn', 'url': 'https://learn.microsoft.com/'},
        {'name': 'Azure Free Account', 'url': 'https://azure.microsoft.com/en-us/free/'},
    ],
    'cisco': [
        {'name': 'Cisco NetAcad', 'url': 'https://www.netacad.com/'},
        {'name': 'Cisco Learning Network', 'url': 'https://learningnetwork.cisco.com/'},
    ],
    'isc2': [
        {'name': 'ISC2 Candidate Resources', 'url': 'https://www.isc2.org/candidate'},
    ],
    'isaca': [
        {'name': 'ISACA Resources', 'url': 'https://www.isaca.org/resources'},
    ],
    'giac': [
        {'name': 'SANS Reading Room', 'url': 'https://www.sans.org/white-papers/'},
    ],
    'google': [
        {'name': 'Google Cloud Skills Boost', 'url': 'https://www.cloudskillsboost.google/'},
        {'name': 'Google Cloud Documentation', 'url': 'https://cloud.google.com/docs'},
    ],
    'ec-council': [
        {'name': 'EC-Council CodeRed', 'url': 'https://codered.eccouncil.org/'},
    ],
    'offsec': [
        {'name': 'OffSec Proving Grounds', 'url': 'https://www.offsec.com/labs/'},
    ],
    'hashicorp': [
        {'name': 'HashiCorp Learn', 'url': 'https://developer.hashicorp.com/tutorials'},
    ],
    'k8s': [
        {'name': 'Kubernetes Documentation', 'url': 'https://kubernetes.io/docs/'},
        {'name': 'Killer.sh Practice', 'url': 'https://killer.sh/'},
    ],
}


def parse_cost(cost_str):
    """Extract numeric cost from string like '$404 USD' or '$1,749 USD (course + exam)'."""
    if not cost_str:
        return 0
    m = re.search(r'\$[\d,]+', cost_str)
    if m:
        return int(m.group().replace('$', '').replace(',', ''))
    return 0


def parse_salary_range(salary_str):
    """Parse salary range like '$65,000–$95,000' into (min, max)."""
    if not salary_str or salary_str == 'N/A':
        return (0, 0)
    nums = re.findall(r'\$?([\d,]+)', salary_str)
    if len(nums) >= 2:
        return (int(nums[0].replace(',', '')), int(nums[1].replace(',', '')))
    elif len(nums) == 1:
        val = int(nums[0].replace(',', ''))
        return (val, val)
    return (0, 0)


def main():
    # Load comparison data for salary ranges
    comp_path = REPO / 'data' / 'cert-comparisons.json'
    comparisons = {}
    if comp_path.exists():
        comp_data = json.loads(comp_path.read_text(encoding='utf-8'))
        comparisons = comp_data.get('certifications', {})

    # Build a lookup from product ID to comparison key
    # The comparison keys use different naming than product IDs
    pid_to_comp = {}
    for p in PRODUCTS:
        # Try exact match with hyphens
        pid = p['id']
        # Try common transformations
        candidates = [
            pid,
            pid.replace('comptia-', ''),
            pid.replace('isc2-', ''),
            pid.replace('aws-', 'aws-'),
            pid.replace('ms-', ''),
        ]
        for key in comparisons:
            if key in candidates or pid.endswith(key) or key.endswith(pid.split('-', 1)[-1] if '-' in pid else pid):
                pid_to_comp[pid] = key
                break

    certs = []
    for product in PRODUCTS:
        pid = product['id']
        vendor = product['vendor']
        name = product['name']
        exam_code = product['meta'].split('·')[0].strip()

        # Load cert config
        config_path = ETSY_CERTS / product['config']
        config = None
        if config_path.exists():
            try:
                config = json.loads(config_path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, IOError):
                pass

        # Extract exam details from config
        exam_details = config.get('exam_details', {}) if config else {}
        exam_fee = parse_cost(exam_details.get('exam_cost', ''))
        study_weeks = config.get('planner_settings', {}).get('num_weeks', 12) if config else 12
        retake_policy = exam_details.get('retake_policy', 'Check vendor website')

        # Get salary from comparison data
        comp_key = pid_to_comp.get(pid, '')
        comp_entry = comparisons.get(comp_key, {})
        salary_str = comp_entry.get('salary_range', '')
        salary_min, salary_max = parse_salary_range(salary_str)

        # Free resources
        free_resources = FREE_RESOURCES.get(vendor, [])

        # Build paid resources list
        paid_resources = [
            {'name': f'{name} Study Planner', 'cost': 5.99}
        ]

        # Quiz and cert page URLs
        quiz_url = f'/{QUIZ_MAP[pid]}' if pid in QUIZ_MAP else ''
        cert_page_url = f'/certs/{pid}.html'
        planner_url = VENDOR_STORE_PAGES.get(vendor, '/store/store.html')
        roadmap_url = f'/roadmaps/{pid}.html'

        certs.append({
            'id': pid,
            'name': name,
            'exam_code': exam_code,
            'vendor': VENDOR_NAMES.get(vendor, vendor),
            'vendor_id': vendor,
            'exam_fee': exam_fee,
            'retake_policy': retake_policy,
            'study_weeks': study_weeks,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'free_resources': free_resources,
            'paid_resources': paid_resources,
            'planner_url': planner_url,
            'quiz_url': quiz_url,
            'cert_page_url': cert_page_url,
            'roadmap_url': roadmap_url,
        })

    output = {'certs': certs, 'generated': True}
    out_path = REPO / 'data' / 'cert-costs.json'
    out_path.write_text(json.dumps(output, indent=2), encoding='utf-8')
    print(f'  Generated {out_path} with {len(certs)} certifications')


if __name__ == '__main__':
    main()
