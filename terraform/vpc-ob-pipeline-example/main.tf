# Region
provider "aws" {
  region  = "${var.aws_region}"
  version = "~> 1.5"
}

# VPC
module "vpc" {
  source = "../modules/vpc"

  name = "${var.vpc_name}"
  cidr = "${var.vpc_main_cidr}"
  azs  = "${var.azs}"

  enable_dns_hostnames = "${var.dns_hostnames}"
  enable_dns_support   = "${var.dns_support}"

  private_subnets = "${var.private_subnets}"
  public_subnets  = "${var.public_subnets}"

  enable_nat_gateway = "${var.nat_gateway}"

  tags = "${var.tags}"
}

# Security Groups
module "sg" {
  source = "../modules/security-groups"

  vpc_id   = "${module.vpc.vpc_id}"
  vpc_name = "${var.vpc_name}"

  tags = "${var.tags}"
}
