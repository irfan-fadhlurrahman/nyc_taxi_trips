# Terraform

Install terraform on a local machine to create Google Cloud Storage Bucket and BigQuery.

## Setup
1. Google service account in .json format
2. Assign IAM roles to this service account
    * Storage Admin
    * Storage Object Admin
    * BigQuery Admin
    * Viewer
3. Assign environment variables to bashrc
```
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/authkeys>.json"
```
4. Refresh authentication
```
gcloud auth application-default login
```
5. Install Terraform.
```
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

Notes: Go to the directory that contains main.tf and variables.tf before using terraform.

## Initialization
```
terraform init
```

## Dry-run
To ensure services are correctly configured.
```
terraform plan
```

## Run
```
terraform apply
```

## Destroy
```
terraform destroy
```
