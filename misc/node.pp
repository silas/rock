yumrepo { 'sewell':
  descr    => 'sewell',
  baseurl  => 'http://dl.sewell.org/yum/epel/6/x86_64/',
  gpgcheck => 0,
  enabled  => 1,
}

package { ['brpm', 'python-argparse', 'PyYAML']:
  ensure  => present,
  require => Yumrepo['sewell'],
}

exec { 'group_mock_vagrant':
  command => '/usr/sbin/usermod -a -G mock vagrant',
  unless  => '/usr/bin/id -G --name vagrant | grep mock &>/dev/null',
  require => Package['brpm'],
}
