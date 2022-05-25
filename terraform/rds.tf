resource "aws_db_subnet_group" "production" {
  name       = "main"
  subnet_ids = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]
}

resource "aws_db_instance" "production" {
  identifier              = "production"
  name                    = var.rds_db_name
  username                = var.rds_username
  password                = jsondecode(data.aws_secretsmanager_secret_version.secrets.secret_string).rds_password
  port                    = "5432"
  engine                  = "postgres"
  engine_version          = "14.2"
  instance_class          = var.rds_instance_class
  allocated_storage       = "5"
  storage_encrypted       = false
  vpc_security_group_ids  = [aws_security_group.rds.id]
  db_subnet_group_name    = aws_db_subnet_group.production.name
  multi_az                = false
  storage_type            = "gp2"
  publicly_accessible     = false
  backup_retention_period = 2
  skip_final_snapshot     = true
}
