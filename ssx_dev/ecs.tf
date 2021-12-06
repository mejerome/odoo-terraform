# ECS Cluster
resource "aws_ecs_cluster" "ssx-cluster" {
  name = "${var.app_name}-${var.app_environment}-cluster"
  tags = {
    Name        = "${var.app_name}-ecs"
    Environment = "${var.app_environment}"
  }
}

# CloudWatch Logs
resource "aws_cloudwatch_log_group" "log-group" {
  name = "${var.app_name}-${var.app_environment}-logs"
  tags = {
    Name        = var.app_name
    Environment = var.app_environment
  }
}

resource "aws_ecs_service" "ssx-ecs-service" {
  name                 = "${var.app_name}-${var.app_environment}-ecs-service"
  cluster              = aws_ecs_cluster.ssx-cluster.id
  task_definition      = aws_ecs_task_definition.odoo.arn
  launch_type          = "FARGATE"
  desired_count        = 1
  force_new_deployment = true
  network_configuration {
    subnets          = aws_subnet.public.*.id
    assign_public_ip = true
    security_groups = [
      aws_security_group.ecs_sg.id,
      aws_security_group.loadbalancer-sg.id
    ]
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.target_group.arn
    container_name   = "odoo"
    container_port   = 8069
  }
  depends_on = [aws_lb_listener.listener]
}

