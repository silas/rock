require 'formula'

class RockRuntimeNode010 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.10.3/node-v0.10.3.tar.gz'
  sha1 '4a1feb4ac18ede9e7193921f59fc181c88b1c7ba'

  keg_only 'rock'

  bottle do
    root_url 'http://dl.rockstack.org/homebrew/bottle'
    revision 1
    sha1 '11a408e929ea8f5891a442b25a0cd89aca654202' => :mountain_lion
  end

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
