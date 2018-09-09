
locals {
  source_bucket = "${var.source_bucket_name}"
  target_bucket = "${var.target_bucket_name}"
}

resource "aws_s3_bucket" "source_bucket" {
  bucket = "${local.source_bucket}"
  acl    = "private"

  tags {
    Name        = "Outlier bio source bucket"
    Environment = "${var.batch_compute_env_name}"
  }
}


resource "aws_s3_bucket" "target_bucket" {
  bucket = "${local.target_bucket}"
  acl    = "private"

  tags {
    Name        = "Outlier bio target bucket"
    Environment = "${var.batch_compute_env_name}"
  }
}


