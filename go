#!/usr/bin/env bash

set -o errexit

die() {
  echo "Error: $@" >&2
  exit 1
}

echo 'Checking for requirements...'

if [[ "$( uname -s )" != Darwin ]]; then
  die 'only supports OS X right now'
fi

if ! type -f 'xcode-select' &>/dev/null ; then
  die "xcode must be installed"
fi

if [[ ! -d '/opt/rock' ]]; then
  echo
  echo 'Creating /opt/rock directory...'
  sudo mkdir -p /opt/rock
  sudo chown "$USER" /opt/rock
fi

if [[ ! -e /usr/local/bin/brew ]]; then
  echo
  echo 'Installing brew...'
  ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
fi

echo
echo 'Updating brew'
brew update

if [[ "$( brew tap )" != *homebrew/dupes* ]]; then
  echo
  echo 'Tapping homebrew/dupes'
  brew tap homebrew/dupes
fi

if [[ "$( brew tap )" != *rockstack/rock* ]]; then
  echo
  echo 'Tapping rockstack/rock'
  brew tap rockstack/rock
fi

if ! pip &>/dev/null; then
  echo
  echo 'Installing pip...'
  sudo easy_install pip
fi

# install manually so we avoid prompting user about java
if [[ "$( brew list )" != *berkeley-db* ]]; then
  echo
  echo "Installing berkeley-db..."
  brew install berkeley-db --without-java
fi

if [[ "${ROCK_SKIP_CLI}" != "true" ]]; then
  echo
  echo "Trying to install/update rock..."
  sudo pip install -U rock
fi

if [[ "${ROCK_SKIP_RUNTIMES}" != "true" ]]; then
  for name in $( brew list | grep -e '^rock-' ); do
    echo
    echo "Trying to update ${name}..."
    brew upgrade $name 2>&1 | grep -v -e '^Error: .* already installed$'
  done
fi
