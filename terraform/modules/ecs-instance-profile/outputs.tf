output "instance_profile_id" {
  value = "${aws_iam_instance_profile.this.id}"
}

output "instance_profile_name" {
  value = "${aws_iam_instance_profile.this.name}"
}
