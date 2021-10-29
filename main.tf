provider "aws" {
  profile = "default"
  region  = "us-east-2"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_network_interface" "odoo_nic" {
  subnet_id   = aws_subnet.public_sub.id
  security_groups = [aws_security_group.ssh_sg.id, aws_security_group.odoo_sg.id]

  tags = {
    Name = "primary_network_interface"
  }
}

resource "aws_instance" "odoo" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.small"
  key_name = var.key_name
  
  network_interface {
    network_interface_id = aws_network_interface.odoo_nic.id
    device_index         = 0
  }
  provisioner "remote-exec" {
    inline = ["sudo apt update", "sudo apt install python3 -y", "echo Done!"]

    connection {
      host        = self.public_ip
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.private_key)
    }
  }

  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -u ubuntu -i '${self.public_ip},' --private-key ${var.private_key} playbook/main.yml"
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