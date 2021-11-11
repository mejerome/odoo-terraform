resource "aws_vpc" "ssx-vpc" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = var.tag_name
  }
}


resource "aws_subnet" "web-subnet" {
  vpc_id                  = aws_vpc.ssx-vpc.id
  cidr_block              = var.public_subnet_cidr
  map_public_ip_on_launch = true
  availability_zone       = var.web_availability_zone

  tags = {
    Name = var.tag_name
  }
}

resource "aws_subnet" "db-subnet-1" {
  vpc_id                  = aws_vpc.ssx-vpc.id
  cidr_block              = var.private_subnet2_cidr
  map_public_ip_on_launch = false
  availability_zone       = var.app_availability_zone_1

  tags = {
    Name = var.tag_name
  }
}

resource "aws_subnet" "db-subnet-2" {
  vpc_id                  = aws_vpc.ssx-vpc.id
  cidr_block              = var.private_subnet_cidr
  map_public_ip_on_launch = false
  availability_zone       = var.app_availability_zone_2

  tags = {
    Name = var.tag_name
  }
}
