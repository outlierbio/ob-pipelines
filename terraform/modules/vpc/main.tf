resource "aws_vpc" "vpc" {
  cidr_block           = "${var.cidr}"
  enable_dns_hostnames = "${var.enable_dns_hostnames}"
  enable_dns_support   = "${var.enable_dns_support}"
  tags                 = "${merge(var.tags, map("Name", format("%s",
                            var.name)))}"
}

resource "aws_internet_gateway" "vpc" {
  vpc_id = "${aws_vpc.vpc.id}"
  tags   = "${merge(var.tags, map("Name", format("%s", var.name)))}"
}

resource "aws_route_table" "public" {
  vpc_id           = "${aws_vpc.vpc.id}"
  propagating_vgws = ["${var.public_propagating_vgws}"]
  tags             = "${merge(var.tags, map("Name", format("%s_public",
                        var.name)))}"
}

resource "aws_route" "public_internet_gateway" {
  route_table_id         = "${aws_route_table.public.id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.vpc.id}"
}

resource "aws_route" "private_nat_gateway" {
  count = "${var.enable_nat_gateway ? 1 : 0}"
  route_table_id         = "${aws_vpc.vpc.main_route_table_id}"
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = "${aws_nat_gateway.natgw.id}"
}

resource "aws_subnet" "private" {
  vpc_id            = "${aws_vpc.vpc.id}"
  cidr_block        = "${var.private_subnets[count.index]}"
  availability_zone = "${element(var.azs, count.index)}"
  count             = "${length(var.private_subnets)}"
  tags              = "${merge(var.tags, map("Name", format("%s_private_%s",
                         var.name, element(var.azs, count.index))))}"
}

resource "aws_subnet" "public" {
  vpc_id                  = "${aws_vpc.vpc.id}"
  cidr_block              = "${var.public_subnets[count.index]}"
  availability_zone       = "${element(var.azs, count.index)}"
  count                   = "${length(var.public_subnets)}"
  map_public_ip_on_launch = "${var.map_public_ip_on_launch}"
  tags                    = "${merge(var.tags, map("Name", format("%s_public_%s",
                                var.name, element(var.azs, count.index))))}"
}

resource "aws_eip" "nateip" {
  count = "${var.enable_nat_gateway ? 1 : 0}"
  vpc        = true
  depends_on = ["aws_internet_gateway.vpc"]
}

resource "aws_nat_gateway" "natgw" {
  count = "${var.enable_nat_gateway ? 1 : 0}"
  allocation_id = "${aws_eip.nateip.id}"
  subnet_id     = "${element(aws_subnet.public.*.id, 0)}"
  depends_on    = ["aws_internet_gateway.vpc"]
  tags          = "${merge(var.tags, map("Name", var.name))}"
}

resource "aws_route_table_association" "private" {
  count          = "${length(var.private_subnets)}"
  subnet_id      = "${element(aws_subnet.private.*.id, count.index)}"
  route_table_id = "${aws_vpc.vpc.main_route_table_id}"
}

resource "aws_route_table_association" "public" {
  count          = "${length(var.public_subnets)}"
  subnet_id      = "${element(aws_subnet.public.*.id, count.index)}"
  route_table_id = "${aws_route_table.public.id}"
}
