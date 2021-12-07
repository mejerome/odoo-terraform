variable "aws_region" {
  type        = string
  description = "AWS Region"
}

variable "aws_cloudwatch_retention_in_days" {
  type        = number
  description = "AWS CloudWatch Logs Retention in Days"
  default     = 1
}

variable "hosted_zone_id" {
  description = "value of the Hosted Zone ID"
}

variable "database_fqdn" {
  description = "value of the Hosted Zone ID"
}

variable "loadbalancer_fqdn" {
  description = "value of the Hosted Zone ID"
}

variable "app_name" {
  type        = string
  description = "Application Name"
}

variable "app_environment" {
  type        = string
  description = "Application Environment"
}

variable "odoo_user" {
  type        = string
  description = "User for Odoo"
}

variable "odoo_db_name" {
  type        = string
  description = "Odoo Database Name"
}

variable "odoo_db_password" {
  type        = string
  description = "Odoo Database Password"
}

variable "cidr" {
  description = "The CIDR block for the VPC."
  default     = "10.0.0.0/16"
}

variable "public_subnets" {
  description = "List of public subnets"
}

variable "private_subnets" {
  description = "List of private subnets"
}

variable "availability_zones" {
  description = "List of availability zones"
}

variable "cloudwatch_group" {
  description = "CloudWatch Log Group"
}