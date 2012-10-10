require 'formula'

class RockRuntimeNode04Npm < Formula
  homepage 'https://npmjs.org/'
  url 'http://registry.npmjs.org/npm/-/npm-1.0.106.tgz'
  sha1 'ef1830b68a1537a606dae3bdee71fd1153d7e71e'

  keg_only 'rock'
  depends_on 'rock-runtime-node04-core'

  def install
    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'
  end
end
