class BuildCommand < Vagrant::Command::Base
  def execute
    all = true
    flags = {}

    opts = OptionParser.new do |o|
      o.banner = 'Usage: vagrant build [-h] package [package ...]'
      o.on('--deb', 'Build deb') do |v|
        all = false
        flags[:deb] = v
      end
      o.on('--rpm', 'Build rpm') do |v|
        all = false
        flags[:rpm] = v
      end
    end

    argv = parse_options(opts)

    if !argv || argv.length < 1
      @env.ui.error('package list required')
      return
    end

    flags = {
      :deb => all,
      :rpm => all,
    }.merge(flags)

    argv.each do |name|
      if flags[:deb]
        @env.vms[:deb].channel.execute("touch #{name}.deb")
      end

      if flags[:rpm]
        @env.vms[:rpm].channel.execute("touch #{name}.rpm")
      end
    end
  end
end

Vagrant.commands.register(:build) { BuildCommand }

Vagrant::Config.run do |config|
  customize = [
    'modifyvm', :id,
    '--cpus', ENV['BUILD_CPUS'] || '4',
  ]

  config.vm.define :deb do |deb_config|
    deb_config.vm.box = 'ubuntu-quantal'
    deb_config.vm.box_url = 'https://github.com/downloads/roderik/VagrantQuantal64Box/quantal64.box'
    deb_config.vm.customize customize
    deb_config.vm.provision :puppet do |puppet|
      puppet.manifests_path = 'puppet/manifests' 
      puppet.manifest_file = 'deb.pp'
    end
  end

  config.vm.define :rpm do |rpm_config|
    rpm_config.vm.box = 'fedora-17'
    rpm_config.vm.box_url = 'http://dl.sewell.org/vagrant/fedora-17-x86_64.box'
    rpm_config.vm.customize customize
    rpm_config.vm.provision :puppet do |puppet|
      puppet.manifests_path = 'puppet/manifests' 
      puppet.manifest_file = 'rpm.pp'
    end
  end
end
