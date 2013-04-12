require 'formula'

class RockRuntimeRuby20 < Formula
  homepage 'http://www.python.org/'
  url 'http://ftp.ruby-lang.org/pub/ruby/2.0/ruby-2.0.0-p0.tar.gz'
  sha1 '5349078b65fdeea85c7217d0ca98e718d3612df4'

  env :std
  keg_only 'rock'

  depends_on 'readline'
  depends_on 'gdbm'
  depends_on 'libyaml'
  depends_on 'openssl'
  depends_on 'curl-ca-bundle'

  bottle do
    root_url 'http://dl.rockstack.org/homebrew/bottle'
    sha1 '86d305e7f09d1565c5d8711084ce1e4155c98311' => :mountain_lion
  end

  def abi_version
    '2.0.0'
  end

  def bundler_version
    '1.3.4'
  end

  def install_bundler
    system 'curl', '-LO', "http://rubygems.org/downloads/bundler-#{bundler_version}.gem"

    ENV['GEM_HOME'] = "#{prefix}/lib/ruby/gems/#{abi_version}"

    system 'gem', 'install',
      '--config-file', 'nofile',
      '--force',
      '--ignore-dependencies',
      '--no-rdoc',
      '--no-ri',
      '--local',
      '--install-dir', "#{prefix}/lib/ruby/gems/#{abi_version}",
      "--bindir", bin,
      "bundler-#{bundler_version}.gem"

    system 'mv', "#{bin}/bundle", "#{bin}/rock-bundle"

    (bin + 'bundle').write <<-EOS.undent
      #!/usr/bin/env bash
      unset RUBYOPT
      exec rock-bundle "$@"
    EOS

    system 'chmod', '755', "#{bin}/bundle"
  end

  def install
    rock = Pathname.new('/opt/rock')

    unless rock.directory? && rock.writable?
      onoe "#{rock} must be a directory and writable"
      exit 1
    end

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

    runtime = rock + 'runtime/ruby20'
    runtime.mkpath
    runtime += 'rock.yml'
    runtime.unlink if runtime.exist?
    runtime.write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
        RUBY_ABI: "#{abi_version}"
        RUBYOPT: "-I#{lib}/ruby/gems/#{abi_version}/gems/bundler-#{bundler_version}/lib -rbundler/setup"
        SSL_CERT_FILE: "#{Formula.factory('curl-ca-bundle').prefix}/share/ca-bundle.crt"
    EOS
  end
end
