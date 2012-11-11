---
layout: default
title: Install (Vagrant)
---

# Install (Vagrant)

 1. Install [Vagrant](http://vagrantup.com/v1/docs/getting-started/)

 1. Create `Vagrantfile`

        Vagrant::Config.run do |config|
          config.vm.box = 'rock-centos6'
          config.vm.box_url = 'http://dl.rockstack.org/vagrant/centos6.box'
          config.vm.provision :shell, :inline => "yum update -y rock 'rock-*'"
          config.vm.forward_port 8000, 8000
          config.vm.forward_port 9000, 9000
        end

 1. Up Vagrant box

        $ vagrant up

 1. Log into box

        $ vagrant ssh

 1. Continue to [getting started](/docs/) page
