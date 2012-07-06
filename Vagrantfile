Vagrant::Config.run do |config|
  config.vm.box = 'centos-6'
  config.vm.box_url = 'http://dl.sewell.org/vagrant/centos-6.box'
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = 'misc'
    puppet.manifest_file = 'node.pp'
  end
end
