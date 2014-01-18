require 'formula'

class RockRuntimeRuby20 < Formula
  homepage 'http://www.python.org/'
  url 'http://ftp.ruby-lang.org/pub/ruby/2.0/ruby-2.0.0-p353.tar.gz'
  sha1 '7f2c8b8f5682aabc1114f44d36d314c6c37c11b8'

  env :std
  keg_only 'rock'

  depends_on 'readline'
  depends_on 'gdbm'
  depends_on 'libyaml'
  depends_on 'openssl'
  depends_on 'curl-ca-bundle'

  resource 'bundler' do
    url "https://rubygems.org/gems/bundler-1.3.4.gem"
    sha1 'fba95c4d82d4fa287de6baea99ed31af8b8973dc'
  end

  def abi_version
    '2.0.0'
  end

  def install_bundler
    ENV['GEM_HOME'] = "#{prefix}/lib/ruby/gems/#{abi_version}"

    resource('bundler').stage { |r|
      system 'gem', 'install',
        '--config-file', 'nofile',
        '--force',
        '--ignore-dependencies',
        '--no-rdoc',
        '--no-ri',
        '--local',
        '--install-dir', "#{prefix}/lib/ruby/gems/#{abi_version}",
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
      "--with-openssl-dir=#{Formula.factory('openssl').prefix}",
      "--with-readline-dir=#{Formula.factory('readline').prefix}"
    system 'make'
    system 'make', 'install'

    ENV['PATH'] = "#{bin}:#{ENV['PATH']}"

    install_bundler

    (prefix + 'rock.yml').write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
        RUBY_ABI: "#{abi_version}"
        RUBYOPT: "-I#{lib}/ruby/gems/#{abi_version}/gems/bundler-#{resource('bundler').version}/lib -rbundler/setup"
        SSL_CERT_FILE: "#{Formula.factory('curl-ca-bundle').prefix}/share/ca-bundle.crt"
    EOS

    runtime = var + 'rock/opt/rock/runtime'
    runtime.mkpath
    runtime += 'ruby20'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
