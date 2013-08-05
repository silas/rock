%filter_from_provides /.*/d
%filter_setup

%global runtime node010
%global node010_rootdir /opt/rock/runtime/%{runtime}

Name:           rock-runtime-node010-core
Version:        0.10.15
Release:        1%{?dist}
Summary:        A Node.js 0.10.x runtime

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
./configure --prefix=%{node010_rootdir}%{_prefix}

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

rm -f %{buildroot}%{node010_rootdir}%{_prefix}/lib/dtrace/node.d

mkdir -p %{buildroot}%{_sysconfdir}/rpm

cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-node010 << EOF
%%node010_rootdir %{node010_rootdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README.md
%{node010_rootdir}%{_bindir}/node
%{node010_rootdir}%{_bindir}/npm
%{node010_rootdir}%{_mandir}/man1/node.1*
%{node010_rootdir}%{_prefix}/lib/node_modules

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-node010

%changelog
* Sat Aug 04 2013 RockStack <packages@rockstack.org> - 0.10.15-1
- Update to 0.10.15

* Sat Jul 13 2013 RockStack <packages@rockstack.org> - 0.10.13-1
- Update to 0.10.13

* Sun Jun 09 2013 RockStack <packages@rockstack.org> - 0.10.10-1
- Update to 0.10.10

* Sat Apr 27 2013 RockStack <packages@rockstack.org> - 0.10.5-1
- Update to 0.10.5

* Sun Apr 14 2013 RockStack <packages@rockstack.org> - 0.10.4-1
- Update to 0.10.4

* Tue Apr 09 2013 RockStack <packages@rockstack.org> - 0.10.3-1
- Update to 0.10.3

* Sat Mar 30 2013 RockStack <packages@rockstack.org> - 0.10.2-1
- Update to 0.10.2

* Mon Mar 25 2013 RockStack <packages@rockstack.org> - 0.10.1-1
- Update to 0.10.1

* Thu Mar 14 2013 RockStack <packages@rockstack.org> - 0.10.0-1
- Initial build
