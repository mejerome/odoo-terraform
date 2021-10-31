variable "tag_name" {
  default = "tf-ssx-test"
}

variable "odoo_ami" {
  default = "ami-060bf7f5257d9bd73"
}

variable "key_name" {
  default = "odoo-key"
}

variable "vpc_cidr_block" {
  default = "10.22.0.0/16"
}

variable "public_subnet_cidr" {
  default = "10.22.1.0/24"
}

variable "private_subnet_cidr" {
  default = "10.22.2.0/24"
}