# output "odoo_rds_url" {
#   value = aws_db_instance.postgres.address
# }

# output "ecr_repository" {
#   value = aws_ecr_repository.worker.repository_url
# }

output "load_balancer_dns" {
  value = aws_alb.application_lb.dns_name
}