# Terraform with Jenkins Pipeline Integration

This project automates the provisioning of AWS infrastructure using **Terraform** **Pyhton** in combination with **Jenkins** pipelines. The solution integrates with **HashiCorp Vault** to securely manage and retrieve access keys and secret credentials for the target AWS accounts.

## Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Pipeline Steps](#pipeline-steps)
- [Setup](#setup)
- [Usage](#usage)


## Overview

This project aims to streamline the infrastructure management process by automating the provisioning of AWS resources using Terraform, Jenkins pipelines, and Vault for secure credential management. It dynamically passes parameters to Terraform, integrates Vault tokens for secure authentication, and retrieves AWS credentials securely from Vault using Python scripts.

## Technologies Used

- **Terraform**: For infrastructure provisioning and management.
- **Jenkins**: For CI/CD pipeline orchestration.
- **Vault**: For managing sensitive secrets like AWS credentials.
- **AWS**: For cloud infrastructure.
- **Python**: For scripting the retrieval of credentials from Vault.
- **Git**: For source control.

## Pipeline Steps

1. **Jenkins Pipeline Setup**:
   - Defines a Jenkins pipeline to automate the steps required to provision infrastructure.
   - Uses Jenkins parameters to pass dynamic values like AWS account ID, Terraform version, etc.

2. **Vault Integration**:
   - Vault tokens are used to authenticate and retrieve secrets from Vault.
   - Securely retrieves AWS credentials (Access Key and Secret Key) using Python scripts integrated into the pipeline.

3. **Terraform Execution**:
   - Terraform is initialized (`terraform init`), validated (`terraform validate`), and the infrastructure plan is created (`terraform plan`).
   - Upon approval, changes are applied to AWS using `terraform apply`.

4. **Secure Secrets Management**:
   - Vault is used to securely store and manage the Vault access tokens, ensuring that sensitive information is never exposed in plain text.

## Setup

To run the pipeline, ensure you have the following prerequisites:

### Prerequisites

- **Terraform** installed on the machine.
- **Jenkins** set up with a working pipeline.
- **HashiCorp Vault** configured to manage AWS credentials.
- **AWS CLI** installed and configured with access to the target AWS accounts.
- **Python** installed for running Vault integration scripts.

### Installation Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/terraform-jenkins-vault-integration.git
    ```

2. Configure your Vault server with the necessary AWS access credentials.
3. Set up the Jenkins pipeline:
   - Define Jenkins environment variables for Vault tokens and other parameters.
   - Install the necessary Jenkins plugins (e.g., Terraform, AWS, Python).

4. Configure your Terraform files (`main.tf`, `variables.tf`, etc.) to reflect the AWS infrastructure you wish to provision.

## Usage

1. Once the Jenkins pipeline is triggered (e.g., on a code push or manual trigger), it will execute the following steps:
   - Fetch Vault credentials using the Python script.
   - Use Terraform to create or update the AWS infrastructure.
   
2. The pipeline will output the results of `terraform plan` and prompt for manual approval before applying changes with `terraform apply`.



