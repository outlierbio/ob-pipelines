# Route53 Setup
data "aws_route53_zone" "provided_zone" {
  name         = "${var.lb_route53_zone}"
  private_zone = "${var.lb_internal ? 1 : 0}"
}

resource "aws_lb" "balancer" {

  name     = "${var.lb_name}"
  internal = "${var.lb_internal}"

  ip_address_type    = "${var.lb_ip_address_type}"
  load_balancer_type = "${var.lb_type}"

  security_groups = ["${var.lb_security_groups}"]
  subnets         = ["${var.lb_subnets}"]

  idle_timeout = "${var.lb_idle_timeout}"
  enable_deletion_protection = "${var.lb_deletion_protection}"

  tags = "${var.tags}"
}

resource "aws_route53_record" "instance" {
  count   = "${length(var.lb_route53_records)}"
  zone_id = "${data.aws_route53_zone.provided_zone.zone_id}"
  name    = "${format("%s.%s", replace(element(var.lb_route53_records, count.index), "_", "-"), data.aws_route53_zone.provided_zone.name)}"
  type    = "CNAME"
  ttl     = "300"
  records = ["${element(aws_lb.balancer.*.dns_name, count.index)}"]
}
