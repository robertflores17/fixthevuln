#!/usr/bin/env python3
"""Generate tracker-objectives.json from cert configs.
Outputs domain names, weights, objectives, and key concepts per cert
for the Study Tracker tool page."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ETSY_CERTS = Path(__file__).resolve().parent.parent.parent / 'Dropshipping' / 'Etsy-Claude' / 'certifications'

# Product catalog (mirrors generate_cert_pages.py)
PRODUCTS = [
    {'id': 'comptia-a-plus-1201',     'vendor': 'comptia',    'name': 'CompTIA A+ Core 1',            'config': 'comptia/a_plus_1201.json'},
    {'id': 'comptia-a-plus-1202',     'vendor': 'comptia',    'name': 'CompTIA A+ Core 2',            'config': 'comptia/a_plus_1202.json'},
    {'id': 'comptia-security-plus',   'vendor': 'comptia',    'name': 'CompTIA Security+',            'config': 'comptia/security_plus_701.json'},
    {'id': 'comptia-network-plus',    'vendor': 'comptia',    'name': 'CompTIA Network+',             'config': 'comptia/network_plus_009.json'},
    {'id': 'comptia-linux-plus',      'vendor': 'comptia',    'name': 'CompTIA Linux+',               'config': 'comptia/linux_plus_006.json'},
    {'id': 'comptia-cloud-plus',      'vendor': 'comptia',    'name': 'CompTIA Cloud+',               'config': 'comptia/cloud_plus_004.json'},
    {'id': 'comptia-cysa-plus',       'vendor': 'comptia',    'name': 'CompTIA CySA+',                'config': 'comptia/cysa_plus_003.json'},
    {'id': 'comptia-pentest-plus',    'vendor': 'comptia',    'name': 'CompTIA PenTest+',             'config': 'comptia/pentest_plus_003.json'},
    {'id': 'comptia-casp-plus',       'vendor': 'comptia',    'name': 'CompTIA CASP+',                'config': 'comptia/casp_plus_005.json'},
    {'id': 'comptia-server-plus',     'vendor': 'comptia',    'name': 'CompTIA Server+',              'config': 'comptia/server_plus_005.json'},
    {'id': 'comptia-data-plus',       'vendor': 'comptia',    'name': 'CompTIA Data+',                'config': 'comptia/data_plus_001.json'},
    {'id': 'comptia-project-plus',    'vendor': 'comptia',    'name': 'CompTIA Project+',             'config': 'comptia/project_plus_005.json'},
    {'id': 'comptia-itf-plus',        'vendor': 'comptia',    'name': 'CompTIA ITF+',                 'config': 'comptia/itf_plus_u71.json'},
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


def main():
    certs = []
    for product in PRODUCTS:
        config_path = ETSY_CERTS / product['config']
        if not config_path.exists():
            continue
        try:
            config = json.loads(config_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            continue

        domains = config.get('domains', [])
        if not domains:
            continue

        cert_domains = []
        for d in domains:
            cert_domains.append({
                'number': d.get('number', 0),
                'name': d.get('name', ''),
                'percentage': d.get('percentage', '0%'),
                'objectives': d.get('objectives', []),
                'key_concepts': d.get('key_concepts', []),
            })

        certs.append({
            'id': product['id'],
            'name': product['name'],
            'vendor': VENDOR_NAMES.get(product['vendor'], product['vendor']),
            'vendor_id': product['vendor'],
            'domains': cert_domains,
        })

    output = {'certs': certs}
    out_path = REPO / 'data' / 'tracker-objectives.json'
    out_path.write_text(json.dumps(output, indent=2), encoding='utf-8')
    total_objectives = sum(len(obj) for c in certs for d in c['domains'] for obj in [d['objectives']])
    print(f'  Generated {out_path} with {len(certs)} certs, {total_objectives} total objectives')


if __name__ == '__main__':
    main()
