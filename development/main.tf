provider "aws" {
  profile = "default"
  region  = var.region
}

resource "aws_network_interface" "odoo_nic" {
  subnet_id   = aws_subnet.public_sub.id
  security_groups = [
    aws_security_group.ssh_sg.id, 
    aws_security_group.odoo_sg.id, 
    aws_security_group.https_sg.id,
    aws_security_group.ntpd_sg.id,
    ]

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
    source      = "../custom_addons"
    destination = "~/custom_addons"
  }

  provisioner "remote-exec" {
    inline = ["sudo apt update", "sudo apt install python3 -y"]
  }
  
  connection {
    type     = "ssh"
    user     = "bitnami"
    private_key = "${file(var.key_file)}"
    host    = self.public_ip
  }

  provisioner "local-exec" {
        command = "sleep 120; ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -u bitnami --private-key ${var.key_file} -i '${self.public_ip},' ../playbook/bitnami_prep.yml"
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
    aws_instance.odoo.public_dns,
  ]
  
  depends_on = [
    aws_instance.odoo,
  ]
}
