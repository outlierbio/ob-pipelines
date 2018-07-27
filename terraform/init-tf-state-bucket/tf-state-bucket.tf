resource "aws_s3_bucket" "tf-state-bucket" {

  #region  = "us-east-1"

  bucket = "ob-terraform-states"
  acl    = "private"
  
  tags {
    Name        = "created_by"
    Environment = "terraform"
  }
}
