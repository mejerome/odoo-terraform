provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

# data "aws_ami" "ubuntu" {
#   most_recent = true

#   filter {
#     name   = "name"
#     values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
#   }

#   filter {
#     name   = "virtualization-type"
#     values = ["hvm"]
#   }

#   owners = ["099720109477"] # Canonical
# }

resource "aws_network_interface" "odoo_nic" {
  subnet_id   = aws_subnet.public_sub.id
  security_groups = [aws_security_group.ssh_sg.id, aws_security_group.odoo_sg.id]

  tags = {
    Name = "primary_network_interface"
  }
}

resource "aws_instance" "odoo" {
  ami           = var.odoo_ami
  instance_type = "t2.small"
  key_name = var.key_name
  
  network_interface {
    network_interface_id = aws_network_interface.odoo_nic.id
    device_index         = 0
  }

  tags = {
    Name = "Odoo-Server"
  }
}

output "odoo_public_dns" {
  description = "Odoo Public DNS"
  value = aws_instance.odoo.public_dns
}

output "odoo_public_ip" {
  description = "Odoo Public IP"
  value = aws_instance.odoo.public_ip
}