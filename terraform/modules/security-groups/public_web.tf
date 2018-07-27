resource "aws_security_group" "public_web" {
  name = "${var.vpc_name}.public.web"
  description = "A set of ports to access from public web"
  vpc_id = "${var.vpc_id}"

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = "${merge(var.tags, map("Name", format("%s_public_web", var.vpc_name)))}"
}
