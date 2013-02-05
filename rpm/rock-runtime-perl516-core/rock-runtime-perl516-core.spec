%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

%global runtime perl516
%global perl516_rootdir /opt/rock/runtime/%{runtime}

%global privlib %{perl516_rootdir}%{_prefix}/share/perl5
%global archlib %{perl516_rootdir}%{_prefix}/lib/perl5

%global perl516_vendorlib  %{privlib}/vendor_perl
%global perl516_vendorarch %{archlib}/vendor_perl

%global perl516_arch_stem -thread-multi
%global perl516_archname %{_arch}-%{_os}%{perl516_arch_stem}

Name:           rock-runtime-perl516-core
Version:        5.16.2
Release:        2%{?dist}
Summary:        A Perl 5.16.x runtime

Group:          Development/Languages
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
URL:            http://www.perl.org
Source0:        http://www.cpan.org/src/5.0/perl-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  bzip2-devel
BuildRequires:  tcsh
BuildRequires:  zlib-devel

%description
Perl is a high-level programming language with roots in C, sed, awk and shell
scripting.

%package        rpmbuild
Summary:        RPM build files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    rpmbuild
Perl is a high-level programming language with roots in C, sed, awk and shell
scripting.

This packages contains resources for building %{name} RPMs.

%prep
%setup -q -n perl-%{version}

%build
./Configure -des \
  -Doptimize="$RPM_OPT_FLAGS" \
  -Dprefix=%{perl516_rootdir}%{_prefix} \
  -Dvendorprefix=%{perl516_rootdir}%{_prefix} \
  -Dsiteprefix=%{perl516_rootdir}%{_prefix}/local \
  -Dsitelib="%{perl516_rootdir}%{_prefix}/local/share/perl5" \
  -Dsitearch="%{perl516_rootdir}%{_prefix}/local/lib/perl5" \
  -Dprivlib="%{privlib}" \
  -Dvendorlib="%{perl516_vendorlib}" \
  -Darchlib="%{archlib}" \
  -Dvendorarch="%{perl516_vendorarch}" \
  -Darchname=%{perl516_archname} \
  -Dman3ext=3pm \
  -Dusethreads \
  -Duseithreads \
  -Duselargefiles \
  -Duseperlio

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/rpm

# FIXME: hack to get strip working
find %{buildroot}%{perl516_rootdir} -type f -exec chmod u+rw {} \;

# Remove .0 files
find %{buildroot} -name '*.0' -type f -delete

cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-perl516 << EOF
%%perl516_rootdir %{perl516_rootdir}
%%perl516_vendorlib  %{privlib}/vendor_perl
%%perl516_vendorarch %{archlib}/vendor_perl
%%perl516_arch_stem -thread-multi
%%perl516_archname %{_arch}-%{_os}%{perl516_arch_stem}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Artistic AUTHORS Copying README Changes
%{perl516_rootdir}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-perl516

%changelog
* Tue Nov 20 2012 RockStack <packages@rockstack.org> - 5.16.2-2
- Fix various path issues

* Sat Nov 17 2012 RockStack <packages@rockstack.org> - 5.16.2-1
- Update to 5.16.2

* Tue Sep 11 2012 RockStack <packages@rockstack.org> - 5.16.1-1
- Update to 5.16.1
- Add threads, largefiles and perlio flags

* Mon May 14 2012 RockStack <packages@rockstack.org> - 5.16.0-1
- Initial build
