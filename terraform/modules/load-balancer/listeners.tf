# Listeners and default target groups
resource "aws_lb_listener" "listener" {

  load_balancer_arn = "${aws_lb.balancer.arn}"

  count    = "${length(var.listeners)}"
  port     = "${lookup(var.listeners[count.index], "port")}"
  protocol = "${lookup(var.listeners[count.index], "certificate", 0) != 0
    ? "HTTPS" : "HTTP"}"

  default_action {
    target_group_arn = "${aws_lb_target_group.target.*.arn[
      index(
        aws_lb_target_group.target.*.name,
        lookup(var.listeners[count.index], "default_target")
      )
    ]}"
    type = "${var.listener_default_action}"
  }

  ssl_policy = "${lookup(var.listeners[count.index], "certificate", 0) != 0
    ? lookup(var.listeners[count.index], "ssl_policy", var.listener_ssl_policy)
    : ""}"
  certificate_arn = "${lookup(var.listeners[count.index], "certificate", "")}"

  depends_on = ["aws_lb_target_group.target"]
}

# Listener custom rules
resource "aws_lb_listener_rule" "listener_rule" {
  count = "${length(var.listener_rules)}"
  listener_arn = "${aws_lb_listener.listener.*.arn[
    index(
      aws_lb_listener.listener.*.port,
      lookup(var.listener_rules[count.index], "port")
    )
  ]}"
  priority = "${lookup(var.listener_rules[count.index], "priority",
    50000 - count.index)}"

  action {
    type             = "${var.listener_rule_action_type}"
    target_group_arn = "${aws_lb_target_group.target.*.arn[
      index(
        aws_lb_target_group.target.*.name,
        lookup(var.listener_rules[count.index], "target_group")
      )
    ]}"
  }

  condition {
    field  = "${lookup(var.listener_rules[count.index], "field")}"
    values = ["${lookup(var.listener_rules[count.index], "values")}"]
  }

  depends_on = ["aws_lb_listener.listener"]
}
