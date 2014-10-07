%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

%global cpan_url http://backpan.cpan.org/authors/id

Name:           rock-runtime-perl518-carton
Version:        1.0.12
Release:        1%{?dist}
Summary:        A tool to manage Perl 5.18.x dependencies

Group:          Development/Languages
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
URL:            http://search.cpan.org/dist/carton/
Source0:        %{cpan_url}/G/GA/GAAS/WWW-RobotRules-6.02.tar.gz
Source1:        %{cpan_url}/G/GA/GAAS/HTTP-Cookies-6.01.tar.gz
Source2:        %{cpan_url}/G/GA/GAAS/Net-HTTP-6.06.tar.gz
Source3:        %{cpan_url}/G/GA/GAAS/HTTP-Daemon-6.01.tar.gz
Source4:        %{cpan_url}/P/PE/PETDANCE/HTML-Tagset-3.20.tar.gz
Source5:        %{cpan_url}/G/GA/GAAS/HTML-Parser-3.71.tar.gz
Source6:        %{cpan_url}/G/GA/GAAS/HTTP-Negotiate-6.01.tar.gz
Source7:        %{cpan_url}/G/GA/GAAS/File-Listing-6.04.tar.gz
Source8:        %{cpan_url}/G/GA/GAAS/HTTP-Date-6.02.tar.gz
Source9:        %{cpan_url}/C/CJ/CJM/IO-HTML-1.00.tar.gz
Source10:       %{cpan_url}/G/GA/GAAS/HTTP-Message-6.06.tar.gz
Source11:       %{cpan_url}/G/GA/GAAS/Encode-Locale-1.03.tar.gz
Source12:       %{cpan_url}/G/GA/GAAS/LWP-MediaTypes-6.02.tar.gz
Source13:       %{cpan_url}/G/GA/GAAS/URI-1.60.tar.gz
Source14:       %{cpan_url}/G/GA/GAAS/libwww-perl-6.05.tar.gz
Source15:       %{cpan_url}/M/MA/MAKAMAKA/JSON-2.90.tar.gz
Source16:       %{cpan_url}/M/MI/MIYAGAWA/Module-CPANfile-1.0002.tar.gz
Source17:       %{cpan_url}/T/TM/TMTM/Class-Data-Inheritable-0.08.tar.gz
Source18:       %{cpan_url}/D/DR/DROLSKY/Devel-StackTrace-1.30.tar.gz
Source19:       %{cpan_url}/D/DR/DROLSKY/Exception-Class-1.37.tar.gz
Source20:       %{cpan_url}/H/HA/HAARG/Module-Reader-0.002000.tar.gz
Source21:       %{cpan_url}/M/MI/MIYAGAWA/App-cpanminus-1.7001.tar.gz
Source22:       %{cpan_url}/F/FR/FREW/Sub-Exporter-Progressive-0.001011.tar.gz
Source23:       %{cpan_url}/H/HA/HAARG/Devel-GlobalDestruction-0.12.tar.gz
Source24:       %{cpan_url}/L/LE/LEONT/ExtUtils-Config-0.007.tar.gz
Source25:       %{cpan_url}/L/LE/LEONT/ExtUtils-InstallPaths-0.010.tar.gz
Source26:       %{cpan_url}/L/LE/LEONT/ExtUtils-Helpers-0.021.tar.gz
Source27:       %{cpan_url}/O/OV/OVID/Test-Harness-3.29.tar.gz
Source28:       %{cpan_url}/L/LE/LEONT/Module-Build-Tiny-0.030.tar.gz
Source29:       %{cpan_url}/E/ET/ETHER/Class-Method-Modifiers-2.08.tar.gz
Source30:       %{cpan_url}/H/HA/HAARG/Role-Tiny-1.003002.tar.gz
Source31:       %{cpan_url}/E/ET/ETHER/strictures-1.004004.tar.gz
Source32:       %{cpan_url}/A/AD/ADAMK/List-MoreUtils-0.33.tar.gz
Source33:       %{cpan_url}/Z/ZE/ZEFRAM/Module-Runtime-0.013.tar.gz
Source34:       %{cpan_url}/R/RJ/RJBS/Test-Fatal-0.013.tar.gz
Source35:       %{cpan_url}/D/DO/DOY/Dist-CheckConflicts-0.09.tar.gz
Source36:       %{cpan_url}/M/MS/MSTROUT/Moo-1.003001.tar.gz
Source37:       %{cpan_url}/B/BI/BINGOS/ExtUtils-MakeMaker-6.80.tar.gz
Source38:       %{cpan_url}/D/DA/DAGOLDEN/File-pushd-1.005.tar.gz
Source39:       %{cpan_url}/J/JV/JV/Getopt-Long-2.42.tar.gz
Source40:       %{cpan_url}/D/DO/DOY/Try-Tiny-0.18.tar.gz
Source41:       %{cpan_url}/S/SM/SMUELLER/PathTools-3.40.tar.gz
Source42:       %{cpan_url}/D/DA/DAGOLDEN/Path-Tiny-0.044.tar.gz
Source43:       %{cpan_url}/L/LE/LEONT/Module-Build-0.4007.tar.gz
Source44:       %{cpan_url}/D/DA/DAGOLDEN/CPAN-Meta-Requirements-2.125.tar.gz
Source45:       %{cpan_url}/D/DA/DAGOLDEN/CPAN-Meta-YAML-0.010.tar.gz
Source46:       %{cpan_url}/D/DA/DAGOLDEN/Parse-CPAN-Meta-1.4409.tar.gz
Source47:       %{cpan_url}/D/DA/DAGOLDEN/CPAN-Meta-2.132830.tar.gz
Source48:       %{cpan_url}/E/ET/ETHER/App-FatPacker-0.009018.tar.gz
Source49:       %{cpan_url}/M/MI/MIYAGAWA/Carton-v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  rock-runtime-perl518-core-rpmbuild >= 5.18.1-1
BuildRequires:  rock-runtime-perl518-cpanm
Requires:       rock-runtime-perl518-core >= 5.18.1-1

%description
carton is a command line tool to track the Perl module dependencies for your
Perl application. The managed dependencies are tracked in a carton.lock file,
which is meant to be version controlled, and the lock file allows other
developers of your application will have the exact same versions of the
modules.

%prep

%build
export PATH="%{perl518_rootdir}%{_bindir}:$PATH"

cpanm -l local --notest \
    %{SOURCE0} \
    %{SOURCE1} \
    %{SOURCE2} \
    %{SOURCE3} \
    %{SOURCE4} \
    %{SOURCE5} \
    %{SOURCE6} \
    %{SOURCE7} \
    %{SOURCE8} \
    %{SOURCE9} \
    %{SOURCE10} \
    %{SOURCE11} \
    %{SOURCE12} \
    %{SOURCE13} \
    %{SOURCE14} \
    %{SOURCE15} \
    %{SOURCE16} \
    %{SOURCE17} \
    %{SOURCE18} \
    %{SOURCE19} \
    %{SOURCE20} \
    %{SOURCE21} \
    %{SOURCE22} \
    %{SOURCE23} \
    %{SOURCE24} \
    %{SOURCE25} \
    %{SOURCE26} \
    %{SOURCE27} \
    %{SOURCE28} \
    %{SOURCE29} \
    %{SOURCE30} \
    %{SOURCE31} \
    %{SOURCE32} \
    %{SOURCE33} \
    %{SOURCE34} \
    %{SOURCE35} \
    %{SOURCE36} \
    %{SOURCE37} \
    %{SOURCE38} \
    %{SOURCE39} \
    %{SOURCE40} \
    %{SOURCE41} \
    %{SOURCE42} \
    %{SOURCE43} \
    %{SOURCE44} \
    %{SOURCE45} \
    %{SOURCE46} \
    %{SOURCE47} \
    %{SOURCE48} \
    %{SOURCE49}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{perl518_rootdir}%{_bindir} \
         %{buildroot}%{perl518_rootdir}%{_prefix}/lib

mv local %{buildroot}%{perl518_rootdir}%{_prefix}/lib/carton

cat << EOF > %{buildroot}%{perl518_rootdir}%{_bindir}/carton
#!/usr/bin/env bash

perl \
  -Mlocal::lib=%{perl518_rootdir}%{_prefix}/lib/carton \
  %{perl518_rootdir}%{_prefix}/lib/carton/bin/carton "\$@"
EOF

chmod 755 %{buildroot}%{perl518_rootdir}%{_bindir}/carton

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl518_rootdir}%{_bindir}/carton
%{perl518_rootdir}%{_prefix}/lib/carton

%changelog
* Thu Oct 31 2013 RockStack <packages@rockstack.org> - 1.0.12-1
- Initial build
