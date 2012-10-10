require 'formula'

class RockRuntimeNode08 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.8.11/node-v0.8.11.tar.gz'
  sha1 'e9dd36cbbe03c632ee7e9c52e06122fa022981c8'
  keg_only 'rock'

  def install
    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'
  end
end
