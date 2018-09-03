resource "aws_default_security_group" "default" {
  vpc_id      = "${var.vpc_id}"

  ingress {
    protocol  = -1
    self      = true
    from_port = 0
    to_port   = 0
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags        = "${merge(var.tags, map("Name", format("%s_default_group", var.vpc_name)))}"
}
