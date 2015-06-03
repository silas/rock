require "formula"

class RockRuntimeRuby22 < Formula
  homepage "https://www.ruby-lang.org/"
  url "https://ftp.ruby-lang.org/pub/ruby/2.2/ruby-2.2.0.tar.gz"
  sha256 "7671e394abfb5d262fbcd3b27a71bf78737c7e9347fa21c39e58b0bb9c4840fc"

  env :std
  keg_only "rock"

  depends_on "readline"
  depends_on "gdbm"
  depends_on "libyaml"
  depends_on "openssl"

  resource "bundler" do
    url "https://rubygems.org/gems/bundler-1.8.2.gem"
    sha256 "342da88174d60adbcb30217325c72f6974d812355dcd6fb3acc001dfcab4485e"
  end

  def abi_version
    "2.2.0"
  end

  def install_bundler
    ENV["GEM_HOME"] = "#{lib}/ruby/gems/#{abi_version}"

    resource("bundler").stage { |r|
      system "gem", "install",
        "--config-file", "nofile",
        "--force",
        "--ignore-dependencies",
        "--no-rdoc",
        "--no-ri",
        "--local",
        "--install-dir", "#{lib}/ruby/gems/#{abi_version}",
        "--bindir", bin,
        r.cached_download
    }

    system "mv", "#{bin}/bundle", "#{bin}/rock-bundle"

    (bin + "bundle").write <<-EOS.undent
      #!/usr/bin/env bash
      unset RUBYOPT
      exec rock-bundle "$@"
    EOS

    system "chmod", "755", "#{bin}/bundle"
  end

  def install
    lib.mkpath

    system "./configure",
      "--prefix=#{prefix}",
      "--enable-shared",
      "--with-opt-dir=#{Formula.factory("openssl").opt_prefix}",
      "--with-opt-dir=#{Formula.factory("readline").prefix}"
    system "make"
    system "make", "install"

    ENV["PATH"] = "#{bin}:#{ENV["PATH"]}"

    install_bundler

    (prefix + "rock.yml").write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
        RUBY_ABI: "#{abi_version}"
        RUBYOPT: "-I#{lib}/ruby/gems/#{abi_version}/gems/bundler-#{resource("bundler").version}/lib -rbundler/setup"
    EOS

    runtime = var + "rock/opt/rock/runtime"
    runtime.mkpath
    runtime += "ruby22"
    system "rm", "-fr", runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
