require 'formula'

class RockRuntimePython27 < Formula
  homepage 'http://www.python.org/'
  url 'http://www.python.org/ftp/python/2.7.4/Python-2.7.4.tar.bz2'
  sha1 'deb8609d8e356b3388f33b6a4d6526911994e5b1'

  env :std
  keg_only 'rock'

  bottle do
    root_url 'http://dl.rockstack.org/homebrew/bottle'
    revision 1
    sha1 '57894c89ae62dbe880d40f7bad99d97a533c7a2b' => :mountain_lion
  end

  def install_virtualenv
    virtualenv_version = '1.9.1'

    system 'curl', '-O', "https://pypi.python.org/packages/source/v/virtualenv/virtualenv-#{virtualenv_version}.tar.gz"
    system 'tar', '-xzf', "virtualenv-#{virtualenv_version}.tar.gz"

    Dir.chdir "virtualenv-#{virtualenv_version}"

    system 'python', 'setup.py', 'install'

    Dir.chdir '..'
  end

  def install
    rock = Pathname.new('/opt/rock')

    unless rock.directory? && rock.writable?
      onoe "#{rock} must be a directory and writable"
      exit 1
    end

    ENV.append 'EXTRA_CFLAGS', '-fwrapv'

    system './configure', "--prefix=#{prefix}"
    ENV.j1
    system 'make', 'install'

    ENV['LDFLAGS'] = "-Wl,-rpath #{prefix}/lib"

    system './configure',
      "--prefix=#{prefix}",
      '--enable-ipv6',
      '--enable-shared'

    ENV['PATH'] = "#{bin}:#{ENV['PATH']}"

    install_virtualenv

    runtime = rock + 'runtime/python27'
    runtime.mkpath
    runtime += 'rock.yml'
    runtime.unlink if runtime.exist?
    runtime.write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS
  end
end
