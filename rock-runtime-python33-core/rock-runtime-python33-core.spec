%filter_from_provides /.*/d
%filter_from_requires /^python.*/d; /^libpython.*/d
%filter_setup

%global runtime python33
%global python33_rootdir /opt/rock/runtime/%{runtime}
%global python33_libdir %{python33_rootdir}%{_prefix}/lib/python3.3
%global python33_sitedir %{python33_libdir}/site-packages

Name:           rock-runtime-python33-core
Version:        3.3.2
Release:        1%{?dist}
Summary:        A Python 3.3.x runtime

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
mkdir -p %{buildroot}%{python33_libdir}

./configure \
  --prefix=%{python33_rootdir}%{_prefix} \
  --enable-ipv6 \
  --enable-shared \
  LDFLAGS="-Wl,-rpath %{buildroot}%{python33_rootdir}/usr/lib"

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

pushd %{buildroot}%{python33_rootdir}%{_bindir}
  ln -s idle3.3 idle
  ln -s pydoc3.3 pydoc
  ln -s python3.3 python
  ln -s python3.3-config python-config
popd

sed -i 's|^#! /usr/local/bin/python|#!/usr/bin/env python|g' \
  %{buildroot}%{python33_rootdir}%{_prefix}/lib/python3.3/cgi.py

sed -i "s|%{buildroot}||g" %{buildroot}%{python33_rootdir}%{_prefix}/lib/python3.3/config-3.3m/Makefile

patchelf --set-rpath %{python33_rootdir}/usr/lib %{buildroot}%{python33_rootdir}%{_bindir}/python3.3

# skip buildroot/rpath check
export QA_SKIP_BUILD_ROOT=1
export QA_SKIP_RPATHS=1

mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-python33 << EOF
%%python33_rootdir %{python33_rootdir}
%%python33_libdir %{python33_libdir}
%%python33_sitedir %{python33_sitedir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{python33_rootdir}%{_bindir}
%{python33_rootdir}%{_includedir}/python3.3m
%{python33_rootdir}%{_mandir}/man1/python3*
%{python33_rootdir}%{_prefix}/lib/libpython*
%{python33_libdir}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-python33
%{python33_rootdir}%{_prefix}/lib/pkgconfig/python*.pc

%changelog
* Sun Aug 04 2013 RockStack <packages@rockstack.org> - 3.3.2-1
- Update to 3.3.2

* Tue Apr 09 2013 RockStack <packages@rockstack.org> - 3.3.1-1
- Update to 3.3.1

* Sun Feb 03 2013 RockStack <packages@rockstack.org> - 3.3.0-2
- Fix Makefile paths

* Sat Sep 29 2012 RockStack <packages@rockstack.org> - 3.3.0-1
- Initial build
