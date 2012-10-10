require 'formula'

class RockRuntimeNode04 < Formula
  homepage 'http://nodejs.org/'
  url "http://nodejs.org/dist/node-v0.4.12.tar.gz"
  sha1 '1c6e34b90ad6b989658ee85e0d0cb16797b16460'

  env :std
  keg_only 'rock'

  def install_npm
    npm_version = '1.0.106'

    ENV['PATH'] = "#{bin}:#{ENV['PATH']}"

    system 'curl', '-O', "http://registry.npmjs.org/npm/-/npm-#{npm_version}.tgz"
    system 'tar', '-xzf', "npm-#{npm_version}.tgz"

    Dir.chdir 'package'

    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'
    system "echo 'prefix = #{prefix}' > #{prefix}/lib/node_modules/npm/npmrc"

    Dir.chdir '..'
  end

  def install
    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'
    install_npm
  end
end
