yumrepo { 'sewell':
  descr    => 'sewell',
  baseurl  => 'http://dl.sewell.org/yum/epel/6/x86_64/',
  gpgcheck => 0,
  enabled  => 1,
}

package { ['brpm', 'git', 'python-argparse', 'PyYAML', 'vim-enhanced']:
  ensure  => present,
  require => Yumrepo['sewell'],
}

exec { 'group_mock_vagrant':
  command => '/usr/sbin/usermod -a -G mock vagrant',
  unless  => '/usr/bin/id -G --name vagrant | grep mock &>/dev/null',
  require => Package['brpm'],
}

$bashrc = '
test -f /etc/bashrc && . /etc/bashrc
test -f /home/vagrant/.bash_local && . /home/vagrant/.bash_local

export PATH="/vagrant/python-rock/scripts:$PATH"
export PYTHONPATH="/vagrant/python-rock:$PYTHONPATH"
'

file { '/home/vagrant/.bashrc':
  ensure  => present,
  owner   => 'vagrant',
  group   => 'vagrant',
  mode    => '0644',
  content => $bashrc,
}
