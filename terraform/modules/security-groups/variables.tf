variable "vpc_id" {}
variable "vpc_name" {}

variable "allowed_cidrs" {
  default     = []
  description = "The source CIDR block to allow traffic from"
}

variable "tags" {
  default = {}
}
