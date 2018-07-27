variable "route53_zone" {
  description = "Zone that used by the VPC"
}

variable "name" {}
variable "records" {
  default = []
}

variable "type" {
  default = "A"
}

variable "ttl" {
  default = 300
}
