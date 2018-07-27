resource "aws_security_group" "public_http" {
  name = "${var.vpc_name}.public.http"
  description = "80 ports access from public web"
  vpc_id = "${var.vpc_id}"

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = "${merge(var.tags, map("Name", format("%s_public_http", var.vpc_name)))}"
}
