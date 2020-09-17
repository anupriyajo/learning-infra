data "aws_availability_zones" "zones" {}

resource "aws_vpc" "python-vpc" {
  cidr_block = "172.17.0.0/16"
  tags = {
    Name = "python-vpc"
  }
}