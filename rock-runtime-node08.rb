require 'formula'

class RockRuntimeNode08 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.8.11/node-v0.8.11.tar.gz'
  sha1 'e9dd36cbbe03c632ee7e9c52e06122fa022981c8'

  keg_only 'rock'

  def install
    rock = Pathname.new('/opt/rock')

    unless rock.directory? && rock.writable?
      onoe "#{rock} must be a directory and writable"
      exit 1
    end

    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'

    runtime = rock + 'runtime/node08'
    runtime.mkpath
    runtime += 'rock.yml'
    runtime.unlink if runtime.exist?
    runtime.write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS
  end
end
