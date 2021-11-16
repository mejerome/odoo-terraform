resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.ssx-vpc.id

  tags = {
    Name = var.tag_name
  }
}

resource "aws_route_table" "web-rt" {
  vpc_id = aws_vpc.ssx-vpc.id


  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = var.tag_name
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.web-subnet.id
  route_table_id = aws_route_table.web-rt.id
}

resource "aws_route_table" "db-rt" {
  vpc_id = aws_vpc.ssx-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.ngw.id
  }

  tags = {
    Name = var.tag_name
  }
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.db-subnet-1.id
  route_table_id = aws_route_table.db-rt.id
}


resource "aws_eip" "nat-eip" {
  vpc = true  
  tags = {
    Name = var.tag_name
  }
}

resource "aws_nat_gateway" "ngw" {
  allocation_id = aws_eip.nat-eip.id
  subnet_id = aws_subnet.web-subnet.id
  tags = {
    Name = var.tag_name
  }
}