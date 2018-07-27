resource "aws_rds_cluster" "default" {
  cluster_identifier      = "${var.name}"
  engine                  = "aurora-mysql"
  availability_zones      = ["us-east-1a", "us-east-1b"]
  database_name           = "fandomedev"
  master_username         = "${var.username}"
  master_password         = "${var.password}"
  backup_retention_period = 5
  preferred_backup_window = "07:00-09:00"
}
