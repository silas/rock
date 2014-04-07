Vagrant.configure('2') do |config|
  customize = [
    'modifyvm', :id,
    '--cpus', ENV['BUILD_CPUS'] || '4',
    '--memory', ENV['BUILD_MEMORY'] || 1024,
  ]

  config.vm.define :deb do |deb_config|
    deb_config.vm.box = 'ubuntu-13_10'
    deb_config.vm.box_url = 'http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_ubuntu-13.10_chef-provisionerless.box'
    deb_config.vm.provider :virtualbox do |v|
      v.customize customize
    end
    deb_config.vm.provision 'shell', path: 'misc/deb.sh'
  end

  config.vm.define :rpm do |rpm_config|
    rpm_config.vm.box = 'fedora-20'
    rpm_config.vm.box_url = 'http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_fedora-20_chef-provisionerless.box'
    rpm_config.vm.provider :virtualbox do |v|
      v.customize customize
    end
    rpm_config.vm.provision 'shell', path: 'misc/rpm.sh'
  end
end
