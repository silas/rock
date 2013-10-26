require 'formula'

class RockRuntimePython27 < Formula
  homepage 'http://www.python.org/'
  url 'http://www.python.org/ftp/python/2.7.4/Python-2.7.4.tar.bz2'
  sha1 'deb8609d8e356b3388f33b6a4d6526911994e5b1'

  env :std
  keg_only 'rock'

  resource 'virtualenv' do
    url 'https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.1.tar.gz'
    sha1 'b7d1704ec186a71c2fff1706896ecd294b708a55'
  end

  def install
    ENV.append 'EXTRA_CFLAGS', '-fwrapv'

    if ENV.compiler == :clang
      ENV.append_to_cflags '-Wno-unused-value'
      ENV.append_to_cflags '-Wno-empty-body'
      ENV.append_to_cflags '-Qunused-arguments'
    else
      ENV.append 'LDFLAGS', "-Wl,-rpath #{prefix}/lib"
    end

    unless MacOS::CLT.installed?
      ENV.append_to_cflags "-I#{MacOS.sdk_path}/usr/include"
    end

    args = %W[
      --prefix=#{prefix}
      --enable-ipv6
      --enable-shared
    ]
    args << '--without-gcc' if ENV.compiler == :clang

    system './configure', *args
    system 'make'
    ENV.deparallelize
    system 'make', 'install'

    ENV['PATH'] = "#{bin}:#{ENV['PATH']}"

    resource('virtualenv').stage {
      system 'python', 'setup.py', 'install'
    }

    (prefix + 'rock.yml').write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS

    runtime = var + 'rock/opt/rock/runtime'
    runtime.mkpath
    runtime += 'python27'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
