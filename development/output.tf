output "odoo_public_dns" {
  description = "Odoo Public DNS"
  value       = aws_instance.odoo.public_dns
}

output "odoo_public_ip" {
  description = "Odoo Public IP"
  value       = aws_instance.odoo.public_ip
}

output "odoo_url" {
  description = "Odoo URL"
  value       = aws_route53_record.ssxodoo.name
}

# output "odoo_db_url" {
#   description = "Odoo DB URL"
#   value = aws_db_instance.odoo_db.endpoint
# }