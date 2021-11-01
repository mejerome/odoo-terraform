resource "aws_vpc" "ssx_vpc" {
  cidr_block = var.vpc_cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = var.tag_name
  }
}

resource "aws_internet_gateway" "ig" {
  vpc_id = aws_vpc.ssx_vpc.id

  tags = {
    Name = var.tag_name
  }
}

resource "aws_eip" "nat_eip" {
  vpc        = true
  depends_on = [aws_internet_gateway.ig]
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.private_sub.id
  depends_on    = [aws_internet_gateway.ig]

  tags = {
    Name = var.tag_name
  }
}

resource "aws_subnet" "public_sub" {
  vpc_id            = aws_vpc.ssx_vpc.id
  cidr_block        = var.public_subnet_cidr
  map_public_ip_on_launch = true
  
  tags = {
    Name = var.tag_name
  }
}

resource "aws_subnet" "private_sub" {
  vpc_id            = aws_vpc.ssx_vpc.id
  cidr_block        = var.private_subnet_cidr
  map_public_ip_on_launch = false

  tags = {
    Name = var.tag_name
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.ssx_vpc.id

  tags = {
    Name = var.tag_name
  }
}
resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.ssx_vpc.id

  tags = {
    Name = var.tag_name
  }
}

resource "aws_route" "public_internet_gateway" {
  route_table_id         = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.ig.id
}

resource "aws_route" "private_nat_gateway" {
  route_table_id         = aws_route_table.private_rt.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public_sub.id
  route_table_id = aws_route_table.public_rt.id
}
resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private_sub.id
  route_table_id = aws_route_table.private_rt.id
}
