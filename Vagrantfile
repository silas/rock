# vi: set ft=ruby

Vagrant.configure('2') do |config|
  config.vm.define :centos do |c|
    c.vm.box = 'centos6'
    c.vm.box_url = 'http://puppet-vagrant-boxes.puppetlabs.com/centos-64-x64-vbox4210.box'

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

  config.vm.define :ubuntu do |c|
    c.vm.box = 'precise64'
    c.vm.box_url = 'http://files.vagrantup.com/precise64.box'

    c.vm.provision :shell, inline: <<-eof
      set -o errexit
      apt-get update
      apt-get install -y curl git python-virtualenv vim
      rm -fr /opt/tests
      virtualenv /opt/tests
      (. /opt/tests/bin/activate ; pip install -r /vagrant/requirements.txt)
    eof
  end
end
