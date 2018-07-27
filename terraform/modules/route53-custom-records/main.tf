data "aws_route53_zone" "krypton" {
  name         = "${var.route53_zone}"
  private_zone = true
}

resource "aws_route53_record" "instance" {
  zone_id = "${data.aws_route53_zone.krypton.zone_id}"
  name    = "${var.name}"
  type    = "${var.type}"
  ttl     = "${var.ttl}"
  records = ["${var.records}"]
}
