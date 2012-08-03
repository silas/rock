---
layout: default
title: Install (Vagrant)
---

# Install (Vagrant)

 1. Install [Vagrant](http://vagrantup.com/v1/docs/getting-started/)

 1. Create `Vagrantfile`

        Vagrant::Config.run do |config|
          config.vm.box = 'rp0-centos6'
          config.vm.box_url = 'http://dl.rockplatform.org/rp0/vagrant/centos6.box'
          config.vm.provision :shell, :inline => "yum update -y rock 'rock-*'"
        end

 1. Up Vagrant box

        $ vagrant up

 1. Log into box

        $ vagrant ssh

 1. Continue to [getting started](/getting-started/) page
