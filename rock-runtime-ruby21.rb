require 'formula'

class RockRuntimeRuby21 < Formula
  homepage 'http://www.python.org/'
  url 'http://ftp.ruby-lang.org/pub/ruby/2.1/ruby-2.1.0.tar.gz'
  sha1 '99114e71c7765b5bdc0414c189a338f6f21fb51d'

  env :std
  keg_only 'rock'

  # https://github.com/rubygems/rubygems/commit/f5bbf838c8b13369a61c6756355305388df5824f
  def patches; DATA; end

  depends_on 'readline'
  depends_on 'gdbm'
  depends_on 'libyaml'
  depends_on 'openssl'
  depends_on 'curl-ca-bundle'

  resource 'bundler' do
    url 'https://rubygems.org/gems/bundler-1.5.2.gem'
    sha1 '78a9fe1161407778f437fae39cb5ac51127f4635'
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
        SSL_CERT_FILE: "#{Formula.factory('curl-ca-bundle').prefix}/share/ca-bundle.crt"
    EOS

    runtime = var + 'rock/opt/rock/runtime'
    runtime.mkpath
    runtime += 'ruby21'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end

__END__
diff -ru ruby-2.1.0.orig/lib/rubygems/commands/install_command.rb ruby-2.1.0/lib/rubygems/commands/install_command.rb
--- ruby-2.1.0.orig/lib/rubygems/commands/install_command.rb	2014-02-01 13:34:30.000000000 -0800
+++ ruby-2.1.0/lib/rubygems/commands/install_command.rb	2014-02-01 13:35:58.000000000 -0800
@@ -228,7 +228,18 @@
   def install_gem_without_dependencies name, req # :nodoc:
     gem = nil
 
-    if remote? then
+    if local? then
+      if name =~ /\.gem$/ and File.file? name then
+        source = Gem::Source::SpecificFile.new name
+        spec = source.spec
+      else
+        source = Gem::Source::Local.new
+        spec = source.find_gem name, req
+      end
+      gem = source.download spec if spec
+    end
+
+    if remote? and not gem then
       dependency = Gem::Dependency.new name, req
       dependency.prerelease = options[:prerelease]
 
@@ -236,13 +247,6 @@
       gem = fetcher.download_to_cache dependency
     end
 
-    if local? and not gem then
-      source = Gem::Source::Local.new
-      spec = source.find_gem name, req
-
-      gem = source.download spec
-    end
-
     inst = Gem::Installer.new gem, options
     inst.install
 
diff -ru ruby-2.1.0.orig/test/rubygems/test_gem_commands_install_command.rb ruby-2.1.0/test/rubygems/test_gem_commands_install_command.rb
--- ruby-2.1.0.orig/test/rubygems/test_gem_commands_install_command.rb	2014-02-01 13:34:30.000000000 -0800
+++ ruby-2.1.0/test/rubygems/test_gem_commands_install_command.rb	2014-02-01 13:35:58.000000000 -0800
@@ -559,6 +559,20 @@
     assert_equal %w[a-2], @cmd.installed_specs.map { |spec| spec.full_name }
   end
 
+  def test_install_gem_ignore_dependencies_specific_file
+    spec = quick_spec 'a', 2
+
+    util_build_gem spec
+
+    FileUtils.mv spec.cache_file, @tempdir
+
+    @cmd.options[:ignore_dependencies] = true
+
+    @cmd.install_gem File.join(@tempdir, spec.file_name), nil
+
+    assert_equal %w[a-2], @cmd.installed_specs.map { |spec| spec.full_name }
+  end
+
   def test_parses_requirement_from_gemname
     spec_fetcher do |fetcher|
       fetcher.gem 'a', 2
Only in ruby-2.1.0/test/rubygems: test_gem_commands_install_command.rb.orig
