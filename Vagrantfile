# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  # config.vm.box = "jerome-bn-odoo"
  config.vm.box = "generic/ubuntu2004"
  # config.ssh.username = "bitnami"
  # config.ssh.password = "bitnami"
  # config.ssh.insert_key = true
  # config.ssh.private_key_path = "../odoo-key-local.pem"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 4096
    vb.cpus = 2
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  config.vm.define "postgresql" do |psql|
    psql.vm.hostname = "postgresql"
    psql.vm.network :private_network, ip: "192.168.56.12"
    psql.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook/postgresql.yml"
    end
  end




  # config.vm.define "odoo" do |odoo|
  #   odoo.vm.hostname = "bitnami-odoo.local"
  #   odoo.vm.network "public_network", bridge: "wlp1s0"
  #   odoo.vm.provision "ansible" do |ansible|
  #     ansible.playbook = "playbook/bitnami_prep_local.yml"    
  #   end
  # end
end