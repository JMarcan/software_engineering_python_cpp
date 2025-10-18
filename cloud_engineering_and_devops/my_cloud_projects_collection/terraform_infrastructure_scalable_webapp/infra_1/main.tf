# Designate a cloud provider, region, and credentials
provider "aws" {
    profile = "default"
    region = "us-east-1"
}

# provision 4 AWS t2.micro EC2 instances named Udacity T2
resource "aws_instance" "udacity_t2" {
  count = "4"
  ami = "ami-00a205cb8e06c3c4e"
  instance_type = "t2.micro"
  subnet_id = "subnet-037f2a86a4dda95fb"
  tags = {
    name = "AWS Architect P2"
  }
}

# provision 2 m4.large EC2 instances named Udacity M4
resource "aws_instance" "udacity_m4" {
  count = "2"
  ami = "ami-00a205cb8e06c3c4e"
  instance_type = "m4.large"
  subnet_id = "subnet-037f2a86a4dda95fb"
  tags = {
    name = "AWS Architect P2"
  }
}
