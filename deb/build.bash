#!/usr/bin/env bash
set -e

ARCHS=( amd64 i386 )
DISTS=( precise quantal lenny squeeze wheezy)

SOURCE_DIR=/root/source
PBUILDER_DIR=/root/pbuilder
PBUILDER_MOUNT="/root/apt"

cd `dirname $0`
cwd=`pwd`
trap "echo $cwd; cd $cwd; mv {*.tar.gz,*.dsc,*.build,*.changes} $SOURCE_DIR/ 2&> /dev/null" SIGINT SIGTERM

cd $cwd
packages=`cat ./build.list`

function build() {
  package=$1
  dist=$2
  arch=$3
  pbuilder_name=$dist
  
  if [ "$arch" == 'i386' ]
  then
    pbuilder_name=$pbuilder_name-$arch
  fi
  
  pbuilder_result_mount="$PBUILDER_DIR/${pbuilder_name}_result"
  pbuilder_package_mount="$PBUILDER_MOUNT/$pbuilder_name"
  pbuilder_name=$pbuilder_name-base.tgz
 
cat << HERE > ~/.pbuilderrc
BINDMOUNTS="$PBUILDER_MOUNT"
HOOKDIR="$pbuilder_package_mount"
ALLOWUNTRUSTED=yes
HERE

mkdir -p $pbuilder_package_mount
cat << HERE > $pbuilder_package_mount/D05deps
#!/usr/bin/env bash

echo "deb file://$pbuilder_package_mount ./" >> /etc/apt/sources.list
apt-get update
HERE

  chmod +x $pbuilder_package_mount/D05deps
 
  pbuilder_create_args=''
  pbuilder_create_args="$pbuilder_args --debootstrapopts --variant=buildd"

  if [ ! -e "$PBUILDER_DIR/$pbuilder_name" ] || [ "`du $PBUILDER_DIR/$pbuilder_name | awk '{print $1}'`" == 0 ]
  then
    echo "Environment $dist-$arch does not exist, creating..."
    echo "Running: pbuilder-dist $dist $arch create $pbuilder_args"
    pbuilder-dist $dist $arch create $pbuilder_create_args
  fi

  cd $cwd
  package_path=`find ./$package -type d -name *debian`
  cd `dirname $package_path`

  deb=`grep -m 1 "(.*)" debian/changelog | sed 's/\([^ ]*\) (\(.*\)*).*/\1_\2/'`
  match_deb=`find $pbuilder_package_mount -type f -name $deb*deb`
  if [ "$match_deb" != '' ]
  then
    echo "$match_deb found, skipping"
    return
  fi

  echo "-----> Building package: $package_path"
  cd $pbuilder_package_mount
  apt-ftparchive packages . > Packages

  cd $cwd
  cd `dirname $package_path`

  if [ -e 'debian/watch' ]
  then
    debian/rules get-orig-source
  fi

  debuild -S -us -uc
  mv ../{*.tar.gz,*.dsc,*.build,*.changes} $SOURCE_DIR/
  pbuilder-dist $dist $arch build $SOURCE_DIR/$(basename $(pwd))_*.dsc

  cd $PBUILDER_DIR
  mkdir -p $pbuilder_package_mount
  mv $pbuilder_result_mount/*.deb $pbuilder_package_mount/
}

# Ensure build deps are installed
echo "Ensuring build tools are installed..."
apt-get install ubuntu-dev-tools debhelper dh-make reprepro -y

# Ensure local apt is available
mkdir -p $PBUILDER_MOUNT

# Ensure local source dir is available
mkdir -p $SOURCE_DIR

# Individual package
package=$1
dist=$2
arch=$3
if [ ! -z "$package" ] && [ ! -z "$dist" ] && [ ! -z "$arch" ]
then
  build $package $dist $arch
  exit 0
fi

# All packages
for dist in ${DISTS[@]}
do
  for arch in ${ARCHS[@]}
  do
    for package in ${packages[@]}
    do
      echo "Processing: $package-$dist-$arch"
      build $package $dist $arch
    done
  done
done
