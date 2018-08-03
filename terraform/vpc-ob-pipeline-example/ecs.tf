locals {
  name        = "ecs"
  environment = "outlier-bio"

  # This is the convention we use to know what belongs to each other
  ec2_resources_name = "${local.name}-${local.environment}"
}

#----- ECS --------
module "ecs" {
  source = "../modules/ecs"
  name   = "${local.name}"
}

module "ecs-instance-profile" {
  source = "../modules/ecs-instance-profile"
  name   = "${local.name}"
}

#----- ECS  Services--------
module "hello-world" {
  source    = "ecs-services/hello-world"
  cluster_id = "${module.ecs.this_ecs_cluster_id}"
}

#----- ECS  Resources--------
# For now we only use the AWS ECS optimized ami <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>
data "aws_ami" "amazon_linux_ecs" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn-ami-*-amazon-ecs-optimized"]
  }

  filter {
    name   = "owner-alias"
    values = ["amazon"]
  }
}

module "this" {
  source = "../modules/aws-autoscaling"

  name = "${local.ec2_resources_name}"

  # Launch configuration
  lc_name = "${local.ec2_resources_name}"
  associate_public_ip_address = true
  spot_price                  = 0.005

  image_id             = "${data.aws_ami.amazon_linux_ecs.id}"
  instance_type        = "t2.micro"
  security_groups      = [ "${module.sg.default}", "${module.sg.public_ssh}" ]
  iam_instance_profile = "${module.ecs-instance-profile.this_iam_instance_profile_id}"
  user_data            = "${data.template_file.user_data.rendered}"
  key_name             = "${var.ssh_key_name}"

  # Auto scaling group
  asg_name                  = "${local.ec2_resources_name}"
  vpc_zone_identifier       = "${module.vpc.public_subnets}"
  health_check_type         = "EC2"
  min_size                  = 0
  max_size                  = 1
  desired_capacity          = 1
  wait_for_capacity_timeout = 0

  tags = [
    {
      key                 = "Environment"
      value               = "${local.environment}"
      propagate_at_launch = true
    },
    {
      key                 = "Cluster"
      value               = "${local.name}"
      propagate_at_launch = true
    },
  ]
}

data "template_file" "user_data" {
  template = "${file("${path.module}/ecs-templates/user-data.sh")}"

  vars {
    cluster_name = "${local.name}"
  }
}
