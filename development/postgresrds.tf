# resource "aws_db_instance" "odoo_db" {
#   allocated_storage    = 10
#   engine               = "postgres"
#   engine_version       = "12.5"
#   instance_class       = "db.t2.micro"
#   name                 = "odoo_db"
#   username             = "odoo"
#   password             = "foobarbaz"
#   skip_final_snapshot  = true
#   vpc_security_group_ids = [ aws_security_group.postgres_sg.id ]
#   multi_az = false
#   db_subnet_group_name = aws_db_subnet_group.odoo_db.name
#   publicly_accessible = true
#   tags = {
#     Name = var.tag_name
#   }
# }

# resource "aws_db_subnet_group" "odoo_db" {
#   name       = "main"
#   subnet_ids = [aws_subnet.private_sub.id, aws_subnet.private_sub2.id]

#   tags = {
#     Name = var.tag_name
#   }
# }