resource "aws_security_group" "public_ssh" {
  name        = "${var.vpc_name}.public.ssh"
  description = "SSH access form public web"
  vpc_id      = "${var.vpc_id}"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = "${merge(var.tags, map("Name", format("%s_public_ssh", var.vpc_name)))}"
}
