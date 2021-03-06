%filter_from_provides /.*/d
%filter_setup

%global runtime node010
%global node010_rootdir /opt/rock/runtime/%{runtime}

Name:           rock-runtime-node010-core
Version:        0.10.36
Release:        1%{?dist}
Summary:        A Node.js 0.10.x runtime

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
%{node010_rootdir}%{_includedir}/node

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-node010

%changelog
* Mon Feb 16 2015 RockStack <packages@rockstack.org> - 0.10.36-1
- Update to 0.10.36

* Thu Sep 18 2014 RockStack <packages@rockstack.org> - 0.10.32-1
- Update to 0.10.32

* Thu Sep 04 2014 RockStack <packages@rockstack.org> - 0.10.31-1
- Update to 0.10.31

* Fri Aug 08 2014 RockStack <packages@rockstack.org> - 0.10.30-1
- Update to 0.10.30

* Thu Jun 26 2014 RockStack <packages@rockstack.org> - 0.10.29-1
- Update to 0.10.29

* Fri Feb 28 2014 RockStack <packages@rockstack.org> - 0.10.26-1
- Update to 0.10.26

* Thu Jan 16 2014 RockStack <packages@rockstack.org> - 0.10.24-1
- Update to 0.10.24

* Sat Oct 19 2013 RockStack <packages@rockstack.org> - 0.10.21-1
- Update to 0.10.21

* Wed Sep 11 2013 RockStack <packages@rockstack.org> - 0.10.18-1
- Update to 0.10.18

* Sun Aug 04 2013 RockStack <packages@rockstack.org> - 0.10.15-1
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
