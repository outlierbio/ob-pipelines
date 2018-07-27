
## Example of ALB load labalncer
#module "alb-example" {
#  source = "../modules/load-balancer"
#
#  vpc_id   = "${module.vpc.vpc_id}"
#  vpc_name = "${var.vpc_name}"
#
#  lb_name = "dev-back-and-front"
#
#  lb_route53_zone = "${var.route53_zone_external}"
#  lb_route53_records = []
#
#  lb_deletion_protection = false
#
#  lb_security_groups = [ "${module.sg.default}", "${module.sg.public_web}" ]
#
#  lb_subnets = "${module.vpc.public_subnets}"
#
#  # Balancer inbound traffic
#  listeners = [{
#    "port"           = "80",
#    "default_target" = "no-op"
#  }]
#
#  # Traffic flow rules
#  listener_rules = []
#
#  # Target groups == rules how should balancer send traffic to the instance port(s)
#  targets = [{
#     "name" = "dev-pipeline-ui",
#     "port" = "80",
#     "checker_path" = "/health"
#    },
#    {
#     "name" = "no-op",
#     "port" = "80",
#     "checker_path" = "/"
#  }]
#
#  tags = "${var.tags}"
#}
