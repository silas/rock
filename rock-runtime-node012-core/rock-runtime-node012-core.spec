%filter_from_provides /.*/d
%filter_setup

%global runtime node012
%global node012_rootdir /opt/rock/runtime/%{runtime}

Name:           rock-runtime-node012-core
Version:        0.12.0
Release:        1%{?dist}
Summary:        A Node.js 0.12.x runtime

Group:          Development/Languages
License:        MIT
URL:            http://nodejs.org
Source0:        http://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libevent-devel
BuildRequires:  openssl-devel
BuildRequires:  python
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
./configure --prefix=%{node012_rootdir}%{_prefix}

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

rm -f %{buildroot}%{node012_rootdir}%{_prefix}/lib/dtrace/node.d

mkdir -p %{buildroot}%{_sysconfdir}/rpm

cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-node012 << EOF
%%node012_rootdir %{node012_rootdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README.md
%{node012_rootdir}%{_bindir}/node
%{node012_rootdir}%{_bindir}/npm
%{node012_rootdir}%{_datadir}/systemtap/tapset/node.stp
%{node012_rootdir}%{_includedir}/node
%{node012_rootdir}%{_mandir}/man1/node.1*
%{node012_rootdir}%{_prefix}/lib/node_modules

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-node012

%changelog
* Mon Feb 16 2015 RockStack <packages@rockstack.org> - 0.12.0-1
- Initial build
