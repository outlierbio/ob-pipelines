variable "ami_id" {}
variable "instance_name" {}
variable "instance_type" {}

variable "subnets" {
  default     = []
  description = "The VPC subnet the instance(s) will go in"
}

variable "number_of_instances" {
  default = 1
}

variable "security_groups" {
  default     = []
  description = "The VPC security groups the instance(s) will go with"
}

variable "iam_instance_profile" {
  default = "default_instances_access"
}

variable "disable_api_termination" {
  default = false
}

variable "key_name" {}

variable "monitoring" {
  default = false
}

variable "user_data" {
  default     = ""
  description = "The path to a file with user_data for the instances"
}

variable "vpc_name" {}

variable "route53_zone" {
  description = "Zone that used by the VPC"
}

variable "ebs_optimized" {
  default = false
}

variable "root_volume_type" {
  default = "gp2"
}

variable "root_volume_size" {
  default = 8
}

variable "delete_root_volume_on_termination" {
  default = false
}

variable "ext_volume" {
  default = false
}

variable "ext_volume_type" {
  default = "standard"
}

variable "ext_volume_size" {
  default = 10
}

variable "associate_eip" {
  default = false
}

variable "tags" {
  default = {}
}
