data "aws_availability_zones" "zones" {}

resource "aws_vpc" "python-vpc" {
  cidr_block = "172.17.0.0/16"
  tags = {
    Name = "python-vpc"
  }
}

resource "aws_subnet" "private" {
  count = var.az_count
  cidr_block = cidrsubnet(aws_vpc.python-vpc.cidr_block, 8, count.index)
  vpc_id = aws_vpc.python-vpc.id
  availability_zone = data.aws_availability_zones.zones.names[count.index]
}