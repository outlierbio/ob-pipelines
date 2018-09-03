# Route53 Setup
data "aws_route53_zone" "intra" {
  name         = "${var.route53_zone}"
  private_zone = true
}

resource "aws_route53_record" "instance" {
  count   = "${var.number_of_instances}"
  zone_id = "${data.aws_route53_zone.intra.zone_id}"
  name    = "${format("%s-%d.%s.%s",
               replace(var.instance_name, "_", "-"), count.index + 1,
               var.tags["env"], data.aws_route53_zone.intra.name)}"
  type    = "A"
  ttl     = "300"
  records = ["${element(aws_instance.instance.*.private_ip, count.index)}"]
}

# Instance spawn
resource "aws_instance" "instance" {
  ami           = "${var.ami_id}"
  root_block_device {
    volume_type = "${var.root_volume_type}"
    volume_size = "${var.root_volume_size}"
    delete_on_termination = "${var.delete_root_volume_on_termination}"
  }
  count         = "${var.number_of_instances}"
  subnet_id     = "${element(var.subnets, count.index)}"
  instance_type = "${var.instance_type}"
  ebs_optimized = "${var.ebs_optimized}"
  monitoring    = "${var.monitoring}"
# user_data     = "${file(var.user_data)}"  # Temporary disabled as not used
  key_name      = "${var.key_name}"
  vpc_security_group_ids  = ["${var.security_groups}"]
  iam_instance_profile    = "${var.iam_instance_profile}"
  disable_api_termination = "${var.disable_api_termination}"

  tags = "${merge(var.tags, map("Name", format("%s_%s_%d",
  var.tags["env"], var.instance_name, count.index + 1)))}"
}

resource "aws_eip" "elastic_ip" {
  vpc = true

  count = "${var.associate_eip ? var.number_of_instances : 0}"
  instance = "${element(aws_instance.instance.*.id, count.index)}"
}

# EBS
resource "aws_ebs_volume" "instance" {
  availability_zone = "${element(aws_instance.instance.*.availability_zone,
                         count.index)}"
  count = "${var.ext_volume ? var.number_of_instances : 0 }"
  type  = "${var.ext_volume_type}"
  size  = "${var.ext_volume_size}"
  tags  = "${merge(var.tags, map("Name", format("%s_%s_%d",
             var.tags["env"], var.instance_name, count.index + 1)))}"

  # Without this, scaling instances up forces re-mounting of already existing and mounted disks 
  lifecycle {
    ignore_changes = ["volume_id", "instance_id"]
  }
}

resource "aws_volume_attachment" "instance" {
  count = "${var.ext_volume ? var.number_of_instances : 0 }"
  device_name = "/dev/xvdb"
  volume_id   = "${element(aws_ebs_volume.instance.*.id, count.index)}"
  instance_id = "${element(aws_instance.instance.*.id, count.index)}"
}
