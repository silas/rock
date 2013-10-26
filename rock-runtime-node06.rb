require 'formula'

class RockRuntimeNode06 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.6.21/node-v0.6.21.tar.gz'
  sha1 '31f564bf34c64b07cae3b9a88a87b4a08bab4dc5'

  env :std
  keg_only 'rock'

  def install
    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'

    src_yml = prefix + 'rock.yml'
    src_yml.write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS

    dst_yml = var + 'rock/opt/rock/runtime/node06'
    dst_yml.mkpath
    dst_yml += 'rock.yml'
    dst_yml.unlink if dst_yml.exist?

    File.symlink(src_yml, dst_yml)
  end
end
