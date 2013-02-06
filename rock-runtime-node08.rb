require 'formula'

class RockRuntimeNode08 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.8.18/node-v0.8.18.tar.gz'
  sha1 'e3bc9b64f60f76a32b7d9b35bf86b5d1b8166717'

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
