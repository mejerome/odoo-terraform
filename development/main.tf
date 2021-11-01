provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_network_interface" "odoo_nic" {
  subnet_id   = aws_subnet.public_sub.id
  security_groups = [aws_security_group.ssh_sg.id, aws_security_group.odoo_sg.id]

  tags = {
    Name = "primary_network_interface"
  }
}

resource "aws_instance" "odoo" {
  ami           = var.odoo_ami
  instance_type = var.instance_type
  key_name = var.key_name
  
  network_interface {
    network_interface_id = aws_network_interface.odoo_nic.id
    device_index         = 0
  }

  provisioner "file" {
    source      = "../lightsail/custom_addons"
    destination = "~/custom_addons"
  }
  connection {
    type     = "ssh"
    user     = "bitnami"
    private_key = "${file("../../odoo-key.pem")}"
    host    = self.public_ip
  }

  tags = {
    Name = "Odoo-Server"
  }
}

resource "aws_route53_record" "ssxodoo" {
  zone_id = var.hosted_zone_id
  name    = "ssxodoo.sysloggh.com"
  type    = "CNAME"
  ttl     = "300"
  
  records = [
    aws_instance.odoo.public_ip,
  ]
}
