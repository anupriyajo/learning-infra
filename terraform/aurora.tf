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

resource "aws_rds_cluster" "db_cluster" {
  cluster_identifier     = "db-cluster"
  database_name          = "customers"
  engine                 = "aurora-postgresql"
  master_username        = "py"
  master_password        = random_password.db_password.result
  vpc_security_group_ids = [
    aws_security_group.db_security_group.id]
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name
  skip_final_snapshot    = true
}

resource "aws_rds_cluster_instance" "db_instance" {
  cluster_identifier = aws_rds_cluster.db_cluster.id
  instance_class     = "db.t3.medium"
  identifier         = "${aws_rds_cluster.db_cluster.cluster_identifier}-identifier"
  engine             = aws_rds_cluster.db_cluster.engine
  engine_version     = aws_rds_cluster.db_cluster.engine_version
}
