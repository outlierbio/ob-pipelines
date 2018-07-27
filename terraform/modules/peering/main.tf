data "aws_vpc" "peering" {
  id = "${var.external_vpc_id}"
}

resource "aws_vpc_peering_connection" "peering" {
  peer_vpc_id   = "${data.aws_vpc.peering.id}"
  vpc_id        = "${var.vpc_id}"
  auto_accept   = true

  accepter {
    allow_remote_vpc_dns_resolution = true
  }

  requester {
    allow_remote_vpc_dns_resolution = true
  }

  tags = "${merge(var.tags, map("Name", format("%s_with_%s",
            var.vpc_name, data.aws_vpc.peering.tags.Name)))}"
}

resource "aws_route" "here2there" {
  count = "${length(var.vpc_route_table_ids)}"
  route_table_id = "${element(var.vpc_route_table_ids, count.index)}"
  destination_cidr_block = "${data.aws_vpc.peering.cidr_block}"
  vpc_peering_connection_id = "${aws_vpc_peering_connection.peering.id}"
}

resource "aws_route" "there2here" {
  count = "${length(var.external_route_table_ids)}"
  route_table_id = "${element(var.external_route_table_ids, count.index)}"
  destination_cidr_block = "${var.vpc_cidr}"
  vpc_peering_connection_id = "${aws_vpc_peering_connection.peering.id}"
}
