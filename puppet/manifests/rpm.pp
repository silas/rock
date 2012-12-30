yumrepo { 'sewell':
  enabled  => 1,
  gpgcheck => 0,
  baseurl  => 'http://dl.sewell.org/rpm/sewell/fedora/$releasever/$basearch',
}

$packages = [ 
  'brpm',
  'fedora-packager',
  'mock',
  'vim-enhanced',
]

package { $packages:
  ensure  => latest,
  require => Yumrepo['sewell'],
}

exec { 'vagrant_mock':
  command => 'usermod vagrant -G mock',
  unless  => 'getent group mock | grep vagrant',
  path    => $::path,
  require => Package['mock'],
}
