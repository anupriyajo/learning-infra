resource "random_password" "db_password" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_security_group" "db_security_group" {
  name   = "db-security-group"
  vpc_id = aws_vpc.python-vpc.id

  ingress {
    from_port   = 5432
    protocol    = "tcp"
    to_port     = 5432
    cidr_blocks = [
      "0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    protocol    = -1
    to_port     = 0
    cidr_blocks = [
      "0.0.0.0/0"]
  }
}

resource "aws_db_subnet_group" "db_subnet_group" {
  subnet_ids = aws_subnet.private.*.id
  name       = "db-subnet-group"
}
