resource "aws_security_group" "ecs_sg" {
  vpc_id = aws_vpc.ssx-vpc.id
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.loadbalancer-sg.id]
  }

  ingress {
    from_port   = 8069
    to_port     = 8069
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.app_name}-ecs-sg"
    Environment = var.app_environment
  }
}

resource "aws_security_group" "loadbalancer-sg" {
  vpc_id = aws_vpc.ssx-vpc.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name        = "${var.app_name}-loadbalancer-sg"
    Environment = var.app_environment
  }
}

# resource "aws_security_group" "rds_sg" {
#   vpc_id = aws_vpc.ssx-vpc.id

#   ingress {
#     protocol        = "tcp"
#     from_port       = 5432
#     to_port         = 5432
#     cidr_blocks     = ["0.0.0.0/0"]
#     security_groups = [aws_security_group.ecs_sg.id]
#   }

#   egress {
#     from_port   = 0
#     to_port     = 65535
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }