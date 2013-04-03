require 'formula'

class RockRuntimePerl516 < Formula
  homepage 'http://www.perl.org/'
  url 'http://www.cpan.org/src/5.0/perl-5.16.3.tar.bz2'
  sha1 '060bc17cf9f142d043f9bf7b861422ec624875ea'

  keg_only 'rock'

  bottle do
    root_url 'http://dl.rockstack.org/homebrew/bottle'
    sha1 '022e1211291b6eea342af81fd6b7a0172549f335' => :mountain_lion
  end

  def install_local_lib
    local_lib_version = '1.008009'

    system 'curl', '-LO', "http://search.cpan.org/CPAN/authors/id/A/AP/APEIRON/local-lib-#{local_lib_version}.tar.gz"
    system 'tar', '-xzf', "local-lib-#{local_lib_version}.tar.gz"

    Dir.chdir "local-lib-#{local_lib_version}"

    system 'perl', 'Makefile.PL'
    system 'make', 'install'

    Dir.chdir '..'
  end

  def install_cpanm
    cpanm_version = '1.6008'

    system 'curl', '-Lo', "#{bin}/cpanm", "https://raw.github.com/miyagawa/cpanminus/#{cpanm_version}/cpanm"
    system 'chmod', '755', "#{bin}/cpanm"
  end

  def install_carton
    carton_version = '0.9.10'

    urls = [
      'http://www.cpan.org/authors/id/T/TO/TOKUHIROM/Test-Requires-0.06.tar.gz',
      'http://www.cpan.org/authors/id/D/DA/DAGOLDEN/Capture-Tiny-0.21.tar.gz',
      'http://www.cpan.org/authors/id/M/MI/MIYAGAWA/App-cpanminus-1.6008.tar.gz',
      'http://www.cpan.org/authors/id/D/DA/DAGOLDEN/CPAN-Meta-YAML-0.008.tar.gz',
      'http://www.cpan.org/authors/id/M/MI/MIYAGAWA/Module-CPANfile-0.9010.tar.gz',
      'http://www.cpan.org/authors/id/D/DA/DAGOLDEN/Parse-CPAN-Meta-1.4404.tar.gz',
      'http://www.cpan.org/authors/id/D/DA/DAGOLDEN/CPAN-Meta-Requirements-2.122.tar.gz',
      'http://www.cpan.org/authors/id/D/DA/DAGOLDEN/CPAN-Meta-2.120921.tar.gz',
      'http://www.cpan.org/authors/id/T/TM/TMTM/Class-Data-Inheritable-0.08.tar.gz',
      'http://www.cpan.org/authors/id/D/DR/DROLSKY/Devel-StackTrace-1.30.tar.gz',
      'http://www.cpan.org/authors/id/D/DR/DROLSKY/Exception-Class-1.37.tar.gz',
      'http://www.cpan.org/authors/id/M/ML/MLEHMANN/common-sense-3.6.tar.gz',
      'http://www.cpan.org/authors/id/M/ML/MLEHMANN/JSON-XS-2.33.tar.gz',
      'http://www.cpan.org/authors/id/M/MA/MAKAMAKA/JSON-2.53.tar.gz',
      'http://www.cpan.org/authors/id/D/DO/DOY/Try-Tiny-0.12.tar.gz',
      'http://www.cpan.org/authors/id/A/AP/APEIRON/local-lib-1.008009.tar.gz',
      "http://www.cpan.org/authors/id/M/MI/MIYAGAWA/carton-v#{carton_version}.tar.gz",
    ]

    system 'cpanm', '-l', 'local', *urls

    system 'mv', 'local', "#{prefix}/lib/carton"

    (bin + 'carton').write <<-EOS.undent
      #!/usr/bin/env bash
      perl -Mlocal::lib=#{prefix}/lib/carton #{prefix}/lib/carton/bin/carton "$@"
    EOS

    system 'chmod', '755', "#{bin}/carton"
  end

  def install
    rock = Pathname.new('/opt/rock')

    unless rock.directory? && rock.writable?
      onoe "#{rock} must be a directory and writable"
      exit 1
    end

    archname='darwin-thread-multi-2level'

    system './Configure', '-des',
      "-Dprefix=#{prefix}",
      "-Dvendorprefix=#{prefix}",
      "-Dsiteprefix=#{prefix}/local",
      "-Dsitelib=#{prefix}/local/share/perl5",
      "-Dsitearch=#{prefix}/local/lib/perl5",
      "-Dprivlib=#{prefix}/share/perl5",
      "-Dvendorlib=#{prefix}/share/perl5",
      "-Darchlib=#{prefix}/lib/perl5",
      "-Dvendorarch=#{prefix}/lib/perl5/vendor_perl",
      "-Darchname=#{archname}",
      '-Dman3ext=3pm',
      '-Dusethreads',
      '-Duseithreads',
      '-Duselargefiles',
      '-Duseperl'

    system 'make'
    system 'make', 'install'

    ENV['PATH'] = "#{bin}:#{ENV['PATH']}"

    install_local_lib
    install_cpanm
    install_carton

    runtime = rock + 'runtime/perl516'
    runtime.mkpath
    runtime += 'rock.yml'
    runtime.unlink if runtime.exist?
    runtime.write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
        PERL_ARCHNAME: "#{archname}"
    EOS
  end
end
