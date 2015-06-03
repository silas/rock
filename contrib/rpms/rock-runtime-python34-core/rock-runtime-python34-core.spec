%filter_from_provides /.*/d
%filter_from_requires /^python.*/d; /^libpython.*/d
%filter_setup

%global runtime python34
%global python34_rootdir /opt/rock/runtime/%{runtime}
%global python34_libdir %{python34_rootdir}%{_prefix}/lib/python3.4
%global python34_sitedir %{python34_libdir}/site-packages

Name:           rock-runtime-python34-core
Version:        3.4.1
Release:        1%{?dist}
Summary:        A Python 3.4.x runtime

Group:          Development/Languages
License:        Python
URL:            http://www.python.org
Source0:        http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  chrpath

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
mkdir -p %{buildroot}%{python34_libdir}

./configure \
  --prefix=%{python34_rootdir}%{_prefix} \
  --enable-ipv6 \
  --enable-shared \
  LDFLAGS="-Wl,-rpath %{buildroot}%{python34_rootdir}/usr/lib"

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

pushd %{buildroot}%{python34_rootdir}%{_bindir}
  ln -s idle3.4 idle
  ln -s pydoc3.4 pydoc
  ln -s python3.4 python
  ln -s python3.4-config python-config
popd

sed -i 's|^#! /usr/local/bin/python|#!/usr/bin/env python|g' \
  %{buildroot}%{python34_rootdir}%{_prefix}/lib/python3.4/cgi.py

sed -i "s|%{buildroot}||g" \
  %{buildroot}%{python34_rootdir}%{_prefix}/lib/python3.4/config-3.4m/Makefile \
  %{buildroot}%{python34_rootdir}%{_prefix}/lib/python3.4/_sysconfigdata.py

chrpath -r %{python34_rootdir}/usr/lib %{buildroot}%{python34_rootdir}%{_bindir}/python3.4

# skip buildroot/rpath check
export QA_SKIP_BUILD_ROOT=1
export QA_SKIP_RPATHS=1

mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-python34 << EOF
%%python34_rootdir %{python34_rootdir}
%%python34_libdir %{python34_libdir}
%%python34_sitedir %{python34_sitedir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{python34_rootdir}%{_bindir}
%{python34_rootdir}%{_includedir}/python3.4m
%{python34_rootdir}%{_mandir}/man1/python3*
%{python34_rootdir}%{_prefix}/lib/libpython*
%{python34_libdir}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-python34
%{python34_rootdir}%{_prefix}/lib/pkgconfig/python*.pc

%changelog
* Mon Aug 11 2014 RockStack <packages@rockstack.org> - 3.4.1-1
- Initial build
