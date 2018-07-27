terraform {
  backend "s3" {
    bucket  = "ob-terraform-states"
    key     = "common.tfstate"
  }
}
