variable "tag_name" {
  default = "tf-ssx-test"
}

variable "key_name" {
  default = "mejerome_2"
}

variable "private_key" {
  default = "../mejerome_2.pem"
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