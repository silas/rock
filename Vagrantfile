# vi: set ft=ruby

Vagrant.configure('2') do |config|
  config.vm.box = 'centos6'
  config.vm.box_url = 'http://puppet-vagrant-boxes.puppetlabs.com/centos-65-x64-virtualbox-puppet.box'

  config.vm.provider :virtualbox do |v|
    v.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    v.customize ['modifyvm', :id, '--natdnsproxy1', 'on']
  end

  config.vm.provision :shell, inline: <<-eof
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
