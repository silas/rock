require 'formula'

class RockRuntimePerl518 < Formula
  homepage 'http://www.perl.org/'
  url 'http://www.cpan.org/src/5.0/perl-5.18.1.tar.bz2'
  sha1 'eb6b402682168a9735b2806d09c1ca5d567b2de8'

  keg_only 'rock'

  def install_local_lib
    local_lib_version = '1.008023'

    system 'curl', '-LO', "http://www.cpan.org/authors/id/E/ET/ETHER/local-lib-#{local_lib_version}.tar.gz"
    system 'tar', '-xzf', "local-lib-#{local_lib_version}.tar.gz"

    Dir.chdir "local-lib-#{local_lib_version}"

    system 'perl', 'Makefile.PL'
    system 'make', 'install'

    Dir.chdir '..'
  end

  def install_cpanm
    cpanm_version = '1.7001'

    system 'curl', '-Lo', "#{bin}/cpanm", "https://raw.github.com/miyagawa/cpanminus/#{cpanm_version}/cpanm"
    system 'chmod', '755', "#{bin}/cpanm"
  end

  def install_carton
    carton_version = '1.0.12'

    url = 'http://www.cpan.org/authors/id'

    urls = [
      "#{url}/G/GA/GAAS/WWW-RobotRules-6.02.tar.gz",
      "#{url}/G/GA/GAAS/HTTP-Cookies-6.01.tar.gz",
      "#{url}/G/GA/GAAS/Net-HTTP-6.06.tar.gz",
      "#{url}/G/GA/GAAS/HTTP-Daemon-6.01.tar.gz",
      "#{url}/P/PE/PETDANCE/HTML-Tagset-3.20.tar.gz",
      "#{url}/G/GA/GAAS/HTML-Parser-3.71.tar.gz",
      "#{url}/G/GA/GAAS/HTTP-Negotiate-6.01.tar.gz",
      "#{url}/G/GA/GAAS/File-Listing-6.04.tar.gz",
      "#{url}/G/GA/GAAS/HTTP-Date-6.02.tar.gz",
      "#{url}/C/CJ/CJM/IO-HTML-1.00.tar.gz",
      "#{url}/G/GA/GAAS/HTTP-Message-6.06.tar.gz",
      "#{url}/G/GA/GAAS/Encode-Locale-1.03.tar.gz",
      "#{url}/G/GA/GAAS/LWP-MediaTypes-6.02.tar.gz",
      "#{url}/G/GA/GAAS/URI-1.60.tar.gz",
      "#{url}/G/GA/GAAS/libwww-perl-6.05.tar.gz",
      "#{url}/M/MA/MAKAMAKA/JSON-2.90.tar.gz",
      "#{url}/M/MI/MIYAGAWA/Module-CPANfile-1.0002.tar.gz",
      "#{url}/T/TM/TMTM/Class-Data-Inheritable-0.08.tar.gz",
      "#{url}/D/DR/DROLSKY/Devel-StackTrace-1.30.tar.gz",
      "#{url}/D/DR/DROLSKY/Exception-Class-1.37.tar.gz",
      "#{url}/H/HA/HAARG/Module-Reader-0.002000.tar.gz",
      "#{url}/M/MI/MIYAGAWA/App-cpanminus-1.7001.tar.gz",
      "#{url}/F/FR/FREW/Sub-Exporter-Progressive-0.001011.tar.gz",
      "#{url}/H/HA/HAARG/Devel-GlobalDestruction-0.12.tar.gz",
      "#{url}/L/LE/LEONT/ExtUtils-Config-0.007.tar.gz",
      "#{url}/L/LE/LEONT/ExtUtils-InstallPaths-0.010.tar.gz",
      "#{url}/L/LE/LEONT/ExtUtils-Helpers-0.021.tar.gz",
      "#{url}/O/OV/OVID/Test-Harness-3.29.tar.gz",
      "#{url}/L/LE/LEONT/Module-Build-Tiny-0.030.tar.gz",
      "#{url}/E/ET/ETHER/Class-Method-Modifiers-2.08.tar.gz",
      "#{url}/H/HA/HAARG/Role-Tiny-1.003002.tar.gz",
      "#{url}/E/ET/ETHER/strictures-1.004004.tar.gz",
      "#{url}/A/AD/ADAMK/List-MoreUtils-0.33.tar.gz",
      "#{url}/Z/ZE/ZEFRAM/Module-Runtime-0.013.tar.gz",
      "#{url}/R/RJ/RJBS/Test-Fatal-0.013.tar.gz",
      "#{url}/D/DO/DOY/Dist-CheckConflicts-0.09.tar.gz",
      "#{url}/M/MS/MSTROUT/Moo-1.003001.tar.gz",
      "#{url}/B/BI/BINGOS/ExtUtils-MakeMaker-6.80.tar.gz",
      "#{url}/D/DA/DAGOLDEN/File-pushd-1.005.tar.gz",
      "#{url}/J/JV/JV/Getopt-Long-2.42.tar.gz",
      "#{url}/D/DO/DOY/Try-Tiny-0.18.tar.gz",
      "#{url}/S/SM/SMUELLER/PathTools-3.40.tar.gz",
      "#{url}/D/DA/DAGOLDEN/Path-Tiny-0.044.tar.gz",
      "#{url}/L/LE/LEONT/Module-Build-0.4007.tar.gz",
      "#{url}/D/DA/DAGOLDEN/CPAN-Meta-Requirements-2.125.tar.gz",
      "#{url}/D/DA/DAGOLDEN/CPAN-Meta-YAML-0.010.tar.gz",
      "#{url}/D/DA/DAGOLDEN/Parse-CPAN-Meta-1.4409.tar.gz",
      "#{url}/D/DA/DAGOLDEN/CPAN-Meta-2.132830.tar.gz",
      "#{url}/E/ET/ETHER/App-FatPacker-0.009018.tar.gz",
      "#{url}/M/MI/MIYAGAWA/Carton-v#{carton_version}.tar.gz",
    ]

    home = ENV['HOME']
    ENV['HOME'] = Dir.getwd

    system 'cpanm', '-l', 'local', '--notest', *urls

    ENV['HOME'] = home

    system 'mv', 'local', "#{prefix}/lib/carton"

    (bin + 'carton').write <<-EOS.undent
      #!/usr/bin/env bash
      perl -Mlocal::lib=#{prefix}/lib/carton #{prefix}/lib/carton/bin/carton "$@"
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

    (prefix + 'rock.yml').write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
        PERL_ARCHNAME: "#{archname}"
    EOS

    runtime = var + 'rock/opt/rock/runtime'
    runtime.mkpath
    runtime += 'perl518'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
