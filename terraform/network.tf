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
  tags = {
    Name = "python-private-subnet"
  }
}

resource "aws_subnet" "public" {
  count = var.az_count
  cidr_block = cidrsubnet(aws_vpc.python-vpc.cidr_block, 8, var.az_count + count.index)
  vpc_id = aws_vpc.python-vpc.id
  availability_zone = data.aws_availability_zones.zones.names[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "python-public-subnet"
  }
}

resource "aws_internet_gateway" "python_gateway" {
  vpc_id = aws_vpc.python-vpc.id
  tags = {
    Name = "python-gateway"
  }
}

resource "aws_route" "python_internet_access" {
  route_table_id = aws_vpc.python-vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.python_gateway.id
}

resource "aws_eip" "python_eip" {
  count = var.az_count
  vpc = true
  depends_on = [aws_internet_gateway.python_gateway]
  tags = {
    Name = "python-eip-${data.aws_availability_zones.zones.names[count.index]}"
  }
}