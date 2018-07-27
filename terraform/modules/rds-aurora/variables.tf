# DB name (this is NOT the RDS name in AWS RDS Console!)
variable "name" {}

# DB storage size to allocate in gigabytes
variable "allocated_storage" {}

# DB storage type ('gp2', 'io1', 'standard', etc)
#variable "storage_type" {
#  default = "gp2"
#}

variable "engine" {
  description = "DB engine. Supported values are: 'aurora', 'aurora-postgresql', 'mariadb', 'mysql', 'oracle-ee', 'oracle-se2', 'oracle-se1', 'oracle-se', 'postgres', 'sqlserver-ee', 'sqlserver-se', 'sqlserver-ex', 'sqlserver-web'"
}

# DB instance class. Examples: 'db.t1.micro', 'db.t1.large
variable "instance_class" {}

# DB user to create. Defaults to DB engine name, i.e. for mysql it will be 'mysql', for postgres - 'postgres', and so on
variable "username" {
  default = "admin"
}

# DB user password
variable "password" {}

# DB subnet group. By default, the default subnet group is used.
variable "subnet_group_name" {
  default = "default"
}

# DB subnet group. By default, the default subnet group is used.
variable "parameter_group_name" {}

# Should the DB be publically accessible
variable "publicly_accessible" {
  default = false
}

# Should the DB internal storage be encrypted. If true, AWS uses AES256 encryption to protect DB EBS volumes
variable "storage_encrypted" {
  default = true
}

# On delete, copy all Instance tags to the final snapshot
variable "copy_tags_to_snapshot" {
  default = true
}

# The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB instance. 
# To disable collecting Enhanced Monitoring metrics, specify 0. The default is 0. 
# Valid Values: 0, 1, 5, 10, 15, 30, 60.
variable "monitoring_interval" {}

# Determines whether a final DB snapshot is created before the DB instance is deleted. 
# If true is specified, no DBSnapshot is created. If false is specified, a DB snapshot is created before the DB instance is deleted, using the value from final_snapshot_identifier. 
variable "skip_final_snapshot" {
  default = true
}

# Indicates that minor engine upgrades will be applied automatically to the DB instance during the maintenance window.
variable "auto_minor_version_upgrade" {
  default = false
}
