## What is this folder for?

This folder contains the Terraform script to create an S3 bucket to keep Terraform states.
Usually, you only need to create Terraform states bucket once and then never change this bucket settings at all, 
so the script here is designed for the once-in-the-life execution.

## How to:

0. Make sure you configured AWS credentials and AWS region: `aws configure`
1. Run `terraform init` and ait for Terraform to download it's plugins
2. Run `terraform apply` 
3. Commit and push the Terraform-generated file `terraform.tfstate` to git

## Known issues:

1. `The authorization header is malformed; the region 'us-east-1' is wrong; expecting 'eu-west-1'`

This error means that the bucket you are trying to create already exists in the 'eu-west-1' region.
The nuance is that S3 bucket names are global across AWS region, so if any other AWS customer already occupied that bucket name you won't be able to create the same bucket in the same region.
This is why the good practice in S3 is to prefix the bucket name with a unique string, such as company name.
