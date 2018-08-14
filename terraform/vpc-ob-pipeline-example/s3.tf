
locals {
  source_bucket = "ob-pipelines"
  target_bucket = "outlier-bio"
}

# We don't create the source bucket and instead assume that it is already created
data "aws_s3_bucket" "source_bucket" {
  bucket = "${local.source_bucket}"
}

resource "aws_s3_bucket" "target_bucket" {
  bucket = "${local.target_bucket}"
  acl    = "private"

  tags {
    Name        = "Outlier bio bucket"
    Environment = "outlier-bio"
  }
}


