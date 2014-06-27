Vagrant.configure('2') do |config|
  config.vm.box = 'fedora-20'
  config.vm.box_url = 'http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_fedora-20_chef-provisionerless.box'

  config.vm.provider :virtualbox do |v|
    v.customize ['modifyvm', :id, '--cpus', ENV['BUILD_CPUS'] || '4']
    v.customize ['modifyvm', :id, '--memory', ENV['BUILD_MEMORY'] || 1024]
    v.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    v.customize ['modifyvm', :id, '--natdnsproxy1', 'on']
    v.customize ['setextradata', :id, 'VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root', '1']
  end

  config.vm.provision :shell, inline: <<-eof
    set -o errexit

    yum clean all

    yum update -y vim-minimal

    yum install -y \
      createrepo \
      curl \
      fedora-packager \
      mock \
      python-pip \
      vim

    pip install ops

    usermod vagrant -G mock

    echo '#!/usr/bin/env python' > /usr/local/bin/brpm

    curl -Ls https://github.com/silas/brpm/raw/master/brpm.py >> /usr/local/bin/brpm

    chmod 755 /usr/local/bin/brpm
  eof
end
