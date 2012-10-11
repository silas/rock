require 'formula'

class RockRuntimePython27 < Formula
  homepage 'http://www.python.org/'
  url 'http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2'
  sha1 '842c4e2aff3f016feea3c6e992c7fa96e49c9aa0'

  env :std
  keg_only 'rock'

  def install_virtualenv
    virtualenv_version = '1.8.2'

    system 'curl', '-O', "http://pypi.python.org/packages/source/v/virtualenv/virtualenv-#{virtualenv_version}.tar.gz"
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
