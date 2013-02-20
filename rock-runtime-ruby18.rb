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

  def rubygems_version
    '1.8.24'
  end

  def bundler_version
    '1.2.3'
  end

  def install_rubygems
    system 'curl', '-LO', "http://production.cf.rubygems.org/rubygems/rubygems-#{rubygems_version}.tgz"
    system 'tar', '-xzf', "rubygems-#{rubygems_version}.tgz"

    Dir.chdir "rubygems-#{rubygems_version}"

    system 'ruby', 'setup.rb',
      "--prefix=#{prefix}",
      '--rdoc'

    system "mv #{prefix}/lib/*.rb #{prefix}/lib/ruby/1.8"
    system "mv #{prefix}/lib/{rbconfig,rubygems} #{prefix}/lib/ruby/1.8"

    Dir.chdir '..'
  end

  def install_bundler
    system 'curl', '-LO', "http://rubygems.org/downloads/bundler-#{bundler_version}.gem"

    ENV['GEM_HOME'] = "#{prefix}/lib/ruby/gems/1.8"

    system 'gem', 'install',
      '--config-file', 'nofile',
      '--force',
      '--ignore-dependencies',
      '--no-rdoc',
      '--no-ri',
      '--local',
      '--install-dir', "#{prefix}/lib/ruby/gems/1.8",
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
      '--without-tk',
      '--enable-shared'
    system 'make'
    system 'make', 'install'

    ENV['PATH'] = "#{bin}:#{ENV['PATH']}"

    install_rubygems
    install_bundler

    runtime = rock + 'runtime/ruby18'
    runtime.mkpath
    runtime += 'rock.yml'
    runtime.unlink if runtime.exist?
    runtime.write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
        RUBY_ABI: "1.8"
        RUBYOPT: "-I#{lib}/ruby/gems/1.8/gems/bundler-#{bundler_version}/lib -rbundler/setup"
    EOS
  end
end
