provider "vault" {
  address = "https://vault.example.com"
  token   = var.VAULT_TOKEN
}

resource "vault_generic_secret" "example" {
  path = "secret/data/myapp"
}


##Integrated the Vault token into Terraform Enterprise (TFE) pipelines
