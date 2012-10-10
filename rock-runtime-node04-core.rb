require 'formula'

class RockRuntimeNode04Core < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/node-v0.4.12.tar.gz'
  sha1 '1c6e34b90ad6b989658ee85e0d0cb16797b16460'

  env :std
  keg_only 'rock'

  def install
    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'
  end
end
