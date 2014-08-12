require 'formula'

class RockRuntimeNode08 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.8.28/node-v0.8.28.tar.gz'
  sha1 'ea2b94d75658914ddfe6a536ef27d1c016156e2d'

  keg_only 'rock'

  def install
    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'

    (prefix + 'rock.yml').write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS

    runtime = var + 'rock/opt/rock/runtime'
    runtime.mkpath
    runtime += 'node08'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
