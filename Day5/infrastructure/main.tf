# infrastructure/main.tf
provider "aws" {
  region = "us-east-1"
}

# Public S3 bucket (intentional insecure config for exercise)
resource "aws_s3_bucket" "public_bucket" {
  bucket = "demo-public-bucket-12345"
  acl    = "public-read" # insecure: public read access
}

# Demo RDS instance (publicly accessible) - simplified example
resource "aws_db_instance" "demo_rds" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "demo"
  username             = "admin"
  password             = "insecure-password" # demo only
  skip_final_snapshot  = true
  publicly_accessible  = true # intentional insecure setting
}
