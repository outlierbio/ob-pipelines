variable "vpc_id" {}
variable "vpc_name" {}

variable "lb_name" {}

variable "lb_internal" {
  default = "false"
}

# Only applies if youset 'lb_internal' to 'true'
variable "lb_route53_zone" {}
variable "lb_route53_records" {
  default = []
}

variable "lb_type" {
  default = "application"
}

variable "lb_ip_address_type" {
  default = "ipv4"
}

variable "lb_security_groups" {
  default = []
}

variable "lb_subnets" {
  default = []
}

variable "lb_idle_timeout" {
  default = 60
}

variable "lb_deletion_protection" {
  default = true
}

variable "listeners" {
  default = []
}

variable "listener_default_action" {
  default = "forward"
}

variable "listener_ssl_policy" {
  default = "ELBSecurityPolicy-2016-08"
}

variable "listener_rules" {
  default = []
}

variable "listener_rule_action_type" {
  default = "forward"
}

variable "targets" {
  default = []
}

variable "target_port" {
  default = 80
}

variable "target_protocol" {
  default = "HTTP"
}

variable "target_type" {
  default = "instance"
}

variable "target_stickiness_enabled" {
  default = true
}

variable "target_stickiness_type" {
  default = "lb_cookie"
}

variable "target_stickiness_cookie_duration" {
  default = 86400
}

variable "target_checker_path" {
  default = "/health"
}

variable "target_checker_port" {
  default = 80
}

variable "target_checker_protocol" {
  default = "HTTP"
}

variable "target_checker_interval" {
  default = 5
}

variable "target_checker_matcher" {
  default = 200
}

variable "target_checker_timeout" {
  default = 3
}

variable "target_checker_healthy_threshold" {
  default = 2
}

variable "target_checker_unhealthy_threshold" {
  default = 2
}

variable "target_deregistration_delay" {
  default = 300
}

variable "tags" {
  default = {}
}
