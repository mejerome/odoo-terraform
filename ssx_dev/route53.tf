# resource "aws_route53_record" "odoo_postgres" {
#   zone_id = var.hosted_zone_id
#   name    = var.database_fqdn
#   type    = "CNAME"
#   ttl     = "300"
#   records = [
#     aws_db_instance.postgres.address
#   ]
# }

resource "aws_route53_record" "odoo_lb" {
  zone_id = var.hosted_zone_id
  name    = var.loadbalancer_fqdn
  type    = "CNAME"
  ttl     = "300"
  records = [
    aws_alb.application_lb.dns_name
  ]
}