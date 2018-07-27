resource "aws_security_group" "public_https" {
  name = "${var.vpc_name}.public.https"
  description = "443 ports access from public web"
  vpc_id = "${var.vpc_id}"

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = "${merge(var.tags, map("Name", format("%s_public_https", var.vpc_name)))}"
}
