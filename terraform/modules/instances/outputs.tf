output "instance_ids" {
  value = ["${aws_instance.instance.*.id}"]
}

output "number_of_instances" {
  value = "${var.number_of_instances}"
}
