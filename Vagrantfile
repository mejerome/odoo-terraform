# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.ssh.insert_key = false
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 1024
    vb.cpus = 1
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  config.vm.define "postgres" do |postgres|
    postgres.vm.hostname = "postgres"
    postgres.vm.network "private_network", ip: "192.168.0.1"
    postgres.vm.provision "ansible" do |ansible|
      ansible.playbook = "./playbook/postgres.yml"
    end
  end
end