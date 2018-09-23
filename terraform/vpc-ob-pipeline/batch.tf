module "ecs-instance-profile" "batch-ecs-instance-profile" {
  source = "../modules/ecs-instance-profile"
  name   = "${var.batch_ecs_instance_profile}"
}

resource "aws_iam_policy" "iam_policy_batch_ecr_role_grant_s3_access" {
  name        = "outlier-bio-aws-batch-s3-access"
  description = "Allow ECS spot instances created by AWS Batch to access outlier-bio S3 buckets"
  policy      =  <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "S3ListAllMyBucketsAccessForSourceAndTargetBucket",
    "Effect": "Allow",
    "Action": [ "s3:ListAllMyBuckets" ],
    "Resource": "*"
  }, {
    "Sid": "S3ReadAccessForSourceBucket",
    "Effect": "Allow",
    "Action": [ "s3:*" ],
    "Resource": [
      "${aws_s3_bucket.source_bucket.arn}",
      "${aws_s3_bucket.source_bucket.arn}/*"
    ]
  }, {
    "Sid": "S3RWAccessForTargetBucket",
    "Effect": "Allow",
    "Action": [ "s3:*" ],
    "Resource": [
      "${aws_s3_bucket.target_bucket.arn}",
      "${aws_s3_bucket.target_bucket.arn}/*"
    ]
  }, {
    "Sid": "ECRReadOnlyAccessForImagesPull",
    "Effect": "Allow",
    "Action": [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:GetRepositoryPolicy",
      "ecr:DescribeRepositories",
      "ecr:ListImages",
      "ecr:DescribeImages",
      "ecr:BatchGetImage"
     ],
    "Resource": [ "*" ]
  }]
}
EOF
}

resource "aws_iam_policy_attachment" "iam_policy_batch_ecr_role_grant_s3_access_attachment" {
  name       = "iam-policy-batch-ecr-role-grant-s3-access-attachment"
  roles      = [ "${module.ecs-instance-profile.instance_role_name}" ]
  policy_arn = "${aws_iam_policy.iam_policy_batch_ecr_role_grant_s3_access.arn}"
}

resource "aws_batch_compute_environment" "test_environment_1" {
  compute_environment_name = "${var.batch_compute_env_name}"
  service_role = "arn:aws:iam::${var.aws_account_id}:role/service-role/AWSBatchServiceRole"
  type = "UNMANAGED"
}

resource "aws_batch_job_queue" "test_queue_1" {
  name = "${var.batch_queue_name}"
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

  name = "${var.batch_resources_name}"

  # Launch configuration
  lc_name = "${var.batch_resources_name}"
  associate_public_ip_address = true
  spot_price                  = 1.0

  image_id             = "ami-00129b193dc81bc31"
  instance_type        = "m4.10xlarge" # "x1e.2xlarge", "m5.12xlarge", "c5.18xlarge"
  security_groups      = [ "${module.sg.default}", "${module.sg.public_ssh}" ]
  iam_instance_profile = "${module.ecs-instance-profile.instance_profile_id}"
  user_data            = "${data.template_file.user_data_batch_1.rendered}"
  key_name             = "${var.ssh_key_name}"

  # Auto scaling group
  asg_name                  = "${var.batch_resources_name}"
  vpc_zone_identifier       = "${module.vpc.public_subnets}"
  health_check_type         = "EC2"
  min_size                  = 0
  max_size                  = 1
  desired_capacity          = 1 # Please set to 1 and re-apply when you need to start Luigi
  wait_for_capacity_timeout = 0

  tags = [{
    key                 = "Environment"
    value               = "main"
    propagate_at_launch = true
  }, {
    key                 = "Cluster"
    value               = "outlier-bio"
    propagate_at_launch = true
  }]
}

resource "aws_autoscaling_policy" "batch-asg-scaling-out-policy" {
  name                   = "${var.batch_resources_name}-scaling-out-by-cpu"

  policy_type = "TargetTrackingScaling"

  adjustment_type        = "ChangeInCapacity"
  autoscaling_group_name = "${module.autoscaling.this_autoscaling_group_name}"
 
  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 3.0
    disable_scale_in = true
  }

}
