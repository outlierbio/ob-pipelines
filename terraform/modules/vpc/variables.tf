variable "name" {}
variable "cidr" {}

variable "public_subnets" {
  default = []
}

variable "private_subnets" {
  default = []
}

variable "azs" {
  default     = []
  description = "A list of Availability zones in the region"
}

variable "enable_dns_hostnames" {
  default     = true
  description = "should be true if you want to use private DNS within the VPC"
}

variable "enable_dns_support" {
  default     = true
  description = "should be true if you want to use private DNS within the VPC"
}

variable "enable_nat_gateway" {
  default     = false
  description = "should be true if you want to provision NAT Gateways for each of your private networks"
}

variable "map_public_ip_on_launch" {
  default     = true
  description = "should be false if you do not want to auto-assign public IP on launch"
}

variable "private_propagating_vgws" {
  default     = []
  description = "A list of VGWs the private route table should propagate."
}

variable "public_propagating_vgws" {
  default     = []
  description = "A list of VGWs the public route table should propagate."
}

variable "tags" {
  default = {}
}
