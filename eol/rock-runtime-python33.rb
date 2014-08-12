require 'formula'

class RockRuntimePython33 < Formula
  homepage 'http://www.python.org/'
  url 'http://www.python.org/ftp/python/3.3.3/Python-3.3.3.tgz'
  sha1 '6c1e974bb40f6e0554d4fe665a864f31ae54e9d5'

  env :std
  keg_only 'rock'

  resource 'distribute' do
    url 'https://bitbucket.org/tarek/distribute/raw/0.6.36/distribute_setup.py'
    sha1 '69561619041d9814e747596747d58c121fe2d996'
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

    File.symlink("#{bin}/python3", "#{bin}/python")

    ENV['PATH'] = "#{bin}:#{ENV['PATH']}"

    resource('distribute').stage {
      system "sed 's|#!python|#!/usr/bin/env python|g' distribute_setup.py > #{bin}/distribute-setup"
      system 'chmod', '755', "#{bin}/distribute-setup"
    }

    (prefix + 'rock.yml').write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS

    runtime = var + 'rock/opt/rock/runtime'
    runtime.mkpath
    runtime += 'python33'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
