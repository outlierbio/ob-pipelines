resource "aws_lb_target_group" "target" {
  vpc_id = "${var.vpc_id}"
  count  = "${length(var.targets)}"
  name   = "${lookup(var.targets[count.index], "name")}"
  port   = "${lookup(var.targets[count.index], "port", var.target_port)}"
  protocol = "${lookup(var.targets[count.index], "protocol",
    var.target_protocol)}"
  target_type = "${lookup(var.targets[count.index], "type",
    var.target_type)}"

  stickiness {
    enabled = "${lookup(var.targets[count.index], "stickiness_enabled",
      var.target_stickiness_enabled)}"
    type = "${lookup(var.targets[count.index], "stickiness_type",
      var.target_stickiness_type)}"
    cookie_duration = "${lookup(var.targets[count.index],
      "stickiness_cookie_duration", var.target_stickiness_cookie_duration)}"
  }

  health_check {
    path = "${lookup(var.targets[count.index], "checker_path",
      var.target_checker_path)}"
    port = "${lookup(var.targets[count.index], "checker_port",
      var.target_checker_port)}"
    protocol = "${lookup(var.targets[count.index], "checker_protocol",
      var.target_checker_protocol)}"
    interval = "${lookup(var.targets[count.index], "checker_interval",
      var.target_checker_interval)}"
    matcher = "${lookup(var.targets[count.index], "checker_matcher",
      var.target_checker_matcher)}"
    timeout = "${lookup(var.targets[count.index], "checker_timeout",
      var.target_checker_timeout)}"
    healthy_threshold = "${lookup(var.targets[count.index],
      "checker_healthy_threshold", var.target_checker_healthy_threshold)}"
    unhealthy_threshold = "${lookup(var.targets[count.index],
      "checker_unhealthy_threshold", var.target_checker_unhealthy_threshold)}"
  }

  deregistration_delay = "${lookup(var.targets[count.index],
    "deregistration_delay", var.target_deregistration_delay)}"

  tags = "${var.tags}"
}
