require 'formula'

class RockRuntimePython33 < Formula
  homepage 'http://www.python.org/'
  url 'http://www.python.org/ftp/python/3.3.1/Python-3.3.1.tar.bz2'
  sha1 'bec78674847a4dacc4717c93b32b6b07adb90afe'

  env :std
  keg_only 'rock'

  bottle do
    root_url 'http://dl.rockstack.org/homebrew/bottle'
    sha1 'feeec20bb5a23cedda9ef6c0274ba0909cf04268' => :mountain_lion
  end

  def install_distribute
    distribute_version = '0.6.36'

    system 'curl', '-LO', "https://bitbucket.org/tarek/distribute/raw/#{distribute_version}/distribute_setup.py"
    system "sed 's|#!python|#!/usr/bin/env python|g' distribute_setup.py > #{bin}/distribute-setup"
    system 'chmod', '755', "#{bin}/distribute-setup"
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

    install_distribute

    runtime = rock + 'runtime/python33'
    runtime.mkpath
    runtime += 'rock.yml'
    runtime.unlink if runtime.exist?
    runtime.write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS
  end
end
