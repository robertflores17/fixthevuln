#!/usr/bin/env python3
"""
FixTheVuln — Practice Test Vendor Page Generator

Generates vendor category pages under practice-tests/ from quiz JSON data.
Uses shared templates from scripts/lib/.

Usage:
    python scripts/generate_practice_test_pages.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure scripts/ is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.constants import (
    PRACTICE_TESTS_CSS_VERSION, STYLE_CSS_VERSION,
    SITE_URL, SITE_NAME,
)
from lib.templates import (
    page_wrapper, breadcrumb_schema, faq_schema, esc,
)

# ---------------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / 'data'
OUT_DIR = ROOT / 'practice-tests'

# ---------------------------------------------------------------------------
# Quiz Registry — maps every quiz to its vendor
# ---------------------------------------------------------------------------

QUIZ_REGISTRY = [
    # ── CompTIA (14) ──
    {'quiz': 'security-quiz.html',     'json': 'security-plus-questions.json', 'name': 'CompTIA Security+',    'short': 'Security+',  'exam': 'SY0-701',  'vendor': 'comptia', 'tagline': 'The #1 entry-level cybersecurity certification'},
    {'quiz': 'network-plus-quiz.html', 'json': 'network-plus-questions.json',  'name': 'CompTIA Network+',     'short': 'Network+',   'exam': 'N10-009',  'vendor': 'comptia', 'tagline': 'Essential networking skills for IT professionals'},
    {'quiz': 'aplus-quiz.html',        'json': 'aplus-questions.json',         'name': 'CompTIA A+ Core 1',    'short': 'A+ Core 1',  'exam': '220-1101', 'vendor': 'comptia', 'tagline': 'IT fundamentals for help desk and support'},
    {'quiz': 'aplus2-quiz.html',       'json': 'aplus2-questions.json',        'name': 'CompTIA A+ Core 2',    'short': 'A+ Core 2',  'exam': '220-1202', 'vendor': 'comptia', 'tagline': 'Operating systems, security, and operational procedures'},
    {'quiz': 'linux-plus-quiz.html',   'json': 'linux-plus-questions.json',    'name': 'CompTIA Linux+',       'short': 'Linux+',     'exam': 'XK0-005',  'vendor': 'comptia', 'tagline': 'Linux system administration and troubleshooting'},
    {'quiz': 'cloud-plus-quiz.html',   'json': 'cloud-plus-questions.json',    'name': 'CompTIA Cloud+',       'short': 'Cloud+',     'exam': 'CV0-004',  'vendor': 'comptia', 'tagline': 'Cloud infrastructure and virtualization skills'},
    {'quiz': 'cysa-plus-quiz.html',    'json': 'cysa-plus-questions.json',     'name': 'CompTIA CySA+',        'short': 'CySA+',      'exam': 'CS0-003',  'vendor': 'comptia', 'tagline': 'Cybersecurity analyst skills for SOC teams'},
    {'quiz': 'pentest-plus-quiz.html', 'json': 'pentest-plus-questions.json',  'name': 'CompTIA PenTest+',     'short': 'PenTest+',   'exam': 'PT0-002',  'vendor': 'comptia', 'tagline': 'Hands-on penetration testing and vulnerability assessment'},
    {'quiz': 'casp-plus-quiz.html',    'json': 'casp-plus-questions.json',     'name': 'CompTIA CASP+',        'short': 'CASP+',      'exam': 'CAS-004',  'vendor': 'comptia', 'tagline': 'Advanced security practitioner for enterprise environments'},
    {'quiz': 'server-plus-quiz.html',  'json': 'server-plus-questions.json',   'name': 'CompTIA Server+',      'short': 'Server+',    'exam': 'SK0-005',  'vendor': 'comptia', 'tagline': 'Server hardware and administration fundamentals'},
    {'quiz': 'data-plus-quiz.html',    'json': 'data-plus-questions.json',     'name': 'CompTIA Data+',        'short': 'Data+',      'exam': 'DA0-001',  'vendor': 'comptia', 'tagline': 'Data analytics concepts and visualization'},
    {'quiz': 'project-plus-quiz.html', 'json': 'project-plus-questions.json',  'name': 'CompTIA Project+',     'short': 'Project+',   'exam': 'PK0-005',  'vendor': 'comptia', 'tagline': 'IT project management methodologies'},
    {'quiz': 'itf-plus-quiz.html',     'json': 'itf-plus-questions.json',      'name': 'CompTIA ITF+',         'short': 'ITF+',       'exam': 'FC0-U71',  'vendor': 'comptia', 'tagline': 'IT fundamentals for beginners'},
    {'quiz': 'secai-quiz.html',        'json': 'secai-questions.json',         'name': 'CompTIA SecAI+',       'short': 'SecAI+',     'exam': 'CY0-001',  'vendor': 'comptia', 'tagline': 'AI security for cybersecurity professionals'},

    # ── Microsoft (12) ──
    {'quiz': 'az900-quiz.html',  'json': 'az900-questions.json',  'name': 'Azure Fundamentals',       'short': 'AZ-900',  'exam': 'AZ-900',  'vendor': 'microsoft', 'tagline': 'Cloud concepts and Azure services for beginners'},
    {'quiz': 'az104-quiz.html',  'json': 'az104-questions.json',  'name': 'Azure Administrator',      'short': 'AZ-104',  'exam': 'AZ-104',  'vendor': 'microsoft', 'tagline': 'Azure identity, governance, storage, compute, and networking'},
    {'quiz': 'az204-quiz.html',  'json': 'az204-questions.json',  'name': 'Azure Developer',          'short': 'AZ-204',  'exam': 'AZ-204',  'vendor': 'microsoft', 'tagline': 'Developing solutions for Microsoft Azure'},
    {'quiz': 'az305-quiz.html',  'json': 'az305-questions.json',  'name': 'Azure Solutions Architect', 'short': 'AZ-305',  'exam': 'AZ-305',  'vendor': 'microsoft', 'tagline': 'Designing Azure infrastructure solutions'},
    {'quiz': 'az400-quiz.html',  'json': 'az400-questions.json',  'name': 'Azure DevOps Engineer',    'short': 'AZ-400',  'exam': 'AZ-400',  'vendor': 'microsoft', 'tagline': 'DevOps practices for Azure'},
    {'quiz': 'az500-quiz.html',  'json': 'az500-questions.json',  'name': 'Azure Security Engineer',  'short': 'AZ-500',  'exam': 'AZ-500',  'vendor': 'microsoft', 'tagline': 'Implementing security controls on Azure'},
    {'quiz': 'sc900-quiz.html',  'json': 'sc900-questions.json',  'name': 'Security Fundamentals',    'short': 'SC-900',  'exam': 'SC-900',  'vendor': 'microsoft', 'tagline': 'Microsoft security, compliance, and identity fundamentals'},
    {'quiz': 'sc300-quiz.html',  'json': 'sc300-questions.json',  'name': 'Identity & Access Admin',  'short': 'SC-300',  'exam': 'SC-300',  'vendor': 'microsoft', 'tagline': 'Microsoft Entra identity and access management'},
    {'quiz': 'dp900-quiz.html',  'json': 'dp900-questions.json',  'name': 'Azure Data Fundamentals',  'short': 'DP-900',  'exam': 'DP-900',  'vendor': 'microsoft', 'tagline': 'Core data concepts on Azure'},
    {'quiz': 'ms900-quiz.html',  'json': 'ms900-questions.json',  'name': 'Microsoft 365 Fundamentals','short': 'MS-900', 'exam': 'MS-900',  'vendor': 'microsoft', 'tagline': 'Microsoft 365 cloud services overview'},
    {'quiz': 'ai900-quiz.html',  'json': 'ai900-questions.json',  'name': 'Azure AI Fundamentals',    'short': 'AI-900',  'exam': 'AI-900',  'vendor': 'microsoft', 'tagline': 'AI and machine learning on Azure'},
    {'quiz': 'ai102-quiz.html',  'json': 'ai102-questions.json',  'name': 'Azure AI Engineer',        'short': 'AI-102',  'exam': 'AI-102',  'vendor': 'microsoft', 'tagline': 'Designing and implementing Azure AI solutions'},

    # ── AWS (8) ──
    {'quiz': 'aws-clf-quiz.html',      'json': 'aws-clf-questions.json',      'name': 'AWS Cloud Practitioner',  'short': 'CLF-C02',  'exam': 'CLF-C02',  'vendor': 'aws',  'tagline': 'The #1 entry-level cloud certification'},
    {'quiz': 'aws-saa-quiz.html',      'json': 'aws-saa-questions.json',      'name': 'AWS Solutions Architect', 'short': 'SAA-C03',  'exam': 'SAA-C03',  'vendor': 'aws',  'tagline': 'The most popular cloud certification globally'},
    {'quiz': 'aws-security-quiz.html', 'json': 'aws-security-questions.json', 'name': 'AWS Security Specialty', 'short': 'SCS-C02',  'exam': 'SCS-C02',  'vendor': 'aws',  'tagline': 'Advanced AWS security services and incident response'},
    {'quiz': 'aws-dva-quiz.html',      'json': 'aws-dva-questions.json',      'name': 'AWS Developer',          'short': 'DVA-C02',  'exam': 'DVA-C02',  'vendor': 'aws',  'tagline': 'AWS application development and deployment'},
    {'quiz': 'aws-soa-quiz.html',      'json': 'aws-soa-questions.json',      'name': 'AWS SysOps Admin',       'short': 'SOA-C02',  'exam': 'SOA-C02',  'vendor': 'aws',  'tagline': 'AWS operations, monitoring, and automation'},
    {'quiz': 'aws-dbs-quiz.html',      'json': 'aws-dbs-questions.json',      'name': 'AWS Database Specialty', 'short': 'DBS-C01',  'exam': 'DBS-C01',  'vendor': 'aws',  'tagline': 'AWS database design, migration, and management'},
    {'quiz': 'aws-mls-quiz.html',      'json': 'aws-mls-questions.json',      'name': 'AWS Machine Learning',   'short': 'MLS-C01',  'exam': 'MLS-C01',  'vendor': 'aws',  'tagline': 'Machine learning solutions on AWS'},
    {'quiz': 'aws-dea-quiz.html',      'json': 'aws-dea-questions.json',      'name': 'AWS Data Engineer',      'short': 'DEA-C01',  'exam': 'DEA-C01',  'vendor': 'aws',  'tagline': 'Data pipeline and analytics engineering on AWS'},

    # ── Google Cloud (5) ──
    {'quiz': 'gcp-ace-quiz.html', 'json': 'gcp-ace-questions.json', 'name': 'Associate Cloud Engineer',       'short': 'ACE',  'exam': 'ACE',  'vendor': 'google-cloud', 'tagline': 'Deploy and manage GCP applications and services'},
    {'quiz': 'gcp-pca-quiz.html', 'json': 'gcp-pca-questions.json', 'name': 'Professional Cloud Architect',   'short': 'PCA',  'exam': 'PCA',  'vendor': 'google-cloud', 'tagline': 'Design and manage GCP solutions architecture'},
    {'quiz': 'gcp-cdl-quiz.html', 'json': 'gcp-cdl-questions.json', 'name': 'Cloud Digital Leader',           'short': 'CDL',  'exam': 'CDL',  'vendor': 'google-cloud', 'tagline': 'Cloud concepts and Google Cloud products'},
    {'quiz': 'gcp-pde-quiz.html', 'json': 'gcp-pde-questions.json', 'name': 'Professional Data Engineer',     'short': 'PDE',  'exam': 'PDE',  'vendor': 'google-cloud', 'tagline': 'Data processing and machine learning on GCP'},
    {'quiz': 'gcp-pse-quiz.html', 'json': 'gcp-pse-questions.json', 'name': 'Professional Security Engineer', 'short': 'PSE',  'exam': 'PSE',  'vendor': 'google-cloud', 'tagline': 'Configuring security on Google Cloud'},

    # ── Cisco (5) ──
    {'quiz': 'ccna-quiz.html',          'json': 'ccna-questions.json',          'name': 'Cisco CCNA',              'short': 'CCNA',    'exam': '200-301',  'vendor': 'cisco', 'tagline': 'Networking fundamentals and Cisco technologies'},
    {'quiz': 'ccnp-quiz.html',          'json': 'ccnp-questions.json',          'name': 'Cisco CCNP ENCOR',        'short': 'ENCOR',   'exam': '350-401',  'vendor': 'cisco', 'tagline': 'Advanced enterprise networking and automation'},
    {'quiz': 'ccnp-security-quiz.html', 'json': 'ccnp-security-questions.json', 'name': 'Cisco CCNP Security SCOR','short': 'SCOR',    'exam': '350-701',  'vendor': 'cisco', 'tagline': 'Cisco network security technologies'},
    {'quiz': 'cyberops-quiz.html',      'json': 'cyberops-questions.json',      'name': 'Cisco CyberOps Associate', 'short': 'CyberOps','exam': '200-201',  'vendor': 'cisco', 'tagline': 'Security operations center fundamentals'},
    {'quiz': 'devnet-quiz.html',        'json': 'devnet-questions.json',        'name': 'Cisco DevNet Associate',   'short': 'DevNet',  'exam': '200-901',  'vendor': 'cisco', 'tagline': 'Network automation and programmability'},

    # ── ISC2 (4) ──
    {'quiz': 'cissp-quiz.html',     'json': 'cissp-questions.json',     'name': 'ISC2 CISSP',  'short': 'CISSP', 'exam': 'CISSP', 'vendor': 'isc2', 'tagline': 'The gold standard for senior security professionals'},
    {'quiz': 'isc2-sscp-quiz.html', 'json': 'isc2-sscp-questions.json', 'name': 'ISC2 SSCP',   'short': 'SSCP',  'exam': 'SSCP',  'vendor': 'isc2', 'tagline': 'Systems security administration and operations'},
    {'quiz': 'isc2-ccsp-quiz.html', 'json': 'isc2-ccsp-questions.json', 'name': 'ISC2 CCSP',   'short': 'CCSP',  'exam': 'CCSP',  'vendor': 'isc2', 'tagline': 'Cloud security architecture and governance'},
    {'quiz': 'isc2-cc-quiz.html',   'json': 'isc2-cc-questions.json',   'name': 'ISC2 CC',     'short': 'CC',    'exam': 'CC',    'vendor': 'isc2', 'tagline': 'Entry-level cybersecurity certification'},

    # ── GIAC (4) ──
    {'quiz': 'gsec-quiz.html', 'json': 'gsec-questions.json', 'name': 'GIAC GSEC',  'short': 'GSEC', 'exam': 'GSEC', 'vendor': 'giac', 'tagline': 'GIAC Security Essentials certification'},
    {'quiz': 'gcih-quiz.html', 'json': 'gcih-questions.json', 'name': 'GIAC GCIH',  'short': 'GCIH', 'exam': 'GCIH', 'vendor': 'giac', 'tagline': 'Incident handling and hacker techniques'},
    {'quiz': 'gpen-quiz.html', 'json': 'gpen-questions.json', 'name': 'GIAC GPEN',  'short': 'GPEN', 'exam': 'GPEN', 'vendor': 'giac', 'tagline': 'Penetration testing methodology'},
    {'quiz': 'gcia-quiz.html', 'json': 'gcia-questions.json', 'name': 'GIAC GCIA',  'short': 'GCIA', 'exam': 'GCIA', 'vendor': 'giac', 'tagline': 'Intrusion analysis and network forensics'},

    # ── EC-Council (3) ──
    {'quiz': 'ceh-quiz.html',  'json': 'ceh-questions.json',  'name': 'EC-Council CEH v13', 'short': 'CEH',  'exam': 'CEH',  'vendor': 'ec-council', 'tagline': 'Certified Ethical Hacker — offensive security fundamentals'},
    {'quiz': 'chfi-quiz.html', 'json': 'chfi-questions.json', 'name': 'EC-Council CHFI v11','short': 'CHFI', 'exam': 'CHFI', 'vendor': 'ec-council', 'tagline': 'Computer hacking forensic investigation'},
    {'quiz': 'cnd-quiz.html',  'json': 'cnd-questions.json',  'name': 'EC-Council CND v3',  'short': 'CND',  'exam': 'CND',  'vendor': 'ec-council', 'tagline': 'Certified network defender'},

    # ── ISACA (3) ──
    {'quiz': 'cism-quiz.html',  'json': 'cism-questions.json',  'name': 'ISACA CISM',  'short': 'CISM',  'exam': 'CISM',  'vendor': 'isaca', 'tagline': 'Certified Information Security Manager for leadership roles'},
    {'quiz': 'cisa-quiz.html',  'json': 'cisa-questions.json',  'name': 'ISACA CISA',  'short': 'CISA',  'exam': 'CISA',  'vendor': 'isaca', 'tagline': 'IT audit, control, and assurance'},
    {'quiz': 'crisc-quiz.html', 'json': 'crisc-questions.json', 'name': 'ISACA CRISC', 'short': 'CRISC', 'exam': 'CRISC', 'vendor': 'isaca', 'tagline': 'Risk and information systems control'},

    # ── OffSec (3) ──
    {'quiz': 'oscp-quiz.html', 'json': 'oscp-questions.json', 'name': 'OffSec OSCP', 'short': 'OSCP', 'exam': 'PEN-200', 'vendor': 'offsec', 'tagline': 'The gold standard for hands-on penetration testing'},
    {'quiz': 'oswa-quiz.html', 'json': 'oswa-questions.json', 'name': 'OffSec OSWA', 'short': 'OSWA', 'exam': 'WEB-200', 'vendor': 'offsec', 'tagline': 'Web application security assessment'},
    {'quiz': 'oswe-quiz.html', 'json': 'oswe-questions.json', 'name': 'OffSec OSWE', 'short': 'OSWE', 'exam': 'WEB-300', 'vendor': 'offsec', 'tagline': 'Advanced web application exploitation'},

    # ── Kubernetes (3) ──
    {'quiz': 'cka-quiz.html',  'json': 'cka-questions.json',  'name': 'Kubernetes CKA',  'short': 'CKA',  'exam': 'CKA',  'vendor': 'kubernetes', 'tagline': 'Certified Kubernetes Administrator'},
    {'quiz': 'ckad-quiz.html', 'json': 'ckad-questions.json', 'name': 'Kubernetes CKAD', 'short': 'CKAD', 'exam': 'CKAD', 'vendor': 'kubernetes', 'tagline': 'Certified Kubernetes Application Developer'},
    {'quiz': 'cks-quiz.html',  'json': 'cks-questions.json',  'name': 'Kubernetes CKS',  'short': 'CKS',  'exam': 'CKS',  'vendor': 'kubernetes', 'tagline': 'Certified Kubernetes Security Specialist'},

    # ── HashiCorp (2) ──
    {'quiz': 'terraform-quiz.html', 'json': 'terraform-questions.json', 'name': 'HashiCorp Terraform', 'short': 'Terraform', 'exam': 'TA-003', 'vendor': 'hashicorp', 'tagline': 'Infrastructure as code with Terraform'},
    {'quiz': 'vault-quiz.html',     'json': 'vault-questions.json',     'name': 'HashiCorp Vault',     'short': 'Vault',     'exam': 'VA-002', 'vendor': 'hashicorp', 'tagline': 'Secrets management and data protection'},

    # ── Specialty (2) ──
    {'quiz': 'ai-security-quiz.html', 'json': 'ai-security-questions.json', 'name': 'AI Security',       'short': 'AI-SEC', 'exam': 'AI-SEC', 'vendor': 'specialty', 'tagline': 'AI/ML security threats and defenses'},
    {'quiz': 'cpts-quiz.html',        'json': 'cpts-questions.json',        'name': 'Hack The Box CPTS', 'short': 'CPTS',   'exam': 'CPTS',   'vendor': 'specialty', 'tagline': 'Hands-on penetration testing across the full kill chain'},
]

# ---------------------------------------------------------------------------
# Vendor Metadata
# ---------------------------------------------------------------------------

VENDOR_META = {
    'comptia': {
        'name': 'CompTIA',
        'icon': '🏆',
        'desc': 'From A+ to CASP+ — the most widely recognized IT certifications worldwide',
        'store_url': '/store/comptia.html',
        'seo_title': 'Free CompTIA Practice Tests',
        'seo_desc': 'Free practice tests for all 14 CompTIA certifications including Security+, Network+, CySA+, PenTest+, CASP+, and more. Domain-weighted questions with explanations.',
        'faq': [
            ('How many CompTIA practice questions are available?', 'We offer practice tests for all 14 CompTIA certifications with questions mapped to every official exam domain. Each quiz includes detailed explanations.'),
            ('Are these official CompTIA practice exams?', 'No. These are independently created practice questions for educational purposes. They cover the same domains as the official exams but are not endorsed by CompTIA.'),
            ('Which CompTIA cert should I start with?', 'Most people start with A+ or Security+. A+ covers IT fundamentals, while Security+ is the most popular entry-level cybersecurity certification. ITF+ is available for complete beginners.'),
            ('Do the quizzes cover the latest exam objectives?', 'Yes. All questions are aligned to the current exam versions including Security+ SY0-701, Network+ N10-009, CySA+ CS0-003, and the new SecAI+ CY0-001.'),
        ],
    },
    'microsoft': {
        'name': 'Microsoft',
        'icon': '🪟',
        'desc': 'Azure, Microsoft 365, and security certifications from fundamentals to expert',
        'store_url': '/store/microsoft.html',
        'seo_title': 'Free Microsoft Certification Practice Tests',
        'seo_desc': 'Free practice tests for 12 Microsoft certifications including AZ-900, AZ-104, AZ-500, SC-900, and more. Domain-weighted with detailed explanations.',
        'faq': [
            ('Which Microsoft cert is best for beginners?', 'AZ-900 (Azure Fundamentals) and SC-900 (Security Fundamentals) are designed for beginners with no prerequisites. MS-900 covers Microsoft 365 basics.'),
            ('Do these cover the latest Microsoft exam updates?', 'Yes. All questions align to current exam objectives. Microsoft updates exams frequently, and our questions reflect the latest domain structure.'),
            ('Are Azure and Microsoft 365 certifications different?', 'Yes. Azure certs (AZ-*) focus on cloud infrastructure and services. Microsoft 365 certs (MS-*) focus on productivity and collaboration. Security certs (SC-*) span both.'),
        ],
    },
    'aws': {
        'name': 'Amazon Web Services',
        'icon': '☁️',
        'desc': 'Cloud Practitioner through Specialty — the most in-demand cloud certifications',
        'store_url': '/store/aws.html',
        'seo_title': 'Free AWS Certification Practice Tests',
        'seo_desc': 'Free practice tests for 8 AWS certifications including Cloud Practitioner, Solutions Architect, Security Specialty, and more. Domain-weighted questions.',
        'faq': [
            ('Which AWS cert should I start with?', 'AWS Cloud Practitioner (CLF-C02) is the recommended starting point. It covers cloud concepts, AWS services, security, and pricing with no prerequisites.'),
            ('How many AWS practice questions do you have?', 'We offer practice tests for 8 AWS certifications spanning foundational, associate, and specialty levels with questions mapped to every exam domain.'),
            ('Are Solutions Architect questions scenario-based?', 'Yes. Our SAA-C03 practice questions include scenario-based questions similar to the actual exam, covering architecture design across all 4 domains.'),
        ],
    },
    'google-cloud': {
        'name': 'Google Cloud',
        'icon': '🌐',
        'desc': 'From Cloud Digital Leader to Professional-level GCP certifications',
        'store_url': '/store/google-cloud.html',
        'seo_title': 'Free Google Cloud Practice Tests',
        'seo_desc': 'Free practice tests for 5 Google Cloud certifications including Associate Cloud Engineer, Professional Cloud Architect, and Security Engineer.',
        'faq': [
            ('Which Google Cloud cert is best for beginners?', 'Cloud Digital Leader (CDL) is the entry-level cert. It covers cloud concepts and GCP products without requiring hands-on experience.'),
            ('Are Professional-level questions harder?', 'Yes. Professional Cloud Architect and Professional Data Engineer questions involve complex scenarios requiring deep GCP knowledge and architecture design skills.'),
        ],
    },
    'cisco': {
        'name': 'Cisco',
        'icon': '🔌',
        'desc': 'CCNA through CCNP — networking and security certifications',
        'store_url': '/store/cisco.html',
        'seo_title': 'Free Cisco Certification Practice Tests',
        'seo_desc': 'Free practice tests for 5 Cisco certifications including CCNA, CCNP Enterprise ENCOR, CCNP Security SCOR, CyberOps, and DevNet.',
        'faq': [
            ('Is CCNA still worth getting?', 'Absolutely. CCNA 200-301 remains one of the most requested networking certifications by employers. It validates foundational networking skills used across all vendors.'),
            ('Should I get CCNP Enterprise or CCNP Security?', 'It depends on your career path. CCNP Enterprise (ENCOR) is for network engineers, while CCNP Security (SCOR) is for security-focused roles. Both start with CCNA.'),
        ],
    },
    'isc2': {
        'name': 'ISC2',
        'icon': '🛡️',
        'desc': 'CISSP, SSCP, CCSP, and CC — the gold standard in cybersecurity',
        'store_url': '/store/security-governance.html',
        'seo_title': 'Free ISC2 Certification Practice Tests',
        'seo_desc': 'Free practice tests for 4 ISC2 certifications including CISSP, SSCP, CCSP, and Certified in Cybersecurity (CC). Domain-weighted questions with explanations.',
        'faq': [
            ('How hard is the CISSP exam?', 'CISSP is considered one of the most challenging cybersecurity exams. It covers 8 domains and uses Computerized Adaptive Testing (CAT). Our practice questions help you prepare for the breadth of topics.'),
            ('What is ISC2 Certified in Cybersecurity (CC)?', 'CC is the entry-level ISC2 certification. It requires no experience and covers security principles, network security, access controls, and incident response. Great stepping stone to CISSP.'),
        ],
    },
    'giac': {
        'name': 'GIAC',
        'icon': '🎖️',
        'desc': 'SANS-affiliated certifications for security professionals',
        'store_url': '/store/security-governance.html',
        'seo_title': 'Free GIAC Certification Practice Tests',
        'seo_desc': 'Free practice tests for 4 GIAC certifications including GSEC, GCIH, GPEN, and GCIA. Questions mapped to SANS course domains.',
        'faq': [
            ('Are GIAC certs worth the investment?', 'GIAC certifications are highly respected in the security industry. They validate hands-on skills and are often required for senior security roles, especially in government and defense.'),
            ('Do I need SANS training to pass GIAC exams?', 'While SANS courses are the recommended preparation, they are not required. Our practice questions cover the same domains and help you identify knowledge gaps.'),
        ],
    },
    'ec-council': {
        'name': 'EC-Council',
        'icon': '🕵️',
        'desc': 'CEH, CHFI, and CND — ethical hacking and forensics certifications',
        'store_url': '/store/offensive-devops.html',
        'seo_title': 'Free EC-Council Practice Tests',
        'seo_desc': 'Free practice tests for 3 EC-Council certifications including CEH v13, CHFI v11, and CND v3. Module-based questions with detailed explanations.',
        'faq': [
            ('Is CEH still relevant?', 'CEH remains one of the most recognized ethical hacking certifications globally. Version 13 includes AI-powered security tools and updated attack techniques.'),
            ('What is the difference between CEH and CHFI?', 'CEH focuses on offensive security (ethical hacking, pen testing), while CHFI focuses on defensive forensics (evidence collection, investigation, analysis).'),
        ],
    },
    'isaca': {
        'name': 'ISACA',
        'icon': '📋',
        'desc': 'CISM, CISA, and CRISC — governance, audit, and risk management',
        'store_url': '/store/security-governance.html',
        'seo_title': 'Free ISACA Certification Practice Tests',
        'seo_desc': 'Free practice tests for 3 ISACA certifications including CISM, CISA, and CRISC. Domain-weighted questions for governance and risk professionals.',
        'faq': [
            ('CISM vs CISSP — which should I get?', 'CISM focuses on security management and governance (management-track), while CISSP covers broader technical security domains. Many senior professionals hold both.'),
            ('Do ISACA exams require work experience?', 'Yes. CISM requires 5 years of security management experience, CISA requires 5 years of audit experience, and CRISC requires 3 years of risk management experience (waivers available).'),
        ],
    },
    'offsec': {
        'name': 'OffSec',
        'icon': '💀',
        'desc': 'OSCP, OSWA, and OSWE — hands-on offensive security certifications',
        'store_url': '/store/offensive-devops.html',
        'seo_title': 'Free OffSec Practice Tests',
        'seo_desc': 'Free practice tests for 3 OffSec certifications including OSCP (PEN-200), OSWA (WEB-200), and OSWE (WEB-300). Concept-check questions for hands-on exam prep.',
        'faq': [
            ('Can practice questions help with the OSCP exam?', 'OSCP is a hands-on practical exam, so lab practice is essential. Our questions test the conceptual knowledge (networking, enumeration, exploitation methodology) needed to succeed in the lab environment.'),
            ('What is the difference between OSWA and OSWE?', 'OSWA (WEB-200) covers web application security assessment fundamentals. OSWE (WEB-300) is advanced — covering source code analysis, custom exploit development, and advanced web attacks.'),
        ],
    },
    'kubernetes': {
        'name': 'Kubernetes',
        'icon': '⚙️',
        'desc': 'CKA, CKAD, and CKS — CNCF Kubernetes certifications',
        'store_url': '/store/offensive-devops.html',
        'seo_title': 'Free Kubernetes Certification Practice Tests',
        'seo_desc': 'Free practice tests for 3 Kubernetes certifications: CKA, CKAD, and CKS. Concept-check questions to complement hands-on lab practice.',
        'faq': [
            ('Are Kubernetes exams performance-based?', 'Yes. CKA, CKAD, and CKS are hands-on exams where you solve problems in a live Kubernetes environment. Our practice questions test the conceptual knowledge that underpins practical skills.'),
            ('Which Kubernetes cert should I get first?', 'CKA (Certified Kubernetes Administrator) is the recommended starting point. CKAD focuses on application development, and CKS covers security — both build on CKA knowledge.'),
        ],
    },
    'hashicorp': {
        'name': 'HashiCorp',
        'icon': '🔐',
        'desc': 'Terraform and Vault certifications for infrastructure and secrets',
        'store_url': '/store/offensive-devops.html',
        'seo_title': 'Free HashiCorp Certification Practice Tests',
        'seo_desc': 'Free practice tests for HashiCorp Terraform Associate and Vault Associate certifications. Questions mapped to official exam objectives.',
        'faq': [
            ('Is Terraform Associate worth getting?', 'Yes. Terraform is the most widely used infrastructure-as-code tool. The certification validates skills that are in high demand for DevOps and cloud engineering roles.'),
            ('What does Vault Associate cover?', 'Vault Associate covers secrets management, encryption, authentication methods, policies, and Vault architecture. It validates skills for managing sensitive data in production environments.'),
        ],
    },
    'specialty': {
        'name': 'Specialty',
        'icon': '🎯',
        'desc': 'AI security and hands-on penetration testing practice',
        'store_url': '/store/store.html',
        'seo_title': 'Free Specialty Cybersecurity Practice Tests',
        'seo_desc': 'Free practice tests for specialty cybersecurity topics including AI security and Hack The Box CPTS certification.',
        'faq': [
            ('What is the AI Security quiz?', 'Our AI Security quiz covers threats to AI/ML systems including model poisoning, adversarial attacks, prompt injection, and AI supply chain security. Great for professionals working with AI systems.'),
            ('What is Hack The Box CPTS?', 'CPTS (Certified Penetration Testing Specialist) is a hands-on certification from Hack The Box that covers the entire penetration testing lifecycle from information gathering through reporting.'),
        ],
    },
}

# Vendor display order (largest first)
VENDOR_ORDER = [
    'comptia', 'microsoft', 'aws', 'google-cloud', 'cisco',
    'isc2', 'giac', 'ec-council', 'isaca', 'offsec',
    'kubernetes', 'hashicorp', 'specialty',
]


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

def load_quiz_data(json_file):
    """Load quiz metadata from JSON file."""
    path = DATA_DIR / json_file
    if not path.exists():
        return None
    with open(path) as f:
        data = json.load(f)
    meta = data.get('metadata', {})
    return {
        'total_questions': meta.get('total_questions', 0),
        'domains': meta.get('domains', {}),
        'domain_count': len(meta.get('domains', {})),
    }


# ---------------------------------------------------------------------------
# HTML Builders
# ---------------------------------------------------------------------------

def build_quiz_card(quiz, data, depth=1):
    """Build a single quiz card HTML."""
    prefix = '../' * depth
    domains_str = ' &bull; '.join(
        esc(d['name']) for d in data['domains'].values()
    ) if data['domains'] else ''

    return f"""        <div class="pt-quiz-card pt-animate">
            <div class="pt-quiz-vendor">{esc(VENDOR_META[quiz['vendor']]['name'])}</div>
            <h3>{esc(quiz['name'])} {esc(quiz['exam'])}</h3>
            <div class="pt-quiz-tagline">{esc(quiz['tagline'])}</div>
            <div class="pt-quiz-stats">
                <span class="pt-quiz-stat"><strong>{data['total_questions']}</strong> questions</span>
                <span class="pt-quiz-stat"><strong>{data['domain_count']}</strong> domains</span>
            </div>
            <div class="pt-quiz-domains">{domains_str}</div>
            <a href="{prefix}{quiz['quiz']}" class="pt-quiz-cta">Start {esc(quiz['short'])} Quiz &rarr;</a>
        </div>"""


def build_vendor_page(vendor_id, quizzes_with_data):
    """Build a complete vendor category page."""
    meta = VENDOR_META[vendor_id]
    today = datetime.now().strftime('%B %-d, %Y')
    today_iso = datetime.now().strftime('%Y-%m-%d')

    total_q = sum(d['total_questions'] for _, d in quizzes_with_data)
    total_domains = sum(d['domain_count'] for _, d in quizzes_with_data)
    quiz_count = len(quizzes_with_data)

    # Build quiz cards
    cards_html = '\n'.join(
        build_quiz_card(q, d, depth=1) for q, d in quizzes_with_data
    )

    # Build related vendors (pick 4 others)
    related = [v for v in VENDOR_ORDER if v != vendor_id][:4]
    related_html = '\n'.join(
        f"""            <a href="{v}.html" class="pt-related-card">
                <div class="pt-related-icon">{VENDOR_META[v]['icon']}</div>
                <div class="pt-related-name">{esc(VENDOR_META[v]['name'])}</div>
            </a>"""
        for v in related
    )

    # Build FAQ
    faq_html = '\n'.join(
        f"""        <details class="pt-faq-item">
            <summary>{esc(q)}</summary>
            <p>{esc(a)}</p>
        </details>"""
        for q, a in meta['faq']
    )

    # Schemas
    breadcrumb = breadcrumb_schema([
        ('Home', f'{SITE_URL}/'),
        ('Practice Tests', f'{SITE_URL}/practice-tests.html'),
        (f'{meta["name"]} Practice Tests', None),
    ])

    item_list = json.dumps({
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'name': f'{meta["name"]} Practice Tests',
        'numberOfItems': quiz_count,
        'itemListElement': [
            {
                '@type': 'ListItem',
                'position': i + 1,
                'name': f'{q["name"]} {q["exam"]} Practice Test',
                'url': f'{SITE_URL}/{q["quiz"]}',
            }
            for i, (q, _) in enumerate(quizzes_with_data)
        ],
    }, indent=8)

    faq_schema_json = faq_schema(meta['faq'])

    canonical = f'{SITE_URL}/practice-tests/{vendor_id}.html'

    content = f"""
    <div class="pt-page">
    <div class="pt-breadcrumb">
        <a href="../practice-tests.html">Practice Tests</a>
        <span class="pt-breadcrumb-sep">/</span>
        {esc(meta['name'])}
    </div>

    <section class="pt-hero pt-animate">
        <div class="pt-hero-badge">{meta['icon']} {esc(meta['name'])} Practice Tests</div>
        <h1>{esc(meta['name'])} Practice Tests</h1>
        <p class="pt-hero-sub">{quiz_count} free practice tests with {total_q:,}+ questions covering every {esc(meta['name'])} certification exam domain.</p>
        <div class="pt-hero-chips">
            <span class="pt-hero-chip">📝 {total_q:,}+ Questions</span>
            <span class="pt-hero-chip">🎯 Domain-Weighted</span>
            <span class="pt-hero-chip">⏱️ Timed Mode</span>
            <span class="pt-hero-chip">📊 Progress Tracking</span>
        </div>
    </section>

    <div class="pt-stats-banner pt-animate pt-delay-1">
        <div class="pt-stat"><div class="pt-stat-value">{quiz_count}</div><div class="pt-stat-label">Practice Tests</div></div>
        <div class="pt-stat"><div class="pt-stat-value">{total_q:,}+</div><div class="pt-stat-label">Questions</div></div>
        <div class="pt-stat"><div class="pt-stat-value">{total_domains}</div><div class="pt-stat-label">Exam Domains</div></div>
    </div>

    <section class="pt-section pt-animate pt-delay-2">
        <h2 class="pt-section-title">All {esc(meta['name'])} Practice Tests</h2>
        <p class="pt-section-subtitle">{esc(meta['desc'])}</p>
        <div class="pt-quiz-grid">
{cards_html}
        </div>
    </section>

    <section class="pt-section">
        <div class="pt-store-cta">
            <h3>Study Planners for {esc(meta['name'])}</h3>
            <p>Pair your practice tests with structured study planners. Domain-by-domain schedules, progress trackers, and exam-day checklists in PDF format.</p>
            <a href="{meta['store_url']}" class="pt-store-cta-btn">Browse {esc(meta['name'])} Planners &rarr;</a>
        </div>
    </section>

    <section class="pt-section">
        <h2 class="pt-section-title">More Practice Tests</h2>
        <div class="pt-related-grid">
{related_html}
        </div>
    </section>

    <section class="pt-faq-section">
        <h2>Frequently Asked Questions</h2>
{faq_html}
    </section>

    <section class="pt-trust-section">
        <div class="pt-trust-grid">
            <div class="pt-trust-item"><div class="pt-trust-icon">🆓</div><div class="pt-trust-label">100% Free</div><div class="pt-trust-desc">No login, no paywall, no ads</div></div>
            <div class="pt-trust-item"><div class="pt-trust-icon">🎯</div><div class="pt-trust-label">Domain-Weighted</div><div class="pt-trust-desc">Questions match official exam weights</div></div>
            <div class="pt-trust-item"><div class="pt-trust-icon">⏱️</div><div class="pt-trust-label">Timed Mode</div><div class="pt-trust-desc">Simulate real exam conditions</div></div>
            <div class="pt-trust-item"><div class="pt-trust-icon">📊</div><div class="pt-trust-label">Progress Tracking</div><div class="pt-trust-desc">Track scores across sessions</div></div>
        </div>
    </section>

    <p class="pt-timestamp">Last updated: {today}</p>

    <p style="text-align:center; margin: 1.5rem 0;"><a href="../practice-tests.html" class="back-link">&larr; Back to All Practice Tests</a></p>
    </div>"""

    theme_js = """
    <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode" title="Toggle dark/light mode">
        <span id="theme-icon">🌙</span>
    </button>
    <script>
    function toggleTheme() {
        var html = document.documentElement;
        var t = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', t);
        localStorage.setItem('fixthevuln-theme', t);
        document.getElementById('theme-icon').textContent = t === 'dark' ? '☀️' : '🌙';
    }
    (function() {
        var s = localStorage.getItem('fixthevuln-theme');
        var d = window.matchMedia('(prefers-color-scheme: dark)').matches;
        var t = s || (d ? 'dark' : 'light');
        if (t === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.getElementById('theme-icon').textContent = '☀️';
        }
    })();
    </script>
    <script src="/js/error-reporter.js"></script>"""

    return page_wrapper(
        title=meta['seo_title'],
        description=meta['seo_desc'],
        canonical=canonical,
        content=content,
        keywords=f'{meta["name"]} practice test, {meta["name"]} mock exam, {meta["name"]} certification quiz, free {meta["name"]} exam questions',
        extra_css=[
            f'practice-tests.css?v={PRACTICE_TESTS_CSS_VERSION}',
        ],
        schema_blocks=[breadcrumb, item_list, faq_schema_json],
        depth=1,
        quiz_disclaimer=meta['name'],
        extra_body_end=theme_js,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    OUT_DIR.mkdir(exist_ok=True)

    # Group quizzes by vendor with loaded data
    vendor_quizzes = {v: [] for v in VENDOR_ORDER}
    skipped = []

    for quiz in QUIZ_REGISTRY:
        data = load_quiz_data(quiz['json'])
        if not data:
            skipped.append(quiz['json'])
            continue
        vendor_quizzes[quiz['vendor']].append((quiz, data))

    if skipped:
        print(f"  Warning: skipped {len(skipped)} missing JSON files: {', '.join(skipped)}")

    # Generate vendor pages
    total_quizzes = 0
    total_questions = 0

    for vendor_id in VENDOR_ORDER:
        quizzes = vendor_quizzes[vendor_id]
        if not quizzes:
            continue

        html = build_vendor_page(vendor_id, quizzes)
        out_path = OUT_DIR / f'{vendor_id}.html'
        with open(out_path, 'w') as f:
            f.write(html)

        q_count = len(quizzes)
        q_total = sum(d['total_questions'] for _, d in quizzes)
        total_quizzes += q_count
        total_questions += q_total
        print(f"  {VENDOR_META[vendor_id]['name']:20s} → {q_count:2d} quizzes, {q_total:,} questions")

    print(f"\n  Total: {len(VENDOR_ORDER)} vendor pages, {total_quizzes} quizzes, {total_questions:,} questions")
    print(f"  Output: {OUT_DIR}/")


if __name__ == '__main__':
    print('Generating practice test vendor pages...\n')
    main()
    print('\nDone.')
