require 'formula'

class RockRuntimePython34 < Formula
  homepage 'http://www.python.org/'
  url 'http://www.python.org/ftp/python/3.4.1/Python-3.4.1.tgz'
  sha1 'e8c1bd575a6ccc2a75f79d9d094a6a29d3802f5d'

  env :std
  keg_only 'rock'

  resource 'virtualenv' do
    url 'https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.11.6.tar.gz'
    sha1 'd3f8e94bf825cc999924e276c8f1c63b8eeb0715'
  end

  def install
    ENV.append 'EXTRA_CFLAGS', '-fwrapv'

    if ENV.compiler == :clang
      ENV.append_to_cflags '-Wno-unused-value'
      ENV.append_to_cflags '-Wno-empty-body'
      ENV.append_to_cflags '-Qunused-arguments'
    else
      ENV.append 'LDFLAGS', "-Wl,-rpath #{lib}"
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
      system 'python3', 'setup.py', 'install'
    }

    (prefix + 'rock.yml').write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS

    runtime = var + 'rock/opt/rock/runtime'
    runtime.mkpath
    runtime += 'python34'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
