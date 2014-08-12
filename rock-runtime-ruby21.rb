require 'formula'

class RockRuntimeRuby21 < Formula
  homepage 'http://www.python.org/'
  url 'http://ftp.ruby-lang.org/pub/ruby/2.1/ruby-2.1.2.tar.gz'
  sha1 'b818d56b4638f1949239038623b761517d4a5686'

  env :std
  keg_only 'rock'

  depends_on 'readline'
  depends_on 'gdbm'
  depends_on 'libyaml'
  depends_on 'openssl'

  resource 'bundler' do
    url 'https://rubygems.org/gems/bundler-1.6.5.gem'
    sha1 'e2d879350fcc417c5b8868bc52ab9309f0a7fae6'
  end

  def abi_version
    '2.1.0'
  end

  def install_bundler
    ENV['GEM_HOME'] = "#{lib}/ruby/gems/#{abi_version}"

    resource('bundler').stage { |r|
      system 'gem', 'install',
        '--config-file', 'nofile',
        '--force',
        '--ignore-dependencies',
        '--no-rdoc',
        '--no-ri',
        '--local',
        '--install-dir', "#{lib}/ruby/gems/#{abi_version}",
        "--bindir", bin,
        r.cached_download
    }

    system 'mv', "#{bin}/bundle", "#{bin}/rock-bundle"

    (bin + 'bundle').write <<-EOS.undent
      #!/usr/bin/env bash
      unset RUBYOPT
      exec rock-bundle "$@"
    EOS

    system 'chmod', '755', "#{bin}/bundle"
  end

  def install
    lib.mkpath

    system './configure',
      "--prefix=#{prefix}",
      '--enable-shared',
      "--with-opt-dir=#{Formula.factory('openssl').opt_prefix}",
      "--with-opt-dir=#{Formula.factory('readline').prefix}"
    system 'make'
    system 'make', 'install'

    ENV['PATH'] = "#{bin}:#{ENV['PATH']}"

    install_bundler

    (prefix + 'rock.yml').write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
        RUBY_ABI: "#{abi_version}"
        RUBYOPT: "-I#{lib}/ruby/gems/#{abi_version}/gems/bundler-#{resource('bundler').version}/lib -rbundler/setup"
    EOS

    runtime = var + 'rock/opt/rock/runtime'
    runtime.mkpath
    runtime += 'ruby21'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
