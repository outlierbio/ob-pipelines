output "external_vpc_cidr" {
  value = ["${data.aws_vpc.peering.cidr_block}"]
}
