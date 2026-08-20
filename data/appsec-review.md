# FixTheVuln AppSec Review

- **Date:** 2026-08-20
- **Reviewer:** Robert Flores, CISSP (FixTheVuln AppSec Reviewer)
- **CVEs reviewed:** 1
- **Approved for publication:** 1

## Severity breakdown

| Priority | Count |
|----------|-------|
| Critical | 1 |
| High     | 0 |
| Medium   | 0 |
| Low      | 0 |

## Per-CVE summary

| CVE | Vendor / Product | Priority | Vulnerability class |
|-----|------------------|----------|---------------------|
| CVE-2026-64849 | MLflow / MLflow | critical | Server-Side Request Forgery (CWE-918) |

## Trend analysis

This cycle's single addition continues a pattern seen across 2025–2026 KEV entries: AI/ML platform components (model registries, tracking servers, notebook backends) increasingly appear alongside traditional enterprise gear. MLflow is exposed on internal networks in the majority of MLOps deployments and, as here, an unauthenticated SSRF that can reach cloud metadata endpoints converts a "developer tool" into a direct path to IAM credential theft. The CVSS 9.3 rating and CISA's inclusion under BOD 26-04 reflect confirmed in-the-wild exploitation, and the pattern echoes prior KEV additions for Ray, Jupyter, and Kubeflow — attackers are prioritizing the ML supply chain because compensating controls (network segmentation, IMDSv2, egress filtering) are often absent on infrastructure that was originally scoped as "internal only."

## Blog post candidates

1. **"SSRF-to-IAM: Why MLflow's CVE-2026-64849 is a Cloud Credential Heist Waiting to Happen"** — technical walkthrough of the SSRF payload, IMDSv1/v2 behavior, and the AWS/GCP/Azure metadata endpoints that turn a webhook bug into a role-assumption chain.
2. **"MLOps on the KEV: A Field Guide to Securing MLflow, Ray, and Kubeflow"** — practitioner-focused hardening playbook covering network policies, IMDSv2 enforcement, egress allowlists, and authentication gateways.
3. **"BOD 26-04 in Practice: Prioritizing ML Platform Patches for Federal and Regulated Environments"** — how to map CISA's new directive to internal ML infrastructure, including forensics triage requirements.

## Newsletter snippet

**MLflow SSRF joins the KEV — treat it as a cloud credential incident, not a "dev tool" bug.** CISA added CVE-2026-64849 to the Known Exploited Vulnerabilities catalog this week, an unauthenticated server-side request forgery (CVSS 9.3) in MLflow that lets an attacker force the server to fetch arbitrary URLs and read back status and body. On any MLflow instance running in AWS, GCP, or Azure without IMDSv2 or egress restrictions, that primitive is enough to pull instance role credentials, service-account tokens, or Kubernetes metadata — a direct path from an "internal ML tool" to full cloud role assumption. The federal remediation deadline under BOD 26-04 is 2026-09-02.

If you run MLflow anywhere, patch to the fixed release referenced in MLflow PR #24258 immediately. In parallel, verify IMDSv2 is enforced on every host that runs a tracking server, apply egress allowlists so the server cannot reach 169.254.169.254 or internal-only ranges, and audit CloudTrail / audit logs for anomalous role-assumption or metadata calls originating from MLflow subnets. Given the ransomware status is "Unknown," assume active exploitation and prioritize this alongside your standard critical-patch workflow — the full technical write-up and remediation checklist is live now at fixthevuln.com.
