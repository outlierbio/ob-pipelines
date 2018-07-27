data "aws_iam_policy_document" "policy" {
  statement {
    actions = [ "sts:AssumeRole" ]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "policy" {
  count  = "${var.iam_policy_name != "" ? 1 : 0 }"
  name   = "${var.iam_policy_name}"
  role   = "${aws_iam_role.role.id}"
  policy ="${var.iam_policy_json}"
}

resource "aws_iam_role" "role" {
  name = "${var.iam_policy_name != "" ?
    var.iam_policy_name : var.default_name}"
  path = "/"
  assume_role_policy = "${data.aws_iam_policy_document.policy.json}"
}

resource "aws_iam_instance_profile" "profile" {
  name = "${aws_iam_role.role.name}"
  role = "${aws_iam_role.role.name}"
}
