%filter_from_provides /.*/d
%filter_setup

%global runtime node04
%global node04_rootdir /opt/rock/runtime/%{runtime}

Name:           rock-runtime-node04-core
Version:        0.4.12
Release:        2%{?dist}
Summary:        A Node.js 0.4.x runtime

Group:          Development/Languages
License:        MIT
URL:            http://nodejs.org
Source0:        http://nodejs.org/dist/node-v%{version}.tar.gz
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
./configure --prefix=%{node04_rootdir}%{_prefix}

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/rpm

cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-node04 << EOF
%%node04_rootdir %{node04_rootdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README.md
%{node04_rootdir}%{_bindir}/node
%{node04_rootdir}%{_bindir}/node-waf
%{node04_rootdir}%{_includedir}/node
%{node04_rootdir}%{_mandir}/man1/node.1*
%{node04_rootdir}%{_prefix}/lib/node

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-node04
%{node04_rootdir}%{_prefix}/lib/pkgconfig/nodejs.pc

%changelog
* Tue Jul 10 2012 Silas Sewell <silas@sewell.org> - 0.4.12-2
- Add man requirement

* Fri Jun 22 2012 Silas Sewell <silas@sewell.org> - 0.4.12-1
- Initial build
