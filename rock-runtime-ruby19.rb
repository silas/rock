require 'formula'

class RockRuntimeRuby19 < Formula
  homepage 'http://www.python.org/'
  url 'http://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p327.tar.gz'
  sha1 'a4075e5126278b5cba982d8c832dc03114e7a02a'

  env :std
  keg_only 'rock'

  depends_on 'readline'
  depends_on 'gdbm'
  depends_on 'libyaml'

  def bundler_version
    '1.1.5'
  end

  def install_bundler
    system 'curl', '-LO', "http://rubygems.org/downloads/bundler-#{bundler_version}.gem"

    ENV['GEM_HOME'] = "#{prefix}/lib/ruby/gems/1.9.1"

    system 'gem', 'install',
      '--config-file', 'nofile',
      '--force',
      '--ignore-dependencies',
      '--no-rdoc',
      '--no-ri',
      '--local',
      '--install-dir', "#{prefix}/lib/ruby/gems/1.9.1",
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
      '--enable-shared'
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
        RUBY_ABI: "1.9.1"
        RUBYOPT: "-I#{lib}/ruby/gems/1.9.1/gems/bundler-#{bundler_version}/lib -rbundler/setup"
    EOS
  end
end
