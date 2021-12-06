# Task Definitions
resource "aws_ecs_task_definition" "odoo" {
  family                = "${var.app_name}-odoo"
  container_definitions = <<DEFINITION
    [
    {
      "name"      : "odoo",
      "image"     : "docker.io/bitnami/odoo:15.0",
      "essential" : true,
      "portMappings" : [
        {
          "containerPort" : 8069,
          "hostPort"      : 8069
        }
      ],
      "logConfiguration":  {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-group" : "${aws_cloudwatch_log_group.log-group.name}",
          "awslogs-region" : "eu-central-1",
          "awslogs-stream-prefix" : "odoo"
        }
      }
    },
    {
      "name": "postgres",
      "image": "docker.io/bitnami/postgresql:13",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5432,
          "hostPort": 5432
        }
      ],
      "logConfiguration":  {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "${aws_cloudwatch_log_group.log-group.name}",
          "awslogs-region": "eu-central-1",
          "awslogs-stream-prefix": "postgres"
        }
      }
    }
  ]
  DEFINITION

  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                     = 1024
  memory                  = 2048
  execution_role_arn       = aws_iam_role.ecs_agent.arn
  task_role_arn            = aws_iam_role.ecs_agent.arn
  volume {
    name = "efs-storage"
    efs_volume_configuration {
      file_system_id = aws_efs_file_system.odoo_data.id
      root_directory = "/opt/data"
      # transit_encryption = "ENABLED"
    }
  }
  tags = {
    Name        = "${var.app_name}-odoo-td"
    Environment = "${var.app_environment}"
  }
}
