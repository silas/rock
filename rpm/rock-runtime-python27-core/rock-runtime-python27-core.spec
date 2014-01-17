%filter_from_provides /.*/d
%filter_from_requires /^python.*/d; /^libpython.*/d
%filter_setup

%global runtime python27
%global python27_rootdir /opt/rock/runtime/%{runtime}
%global python27_libdir %{python27_rootdir}%{_prefix}/lib/python2.7
%global python27_sitedir %{python27_libdir}/site-packages

Name:           rock-runtime-python27-core
Version:        2.7.6
Release:        1%{?dist}
Summary:        A Python 2.7.x runtime

Group:          Development/Languages
License:        Python
URL:            http://www.python.org
Source0:        http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  patchelf

BuildRequires:  autoconf
BuildRequires:  bzip2
BuildRequires:  bzip2-devel
BuildRequires:  findutils
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  gmp-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  readline-devel
BuildRequires:  sqlite-devel
BuildRequires:  tar
BuildRequires:  zlib-devel

%description
Python is an interpreted, interactive, object-oriented programming language.

%package        rpmbuild
Summary:        RPM build files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    rpmbuild
Python is an interpreted, interactive, object-oriented programming language.

This packages contains resources for building %{name} RPMs.

%prep
%setup -q -n Python-%{version}

%build
mkdir -p %{buildroot}%{python27_libdir}

./configure \
  --prefix=%{python27_rootdir}%{_prefix} \
  --enable-ipv6 \
  --enable-shared \
  LDFLAGS="-Wl,-rpath %{buildroot}%{python27_rootdir}/usr/lib"

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

sed -i 's|^#! /usr/local/bin/python|#!/usr/bin/env python|g' \
  %{buildroot}%{python27_rootdir}%{_prefix}/lib/python2.7/cgi.py

sed -i "s|%{buildroot}||g" %{buildroot}%{python27_rootdir}%{_prefix}/lib/python2.7/config/Makefile

patchelf --set-rpath %{python27_rootdir}/usr/lib %{buildroot}%{python27_rootdir}%{_bindir}/python2.7

# skip buildroot/rpath check
export QA_SKIP_BUILD_ROOT=1
export QA_SKIP_RPATHS=1

mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-python27 << EOF
%%python27_rootdir %{python27_rootdir}
%%python27_libdir %{python27_libdir}
%%python27_sitedir %{python27_sitedir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{python27_rootdir}%{_bindir}
%{python27_rootdir}%{_includedir}/python2.7
%{python27_rootdir}%{_mandir}/man1/python*
%{python27_rootdir}%{_prefix}/lib/libpython*
%{python27_libdir}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-python27
%{python27_rootdir}%{_prefix}/lib/pkgconfig/python*.pc

%changelog
* Thu Jan 16 2014 RockStack <packages@rockstack.org> - 2.7.6-1
- Update to 2.7.6

* Sun Aug 04 2013 RockStack <packages@rockstack.org> - 2.7.5-1
- Update to 2.7.5

* Tue Apr 09 2013 RockStack <packages@rockstack.org> - 2.7.4-1
- Update to 2.7.4

* Mon May 14 2012 RockStack <packages@rockstack.org> - 2.7.3-1
- Initial build
