output "private_subnets" {
  value = ["${aws_subnet.private.*.id}"]
}

output "public_subnets" {
  value = ["${aws_subnet.public.*.id}"]
}

output "vpc_id" {
  value = "${aws_vpc.vpc.id}"
}

output "main_route_table_id" {
  value = "${aws_vpc.vpc.main_route_table_id}"
}

output "public_route_table_id" {
  value = "${aws_route_table.public.id}"
}

output "default_security_group_id" {
  value = "${aws_vpc.vpc.default_security_group_id}"
}
