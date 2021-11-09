variable "tag_name" {
  default = "tf-ssx-odoo"
}

variable "region" {
  default = "eu-central-1"
}

variable "availability_zone1" {
  default = "eu-central-1a"
}

variable "availability_zone2" {
  default = "eu-central-1b"
}

variable "odoo_ami" {
  default = "ami-082a406c73ae55324" # ami-060bf7f5257d9bd73
}

variable "key_name" {
  default = "odoo-key-eu"
}

variable "key_file" {
  default = "../../odoo-key-eu.pem"
}

variable "instance_type" {
  default = "t3.small"
}

variable "hosted_zone_id" {
  default = "Z1PSEXSC6MXGQ4"
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

variable "private_subnet2_cidr" {
  default = "10.22.3.0/24"
}