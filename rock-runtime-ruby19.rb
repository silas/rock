require 'formula'

class RockRuntimeRuby19 < Formula
  homepage 'http://www.python.org/'
  url 'http://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p392.tar.gz'
  sha1 'ec75fcbd3b6b46ce6ec997ee4c86145b4abd5748'

  env :std
  keg_only 'rock'

  depends_on 'readline'
  depends_on 'gdbm'
  depends_on 'libyaml'
  depends_on 'openssl'
  depends_on 'curl-ca-bundle'

  bottle do
    root_url 'http://dl.rockstack.org/homebrew/bottle'
    sha1 'e4aed301424b88640094dbdc267bcc26488291b9' => :mountain_lion
  end

  def abi_version
    '1.9.1'
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

    runtime = rock + 'runtime/ruby19'
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
