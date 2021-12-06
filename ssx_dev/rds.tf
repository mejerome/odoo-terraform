# resource "aws_db_subnet_group" "postgres" {
#   subnet_ids = aws_subnet.public.*.id
# }


# resource "aws_db_instance" "postgres" {
#   engine                  = "postgres"
#   engine_version          = "12.5"
#   instance_class          = "db.t2.micro"
#   name                    = var.odoo_db_name
#   username                = var.odoo_user
#   password                = var.odoo_db_password
#   port                    = 5432
#   db_subnet_group_name    = aws_db_subnet_group.postgres.name
#   vpc_security_group_ids  = [aws_security_group.rds_sg.id]
#   allocated_storage       = 10
#   backup_retention_period = 2
#   skip_final_snapshot     = true
#   publicly_accessible     = true
#   backup_window           = "01:00-01:30"
#   maintenance_window      = "sun:03:00-sun:03:30"
#   multi_az                = true
# }
