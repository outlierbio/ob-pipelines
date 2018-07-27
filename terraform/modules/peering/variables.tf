variable "external_vpc_id" {}
variable "external_route_table_ids" {
  default = []
}

variable "vpc_name" {}
variable "vpc_id" {}
variable "vpc_cidr" {}
variable "vpc_route_table_ids" {
  default = []
}

variable "tags" {
  default = {}
}
