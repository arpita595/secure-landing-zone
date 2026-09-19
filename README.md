# Secure Cloud Landing Zone (IaC & DevSecOps)

![Terraform](https://img.shields.io/badge/Terraform-1.5+-844FBA?style=for-the-badge&logo=terraform&logoColor=white)
![LocalStack](https://img.shields.io/badge/LocalStack-AWS_Emulated-000000?style=for-the-badge&logo=localstack&logoColor=00E5FF)
![Security Scanning](https://img.shields.io/badge/Checkov-Passed-success?style=for-the-badge&logo=bridgecrew&logoColor=white)
![CI/CD](https://img.shields.io/badge/GitHub_Actions-Automated-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

An enterprise-grade, zero-cost AWS Secure Landing Zone built with **Terraform**, emulated locally via **LocalStack**, and secured using Policy-as-Code (**Checkov** + **tfsec**) with GitHub Actions CI/CD.

---

## Architecture Overview
```text
                           Internet
                              │
                    ┌─────────┴─────────┐
             [ Internet Gateway / EIP ]
                    └─────────┬─────────┘
                              │
           ┌──────────────────┴──────────────────┐
           │            Dev VPC (10.0.0.0/16)    │
           │                                     │
           │  ┌───────────────────────────────┐  │
           │  │ Public Subnets (AZ1 / AZ2)    │  │
           │  │  • NAT Gateway                │  │
           │  │  • Bastion SG (SSH Restricted)│  │
           │  └───────────────┬───────────────┘  │
           │                  │                  │
           │  ┌───────────────▼───────────────┐  │
           │  │ Private Subnets (AZ1 / AZ2)   │  │
           │  │  • Isolated Workloads         │  │
           │  └───────────────────────────────┘  │
           └─────────────────────────────────────┘
```

## Key Highlights & Architecture Features
* Modular Infrastructure-as-Code: Reusable Terraform network modules featuring multi-AZ VPC segmentation, public/private subnets, NAT Gateways, and strict Security Groups.

* Keyless OIDC Identity Federation: Configured OpenID Connect (oidc.tf) between GitHub Actions and AWS IAM, eliminating long-lived static AWS credentials in CI/CD pipelines.

* Policy-as-Code Guardrails: Automated pre-deployment security scanning using Checkov and tfsec directly in GitHub Actions to block misconfigured resources before deployment.

* Zero Cloud Expense: Entire stack runs locally on Docker via LocalStack, delivering 1:1 AWS API emulation without cloud charges.

* Remote State Management: Configured S3 remote state backend with DynamoDB locking emulated in LocalStack to handle state locking and collaboration patterns.

---

## Repository Structure
```text
.
├── .github/
│   └── workflows/
│       └── terraform.yml          # GitHub Actions CI/CD Pipeline
├── envs/
│   └── dev/
│       ├── main.tf                # Dev environment module instantiation
│       ├── oidc.tf                # GitHub Actions OIDC Trust Role & Provider
│       ├── backend.tf             # LocalStack S3 + DynamoDB state backend
│       └── variables.tf           # Input definitions
├── modules/
│   └── network/                   # Reusable Network Module (VPC, Subnets, Route Tables)
└── README.md
```
---

## Local Development & Testing
### Prerequisites
* Docker Desktop
* HashiCorp Terraform CLI
* tflocal (pip install terraform-local)
* AWS CLI

1. Start LocalStack
```bash
docker run -d -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack
```

2. Initialize and Deploy Stack
```bash
cd envs/dev
tflocal init
tflocal apply -var="admin_ip_cidr=10.0.0.1/32"
```

3. Run Local Security Audit
```bash
checkov -d .
tfsec .
```

## Security & CI/CD Pipeline Flow

1. Pull Request Trigger: Any branch push triggers automated Checkov and tfsec static code scans.

2. Scan Gates: Scans run in parallel. Non-compliant configurations block downstream deployment jobs.

3. Plan Generation: If security scans pass, GitHub Actions initializes LocalStack and generates a terraform plan.

4. Automated Feedback: Compliance and scan summaries are automatically commented onto the Pull Request.
   
