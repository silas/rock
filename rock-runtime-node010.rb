require 'formula'

class RockRuntimeNode010 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.10.31/node-v0.10.31.tar.gz'
  sha1 '80f2160b0525763b557742aa73d8dacf1a71e53c'

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
    runtime += 'node010'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
