$packages = [ 
  'createrepo',
  'curl',
  'fedora-packager',
  'mock',
  'python-pip',
  'vim-enhanced',
]

package { $packages:
  ensure  => latest,
}->
package { 'ops':
  ensure   => latest,
  provider => 'pip'
}

exec { 'vagrant_mock':
  command => 'usermod vagrant -G mock',
  unless  => 'getent group mock | grep vagrant',
  path    => $::path,
  require => Package['mock'],
}

exec { 'brpm':
  command => 'bash -c \'
    echo "#!/usr/bin/env python" > /usr/local/bin/brpm
    curl -Ls https://raw.github.com/silas/brpm/master/brpm.py >> /usr/local/bin/brpm
  \'',
  unless  => 'test -f /usr/local/bin/brpm',
  path    => $::path,
  require => Package['curl'],
}

file { '/usr/local/bin/brpm':
  owner   => 'root',
  mode    => '755',
  require => Exec['brpm'],
}
