require 'formula'

class RockRuntimeNode010 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.10.0/node-v0.10.0.tar.gz'
  sha1 '7321266347dc1c47ed2186e7d61752795ce8a0ef'

  keg_only 'rock'

  def install
    rock = Pathname.new('/opt/rock')

    unless rock.directory? && rock.writable?
      onoe "#{rock} must be a directory and writable"
      exit 1
    end

    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'

    runtime = rock + 'runtime/node010'
    runtime.mkpath
    runtime += 'rock.yml'
    runtime.unlink if runtime.exist?
    runtime.write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS
  end
end
