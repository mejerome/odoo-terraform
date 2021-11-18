# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "jerome-bitnami-odoo"
  config.ssh.username = "bitnami"
  config.ssh.private_key_path = "../odoo-key-local.pem"
  config.vm.synced_folder ".", "/vagrant"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 4096
    vb.cpus = 2
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  config.vm.define "odoo" do |odoo|
    odoo.vm.hostname = "bitnami-odoo.local"
    odoo.vm.network "public_network", bridge: "wlp1s0"
    odoo.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "playbook/bitnami_prep.yml"    
    end
  end
end