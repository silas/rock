require 'formula'

class RockRuntimeRuby18 < Formula
  homepage 'http://www.ruby-lang.org/en/'
  url 'http://ftp.ruby-lang.org/pub/ruby/1.8/ruby-1.8.7-p371.tar.gz'
  sha1 '59a19b93e1e146ad65efd8be930b9ddc5a95dd4e'

  env :std
  keg_only 'rock'

  depends_on 'readline'
  depends_on 'gdbm'
  depends_on 'libyaml'

  resource 'rubygems' do
    url 'http://production.cf.rubygems.org/rubygems/rubygems-1.8.24.tgz'
    sha1 '30f27047e74f7943117736a0d3e224994fee0905'
  end

  resource 'bundler' do
    url "https://rubygems.org/gems/bundler-1.3.4.gem"
    sha1 'fba95c4d82d4fa287de6baea99ed31af8b8973dc'
  end

  def abi_version
    '1.8'
  end

  def install_rubygems
    resource('rubygems').stage { |r|
      system 'ruby', 'setup.rb',
        "--prefix=#{prefix}",
        '--rdoc'
      system "mv #{lib}/*.rb #{lib}/ruby/1.8"
      system "mv #{lib}/{rbconfig,rubygems} #{lib}/ruby/1.8"
    }
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
      '--without-tk',
      '--enable-shared',
      "--with-readline-dir=#{Formula.factory('readline').prefix}"
    system 'make'
    system 'make', 'install'

    ENV['PATH'] = "#{bin}:#{ENV['PATH']}"

    install_rubygems
    install_bundler

    (prefix + 'rock.yml').write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
        RUBY_ABI: "#{abi_version}"
        RUBYOPT: "-I#{lib}/ruby/gems/#{abi_version}/gems/bundler-#{resource('bundler').version}/lib -rbundler/setup"
    EOS

    runtime = var + 'rock/opt/rock/runtime'
    runtime.mkpath
    runtime += 'ruby18'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
