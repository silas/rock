# vi: set ft=ruby

Vagrant.configure('2') do |config|
  config.vm.define :centos6 do |c|
    c.vm.box = 'chef/centos-6.5'

    c.vm.provider :virtualbox do |v|
      v.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
      v.customize ['modifyvm', :id, '--natdnsproxy1', 'on']
    end

    c.vm.provision :shell, inline: <<-eof
      set -o errexit
      rpm -qi epel-release &>/dev/null || \
        rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
      yum clean all
      yum install -y curl git python-virtualenv vim
      rm -fr /opt/tests
      virtualenv /opt/tests
      (. /opt/tests/bin/activate ; pip install -r /vagrant/requirements.txt)
    eof
  end

  config.vm.define :centos7 do |c|
    c.vm.box = 'chef/centos-7.0'

    c.vm.provider :virtualbox do |v|
      v.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
      v.customize ['modifyvm', :id, '--natdnsproxy1', 'on']
    end

    c.vm.provision :shell, inline: <<-eof
      set -o errexit
      rpm -qi epel-release &>/dev/null || \
        rpm -Uvh http://mirror.pnl.gov/epel/7/x86_64/e/epel-release-7-1.noarch.rpm
      yum clean all
      yum install -y curl git python-virtualenv vim
      rm -fr /opt/tests
      virtualenv /opt/tests
      (. /opt/tests/bin/activate ; pip install -r /vagrant/requirements.txt)
    eof
  end
end
