# IAM Instance profiles

module "default_instances_access" {
  source = "../modules/iam-instance-profile"

  iam_policy_name = "default_ob_instances_access"

  iam_policy_json = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:GetBucketLocation",
          "s3:ListAllMyBuckets"
        ],
        "Resource": "*"
      }
    ]
}
EOF
}
