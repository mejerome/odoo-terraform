# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu2004"
  # config.ssh.username = "bitnami"
  # config.ssh.password = "bitnami"
  # config.ssh.insert_key = true
  # config.ssh.private_key_path = "../odoo-key-local.pem"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 1024
    vb.cpus = 1
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  config.vm.define "postgres" do |odoo|
    odoo.vm.hostname = "postgres.local"
    odoo.vm.network "private_network", ip: "192.168.56.12"
    odoo.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook/postgres.yml"    
    end
  end
end