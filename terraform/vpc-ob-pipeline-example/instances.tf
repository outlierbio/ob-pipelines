module "instances_processing_instance_1" {
  source = "../modules/instances"

  number_of_instances = 0

  instance_name = "processing-1"
  instance_type = "t2.nano"
  ami_id        = "ami-14c5486b"
  associate_eip = true
  iam_instance_profile = "default_ob_instances_access"

  root_volume_size = 8

  security_groups = [ "${module.sg.default}", "${module.sg.public_ssh}", "${module.sg.public_web}" ]

  vpc_name = "${var.vpc_name}"
  subnets  = [ "${module.vpc.public_subnets}" ]
  route53_zone = "${var.route53_zone_internal}"
  key_name = "${var.ssh_key_name}"

  tags = "${merge(var.tags, map("env", "ob", "service", "processing"))}"
}
