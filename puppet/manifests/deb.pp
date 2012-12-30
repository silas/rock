$packages = [ 
  'debhelper',
  'dh-make',
  'reprepro',
  'ubuntu-dev-tools',
  'vim',
]

package { $packages:
  ensure  => latest,
}
