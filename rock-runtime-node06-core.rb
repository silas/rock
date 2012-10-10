require 'formula'

class RockRuntimeNode06 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.6.21/node-v0.6.21.tar.gz'
  sha1 '31f564bf34c64b07cae3b9a88a87b4a08bab4dc5'
  keg_only 'rock'

  def install
    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'
  end
end
