Vagrant.configure('2') do |config|
  config.vm.define :centos do |c|
    c.vm.box = 'centos6'
    c.vm.box_url = 'http://puppet-vagrant-boxes.puppetlabs.com/centos-64-x64-vbox4210.box'
  end
  config.vm.define :ubuntu do |c|
    c.vm.box = 'precise64'
    c.vm.box_url = 'http://files.vagrantup.com/precise64.box'
  end
end
