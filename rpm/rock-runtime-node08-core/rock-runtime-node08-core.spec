%filter_from_provides /.*/d
%filter_setup

%global runtime node08
%global node08_rootdir /opt/rock/runtime/%{runtime}

Name:           rock-runtime-node08-core
Version:        0.8.18
Release:        1%{?dist}
Summary:        A Node.js 0.8.x runtime

Group:          Development/Languages
License:        MIT
URL:            http://nodejs.org
Source0:        http://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libevent-devel
BuildRequires:  openssl-devel
Requires:       man

%description
Node is an evented I/O framework for the V8 JavaScript engine.

%package        rpmbuild
Summary:        RPM build files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    rpmbuild
Node is an evented I/O framework for the V8 JavaScript engine.

This packages contains resources for building %{name} RPMs.

%prep
%setup -q -n node-v%{version}

%build
./configure --prefix=%{node08_rootdir}%{_prefix}

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

rm -f %{buildroot}%{node08_rootdir}%{_prefix}/lib/dtrace/node.d

mkdir -p %{buildroot}%{_sysconfdir}/rpm

cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-node08 << EOF
%%node08_rootdir %{node08_rootdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README.md
%{node08_rootdir}%{_bindir}/node
%{node08_rootdir}%{_bindir}/node-waf
%{node08_rootdir}%{_bindir}/npm
%{node08_rootdir}%{_includedir}/node
%{node08_rootdir}%{_mandir}/man1/node.1*
%{node08_rootdir}%{_prefix}/lib/node
%{node08_rootdir}%{_prefix}/lib/node_modules

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-node08

%changelog
* Sun Feb 03 2013 Silas Sewell <silas@sewell.org> - 0.8.18-1
- Update to 0.8.18

* Sat Nov 17 2012 Silas Sewell <silas@sewell.org> - 0.8.14-1
- Update to 0.8.14

* Sat Sep 29 2012 Silas Sewell <silas@sewell.org> - 0.8.11-1
- Update to 0.8.11

* Tue Sep 11 2012 Silas Sewell <silas@sewell.org> - 0.8.9-1
- Update to 0.8.9

* Fri Aug 10 2012 Silas Sewell <silas@sewell.org> - 0.8.6-1
- Update to 0.8.6

* Tue Jul 10 2012 Silas Sewell <silas@sewell.org> - 0.8.1-2
- Add man requirement
- Add rpm macro

* Sat Jun 30 2012 Silas Sewell <silas@sewell.org> - 0.8.1-1
- Initial build
