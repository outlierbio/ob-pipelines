resource "aws_db_instance" "rds_db_default" {
  name                       = "${var.name}"
  identifier                 = "${var.identifier}"
  publicly_accessible        = "${var.publicly_accessible}"
  allocated_storage          = "${var.allocated_storage}"
  storage_type               = "${var.storage_type}"
  engine                     = "${var.engine}"
  engine_version             = "${var.engine_version}"
  instance_class             = "${var.instance_class}"
  username                   = "${var.username}"
  password                   = "${var.password}"
  db_subnet_group_name       = "${var.subnet_group_name}"
  parameter_group_name       = "${var.parameter_group_name}"
  storage_encrypted          = "${var.storage_encrypted}"
  copy_tags_to_snapshot      = "${var.copy_tags_to_snapshot}"
  monitoring_interval        = "${var.monitoring_interval}"
  skip_final_snapshot        = "${var.skip_final_snapshot}"
  auto_minor_version_upgrade = "${var.auto_minor_version_upgrade}"
  auto_minor_version_upgrade = "${var.auto_minor_version_upgrade}"
  vpc_security_group_ids     = "${var.vpc_security_group_ids}"
  backup_retention_period    = "${var.backup_retention_period}"
}


# Route53 Setup
data "aws_route53_zone" "intra" {
  name         = "${var.route53_zone}"
  private_zone = true
}

resource "aws_route53_record" "internal_dns" {
  zone_id = "${data.aws_route53_zone.intra.zone_id}"
  name    = "${var.engine}-${var.identifier}"
  type    = "CNAME"
  ttl     = "300"
  records = [ "${aws_db_instance.rds_db_default.address}" ]
}
