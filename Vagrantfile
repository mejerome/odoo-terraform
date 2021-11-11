# -*- mode: ruby -*-
# vi: set ft=ruby :

$workstation_script = <<-SHELL
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
apt-add-repository "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

apt update
apt upgrade -y
apt install ansible git awscli -y

apt install terraform -y
apt install apt-transport-https ca-certificates curl software-properties-common -y

apt install docker-ce -y
usermod -aG docker ${USER}
SHELL


Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.ssh.insert_key = false
  config.vm.synced_folder ".", "/home/vagrant/odoo-terraform", disabled: false
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 1024
    vb.cpus = 1
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  config.vm.define "workstation" do |wks|
    wks.vm.hostname = "workstation.local"
    wks.vm.network "private_network", ip: "192.168.0.2"
    wks.vm.provision "shell", inline: $workstation_script
    wks.vm.provision "file", source: "~/.aws", destination: "~/.aws"
  end
end