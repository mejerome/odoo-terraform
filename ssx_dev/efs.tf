resource "aws_efs_file_system" "odoo_data" {
  tags = {
    Name = "${var.app_name}-store"
  }
}

resource "aws_efs_mount_target" "mount" {
  file_system_id = "${aws_efs_file_system.odoo_data.id}"
  subnet_id      = aws_subnet.public[count.index].id
  security_groups = [aws_security_group.ecs_sg.id]
  count          = 2
}