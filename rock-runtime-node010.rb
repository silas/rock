require 'formula'

class RockRuntimeNode010 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.10.21/node-v0.10.21.tar.gz'
  sha1 'b7fd2a3660635af40e3719ca0db49280d10359b2'

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
