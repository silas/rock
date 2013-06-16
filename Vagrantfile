Vagrant.configure('2') do |config|
  customize = [
    'modifyvm', :id,
    '--cpus', ENV['BUILD_CPUS'] || '4',
    "--memory", ENV['BUILD_MEMORY'] || 1024,
  ]

  config.vm.define :deb do |deb_config|
    deb_config.vm.box = 'ubuntu-quantal'
    deb_config.vm.box_url = 'https://github.com/downloads/roderik/VagrantQuantal64Box/quantal64.box'
    deb_config.vm.provider :virtualbox do |v|
      v.customize customize
    end
    deb_config.vm.provision :puppet do |puppet|
      puppet.manifests_path = 'puppet/manifests' 
      puppet.manifest_file = 'deb.pp'
    end
  end

  config.vm.define :rpm do |rpm_config|
    rpm_config.vm.box = 'fedora-17'
    rpm_config.vm.box_url = 'http://dl.sewell.org/vagrant/fedora-17-x86_64.box'
    rpm_config.vm.provider :virtualbox do |v|
      v.customize customize
    end
    rpm_config.vm.provision :puppet do |puppet|
      puppet.manifests_path = 'puppet/manifests' 
      puppet.manifest_file = 'rpm.pp'
    end
  end
end
