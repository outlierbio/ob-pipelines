terraform {
  backend "s3" {
    bucket  = "ob-terraform-states"
    key     = "vpc-ob-pipeline-example.tfstate"
  }
}
