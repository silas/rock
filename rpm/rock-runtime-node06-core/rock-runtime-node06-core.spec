%filter_from_provides /.*/d
%filter_setup

%global runtime node06
%global node06_rootdir /opt/rock/runtime/%{runtime}

Name:           rock-runtime-node06-core
Version:        0.6.19
Release:        2%{?dist}
Summary:        A Node.js 0.6.x runtime

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
./configure --prefix=%{node06_rootdir}%{_prefix}

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/rpm

cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-node06 << EOF
%%node06_rootdir %{node06_rootdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README.md
%{node06_rootdir}%{_bindir}/node
%{node06_rootdir}%{_bindir}/node-waf
%{node06_rootdir}%{_bindir}/npm
%{node06_rootdir}%{_includedir}/node
%{node06_rootdir}%{_mandir}/man1/node.1*
%{node06_rootdir}%{_prefix}/lib/node
%{node06_rootdir}%{_prefix}/lib/node_modules

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-node06

%changelog
* Tue Jul 10 2012 Silas Sewell <silas@sewell.org> - 0.6.18-2
- Add man requirement
- Add rpm macro

* Fri Jun 22 2012 Silas Sewell <silas@sewell.org> - 0.6.19-1
- Update to 0.6.19

* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 0.6.17-1
- Initial build
