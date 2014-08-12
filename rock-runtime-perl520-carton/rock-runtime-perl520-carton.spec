%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

%global cpan_url http://www.cpan.org/authors/id

Name:           rock-runtime-perl520-carton
Version:        1.0.12
Release:        1%{?dist}
Summary:        A tool to manage Perl 5.20.x dependencies

Group:          Development/Languages
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
URL:            http://search.cpan.org/dist/carton/
Source0:        %{cpan_url}/D/DA/DAGOLDEN/File-pushd-1.009.tar.gz
Source1:        %{cpan_url}/H/HA/HAARG/Module-Reader-0.002001.tar.gz
Source2:        %{cpan_url}/M/MS/MSTROUT/App-FatPacker-0.010001.tar.gz
Source3:        %{cpan_url}/M/MA/MAKAMAKA/JSON-2.90.tar.gz
Source4:        %{cpan_url}/D/DO/DOY/Try-Tiny-0.22.tar.gz
Source5:        %{cpan_url}/T/TM/TMTM/Class-Data-Inheritable-0.08.tar.gz
Source6:        %{cpan_url}/D/DR/DROLSKY/Devel-StackTrace-1.34.tar.gz
Source7:        %{cpan_url}/D/DR/DROLSKY/Exception-Class-1.38.tar.gz
Source8:        %{cpan_url}/D/DA/DAGOLDEN/Path-Tiny-0.056.tar.gz
Source9:        %{cpan_url}/M/MI/MIYAGAWA/Module-CPANfile-1.0002.tar.gz
Source10:       %{cpan_url}/T/TS/TSCH/ExtUtils-Depends-0.400.tar.gz
Source11:       %{cpan_url}/L/LE/LEONT/Module-Build-0.4206.tar.gz
Source12:       %{cpan_url}/Z/ZE/ZEFRAM/B-Hooks-OP-Check-0.19.tar.gz
Source13:       %{cpan_url}/Z/ZE/ZEFRAM/Lexical-SealRequireHints-0.007.tar.gz
Source14:       %{cpan_url}/V/VP/VPIT/indirect-0.31.tar.gz
Source15:       %{cpan_url}/I/IL/ILMARI/bareword-filehandles-0.003.tar.gz
Source16:       %{cpan_url}/I/IL/ILMARI/multidimensional-0.011.tar.gz
Source17:       %{cpan_url}/H/HA/HAARG/strictures-1.005004.tar.gz
Source18:       %{cpan_url}/Z/ZE/ZEFRAM/Module-Runtime-0.014.tar.gz
Source19:       %{cpan_url}/E/ET/ETHER/Import-Into-1.002004.tar.gz
Source20:       %{cpan_url}/E/ET/ETHER/Class-Method-Modifiers-2.10.tar.gz
Source21:       %{cpan_url}/H/HA/HAARG/Role-Tiny-1.003003.tar.gz
Source22:       %{cpan_url}/F/FR/FREW/Sub-Exporter-Progressive-0.001011.tar.gz
Source23:       %{cpan_url}/H/HA/HAARG/Devel-GlobalDestruction-0.12.tar.gz
Source24:       %{cpan_url}/H/HA/HAARG/Moo-1.005000.tar.gz
Source25:       %{cpan_url}/M/MI/MIYAGAWA/App-cpanminus-1.7004.tar.gz
Source26:       %{cpan_url}/M/MI/MIYAGAWA/Carton-v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  rock-runtime-perl520-core-rpmbuild >= 5.20.0-1
BuildRequires:  rock-runtime-perl520-cpanm
Requires:       rock-runtime-perl520-core >= 5.20.0-1

%description
carton is a command line tool to track the Perl module dependencies for your
Perl application. The managed dependencies are tracked in a carton.lock file,
which is meant to be version controlled, and the lock file allows other
developers of your application will have the exact same versions of the
modules.

%prep

%build
export PATH="%{perl520_rootdir}%{_bindir}:$PATH"

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
    %{SOURCE26}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{perl520_rootdir}%{_bindir} \
         %{buildroot}%{perl520_rootdir}%{_prefix}/lib

mv local %{buildroot}%{perl520_rootdir}%{_prefix}/lib/carton

cat << EOF > %{buildroot}%{perl520_rootdir}%{_bindir}/carton
#!/usr/bin/env bash

perl \
  -Mlocal::lib=%{perl520_rootdir}%{_prefix}/lib/carton \
  %{perl520_rootdir}%{_prefix}/lib/carton/bin/carton "\$@"
EOF

chmod 755 %{buildroot}%{perl520_rootdir}%{_bindir}/carton

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl520_rootdir}%{_bindir}/carton
%{perl520_rootdir}%{_prefix}/lib/carton

%changelog
* Mon Aug 11 2014 RockStack <packages@rockstack.org> - 1.0.12-1
- Initial build
