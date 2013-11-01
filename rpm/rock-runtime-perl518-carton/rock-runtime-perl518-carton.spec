%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

Name:           rock-runtime-perl518-carton
Version:        1.0.12
Release:        1%{?dist}
Summary:        A tool to manage Perl 5.18.x dependencies

Group:          Development/Languages
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
URL:            http://search.cpan.org/dist/carton/
Source0:        http://www.cpan.org/authors/id/L/LE/LEONT/ExtUtils-InstallPaths-0.010.tar.gz
Source1:        http://www.cpan.org/authors/id/L/LE/LEONT/ExtUtils-Helpers-0.021.tar.gz
Source2:        http://www.cpan.org/authors/id/L/LE/LEONT/ExtUtils-Config-0.007.tar.gz
Source3:        http://www.cpan.org/authors/id/O/OV/OVID/Test-Harness-3.29.tar.gz
Source4:        http://www.cpan.org/authors/id/L/LE/LEONT/Module-Build-Tiny-0.030.tar.gz
Source5:        http://www.cpan.org/authors/id/E/ET/ETHER/Class-Method-Modifiers-2.08.tar.gz
Source6:        http://www.cpan.org/authors/id/H/HA/HAARG/Role-Tiny-1.003002.tar.gz
Source7:        http://www.cpan.org/authors/id/F/FR/FREW/Sub-Exporter-Progressive-0.001011.tar.gz
Source8:        http://www.cpan.org/authors/id/H/HA/HAARG/Devel-GlobalDestruction-0.11.tar.gz
Source9:        http://www.cpan.org/authors/id/E/ET/ETHER/strictures-1.004004.tar.gz
Source10:       http://www.cpan.org/authors/id/D/DO/DOY/Try-Tiny-0.18.tar.gz
Source11:       http://www.cpan.org/authors/id/R/RJ/RJBS/Test-Fatal-0.013.tar.gz
Source12:       http://www.cpan.org/authors/id/A/AD/ADAMK/List-MoreUtils-0.33.tar.gz
Source13:       http://www.cpan.org/authors/id/Z/ZE/ZEFRAM/Module-Runtime-0.013.tar.gz
Source14:       http://www.cpan.org/authors/id/D/DO/DOY/Dist-CheckConflicts-0.09.tar.gz
Source15:       http://www.cpan.org/authors/id/M/MS/MSTROUT/Moo-1.003001.tar.gz
Source16:       http://www.cpan.org/authors/id/M/MI/MIYAGAWA/Module-CPANfile-1.0002.tar.gz
Source17:       http://www.cpan.org/authors/id/D/DA/DAGOLDEN/File-pushd-1.005.tar.gz
Source18:       http://www.cpan.org/authors/id/M/MI/MIYAGAWA/App-cpanminus-1.7001.tar.gz
Source19:       http://www.cpan.org/authors/id/H/HA/HAARG/Module-Reader-0.002000.tar.gz
Source20:       http://www.cpan.org/authors/id/E/ET/ETHER/App-FatPacker-0.009018.tar.gz
Source21:       http://www.cpan.org/authors/id/L/LE/LEONT/Module-Build-0.4007.tar.gz
Source22:       http://www.cpan.org/authors/id/D/DA/DAGOLDEN/Path-Tiny-0.044.tar.gz
Source23:       http://www.cpan.org/authors/id/D/DR/DROLSKY/Devel-StackTrace-1.30.tar.gz
Source24:       http://www.cpan.org/authors/id/T/TM/TMTM/Class-Data-Inheritable-0.08.tar.gz
Source25:       http://www.cpan.org/authors/id/D/DR/DROLSKY/Exception-Class-1.37.tar.gz
Source26:       http://www.cpan.org/authors/id/M/MA/MAKAMAKA/JSON-2.90.tar.gz
Source27:       http://www.cpan.org/authors/id/M/MI/MIYAGAWA/Carton-v%{version}.tar.gz
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

cpanm -l local \
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
    %{SOURCE27}

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
