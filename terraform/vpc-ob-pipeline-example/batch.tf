locals {

  # This is the convention we use to know what belongs to each other
  batch_resources_name = "outlier-bio-batch-ecs"
  
  # The names of resources that will be created
  batch_ecs_instance_profile = "batch-ecs-instance-profile"
  batch_compute_env_name = "test-env" 
  batch_queue_name = "test-queue"
}

module "ecs-instance-profile" "batch-ecs-instance-profile" {
  source = "../modules/ecs-instance-profile"
  name   = "${local.batch_ecs_instance_profile}"
}

resource "aws_iam_policy" "iam_policy_batch_ecr_role_grant_s3_access" {
  name        = "outlier-bio-aws-batch-s3-access"
  description = "Allow ECS spot instances created by AWS Batch to access outlier-bio S3 buckets"
  policy      =  <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "S3ReadAccessForSourceBucket",
    "Effect": "Allow",
    "Action": [
       "s3:GetObject",
       "s3:GetObjectAcl"
    ],
    "Resource": [ "${data.aws_s3_bucket.source_bucket.arn}" ]
  }]
}
EOF
}

resource "aws_iam_policy_attachment" "iam_policy_batch_ecr_role_grant_s3_access-attachment" {
  name       = "lambda-sns-alerts-policy-attachment"
  roles      = [ "${module.ecs-instance-profile.instance_profile_name}" ]
  policy_arn = "${aws_iam_policy.iam_policy_batch_ecr_role_grant_s3_access.arn}"
}

resource "aws_batch_compute_environment" "test_environment_1" {
  compute_environment_name = "${local.batch_compute_env_name}"
  service_role = "arn:aws:iam::469810709223:role/service-role/AWSBatchServiceRole"
  type = "UNMANAGED"
}

resource "aws_batch_job_queue" "test_queue_1" {
  name = "${local.batch_queue_name}"
  state = "ENABLED"
  priority = 1
  compute_environments = [ "${aws_batch_compute_environment.test_environment_1.arn}" ]
}

data "template_file" "user_data_batch_1" {
  template = "${file("${path.module}/ecs-templates/user-data.sh")}"

  vars {
    cluster_name = "${aws_batch_compute_environment.test_environment_1.ecs_cluster_arn}"
  }
}

module "autoscaling" "ecs_instances" {
  source = "../modules/aws-autoscaling"

  name = "${local.batch_resources_name}"

  # Launch configuration
  lc_name = "${local.batch_resources_name}"
  associate_public_ip_address = true
  spot_price                  = 1.5

  image_id             = "ami-644a431b"
  instance_type        = "x1e.2xlarge"
  security_groups      = [ "${module.sg.default}", "${module.sg.public_ssh}" ]
  iam_instance_profile = "${module.ecs-instance-profile.instance_profile_id}"
  user_data            = "${data.template_file.user_data_batch_1.rendered}"
  key_name             = "${var.ssh_key_name}"

  # Auto scaling group
  asg_name                  = "${local.batch_resources_name}"
  vpc_zone_identifier       = "${module.vpc.public_subnets}"
  health_check_type         = "EC2"
  min_size                  = 0
  max_size                  = 1
  desired_capacity          = 1
  wait_for_capacity_timeout = 0

  tags = [{
    key                 = "Environment"
    value               = "main"
    propagate_at_launch = true
  },
  {
    key                 = "Cluster"
    value               = "outlier-bio"
    propagate_at_launch = true
  }]
}
