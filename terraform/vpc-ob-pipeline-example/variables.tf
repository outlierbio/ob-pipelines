variable "aws_account_id" {
  default = "469810709223"
}

# VPC general settings
variable "aws_region" {
  default     = "us-east-1"
  description = "A region where the VPC will be located"
}

variable "azs" {
  default = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "vpc_main_cidr" {
  default = "172.5.0.0/16"
}

variable "public_subnets" {
  default = ["172.5.0.0/25","172.5.0.128/25"]
}

variable  "private_subnets" {
  default = [
    "172.5.1.0/25",
    "172.5.1.128/25",
    "172.5.2.0/25"
  ]
}

variable "nat_gateway" {
  default = true
}

variable "route53_zone_external" {
  default     = "bekitzur.com."
  description = "Public zone"
}

variable "route53_zone_internal" {
  default     = "bkz.private."
  description = "Private zone"
}

# This is the convention we use in ECS resources to know what belongs to each other
variable "batch_resources_name" {
  default = "outlier-bio-batch-ecs"
}

# The prefix for names of ECS resources that will be created
variable "batch_ecs_instance_profile" {
  default = "outlier-bio"
}

variable "batch_compute_env_name" {
  default = "test-env"
}

variable "batch_queue_name" {
  default = "test-queue"
}

# VPC additional options
variable "vpc_name" {
  default     = "ob-terraform"
  description = "The VPC name and also prefix for subnet names"
}

variable "dns_support" {
  default = true
}

variable "dns_hostnames" {
  default = true
}

variable "ssh_key_name" {
  default = "bekitzur"
}

variable "tags" {
  description = "A map of tags to be added to all resources"
  default     = { "created_by_terraform" = "true" }
}
