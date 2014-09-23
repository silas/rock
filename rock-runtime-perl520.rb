require 'formula'

class RockRuntimePerl520 < Formula
  homepage 'http://www.perl.org/'
  url 'http://www.cpan.org/src/5.0/perl-5.20.1.tar.bz2'
  sha1 'cd424d1520ba2686fe5d4422565aaf880e9467f6'

  keg_only 'rock'

  def install_local_lib
    local_lib_version = '2.000012'

    system 'curl', '-LO', "http://search.cpan.org/CPAN/authors/id/H/HA/HAARG/local-lib-#{local_lib_version}.tar.gz"
    system 'tar', '-xzf', "local-lib-#{local_lib_version}.tar.gz"

    Dir.chdir "local-lib-#{local_lib_version}"

    system 'perl', 'Makefile.PL'
    system 'make', 'install'

    Dir.chdir '..'
  end

  def install_cpanm
    cpanm_version = '1.7102'

    system 'curl', '-Lo', "#{bin}/cpanm", "https://raw.github.com/miyagawa/cpanminus/#{cpanm_version}/cpanm"
    system 'chmod', '755', "#{bin}/cpanm"
  end

  def install_carton
    carton_version = '1.0.12'

    url = 'http://www.cpan.org/authors/id'

    urls = [
      "#{url}/D/DA/DAGOLDEN/File-pushd-1.009.tar.gz",
      "#{url}/H/HA/HAARG/Module-Reader-0.002001.tar.gz",
      "#{url}/M/MS/MSTROUT/App-FatPacker-0.010001.tar.gz",
      "#{url}/M/MA/MAKAMAKA/JSON-2.90.tar.gz",
      "#{url}/D/DO/DOY/Try-Tiny-0.22.tar.gz",
      "#{url}/T/TM/TMTM/Class-Data-Inheritable-0.08.tar.gz",
      "#{url}/D/DR/DROLSKY/Devel-StackTrace-1.34.tar.gz",
      "#{url}/D/DR/DROLSKY/Exception-Class-1.38.tar.gz",
      "#{url}/D/DA/DAGOLDEN/Path-Tiny-0.056.tar.gz",
      "#{url}/M/MI/MIYAGAWA/Module-CPANfile-1.0002.tar.gz",
      "#{url}/T/TS/TSCH/ExtUtils-Depends-0.400.tar.gz",
      "#{url}/L/LE/LEONT/Module-Build-0.4206.tar.gz",
      "#{url}/Z/ZE/ZEFRAM/B-Hooks-OP-Check-0.19.tar.gz",
      "#{url}/Z/ZE/ZEFRAM/Lexical-SealRequireHints-0.007.tar.gz",
      "#{url}/V/VP/VPIT/indirect-0.31.tar.gz",
      "#{url}/I/IL/ILMARI/bareword-filehandles-0.003.tar.gz",
      "#{url}/I/IL/ILMARI/multidimensional-0.011.tar.gz",
      "#{url}/H/HA/HAARG/strictures-1.005004.tar.gz",
      "#{url}/Z/ZE/ZEFRAM/Module-Runtime-0.014.tar.gz",
      "#{url}/E/ET/ETHER/Import-Into-1.002004.tar.gz",
      "#{url}/E/ET/ETHER/Class-Method-Modifiers-2.10.tar.gz",
      "#{url}/H/HA/HAARG/Role-Tiny-1.003003.tar.gz",
      "#{url}/F/FR/FREW/Sub-Exporter-Progressive-0.001011.tar.gz",
      "#{url}/H/HA/HAARG/Devel-GlobalDestruction-0.12.tar.gz",
      "#{url}/H/HA/HAARG/Moo-1.005000.tar.gz",
      "#{url}/M/MI/MIYAGAWA/App-cpanminus-1.7004.tar.gz",
      "#{url}/M/MI/MIYAGAWA/Carton-v#{carton_version}.tar.gz",
    ]

    home = ENV['HOME']
    ENV['HOME'] = Dir.getwd

    system 'cpanm', '-l', 'local', '--notest', *urls

    ENV['HOME'] = home

    system 'mv', 'local', "#{lib}/carton"

    (bin + 'carton').write <<-EOS.undent
      #!/usr/bin/env bash
      perl -Mlocal::lib=#{lib}/carton #{lib}/carton/bin/carton "$@"
    EOS

    system 'chmod', '755', "#{bin}/carton"
  end

  def install
    archname='darwin-thread-multi-2level'

    system './Configure', '-des',
      "-Dprefix=#{prefix}",
      "-Dvendorprefix=#{prefix}",
      "-Dsiteprefix=#{prefix}/local",
      "-Dsitelib=#{prefix}/local/share/perl5",
      "-Dsitearch=#{prefix}/local/lib/perl5",
      "-Dprivlib=#{share}/perl5",
      "-Dvendorlib=#{share}/perl5",
      "-Darchlib=#{lib}/perl5",
      "-Dvendorarch=#{lib}/perl5/vendor_perl",
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

    (prefix + 'rock.yml').write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
        PERL_ARCHNAME: "#{archname}"
    EOS

    runtime = var + 'rock/opt/rock/runtime'
    runtime.mkpath
    runtime += 'perl520'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
