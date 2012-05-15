%global __find_provides ''
%global __perl_provides ''
%global __perl_requires ''

%global runtime perl514
%global perl514_rootdir /opt/rock/runtime/%{runtime}

Name:           rock-runtime-perl514-core
Version:        5.14.2
Release:        1%{?dist}
Summary:        A Perl 5.14.x runtime

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
./Configure -des -Doptimize="$RPM_OPT_FLAGS" \
  -Dprefix=%{perl514_rootdir}%{_prefix} \
  -Dbin="%{perl514_rootdir}%{_bindir}" \
  -Dprivlib="%{perl514_rootdir}%{_prefix}/lib/perl5" \
  -Dman1dir="%{perl514_rootdir}%{_mandir}/man1" \
  -Dman3dir="%{perl514_rootdir}%{_mandir}/man3" \
  -Dlddlflags="-shared $RPM_OPT_FLAGS $RPM_LD_FLAGS" \
  -Duseshrplib \
  -Dusethreads \
  -Duseithreads \
  -Dman3ext=3pm
%{__make}

%install
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/rpm

cat >> %{buildroot}%{_sysconfdir}/rpm/macros.rock-perl514 << \EOF
%%perl514_rootdir %{perl514_rootdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Artistic AUTHORS Copying README Changes
%{perl514_rootdir}%{_bindir}
%{perl514_rootdir}%{_mandir}
%{perl514_rootdir}%{_prefix}/lib/perl5

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-perl514

%changelog
* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 5.14.2-1
- Initial build
