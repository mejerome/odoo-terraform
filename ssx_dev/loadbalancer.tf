resource "aws_alb" "application_lb" {
  name               = "${var.app_name}-${var.app_environment}-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = aws_subnet.public.*.id
  security_groups = [
    aws_security_group.loadbalancer-sg.id,
  ]
  tags = {
    Name        = "${var.app_name}-alb"
    Environment = "${var.app_environment}"
  }
}

resource "aws_lb_target_group" "target_group" {
  name        = "${var.app_name}-${var.app_environment}-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.ssx-vpc.id

  health_check {
    interval            = 300
    port                = 80
    protocol            = "HTTP"
    timeout             = 3
    healthy_threshold   = 3
    unhealthy_threshold = 2
    matcher             = "200"
    path                = "/v1/status"
  }

  tags = {
    Name        = "${var.app_name}-tg"
    Environment = "${var.app_environment}"
  }
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_alb.application_lb.id
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target_group.id
  }
}