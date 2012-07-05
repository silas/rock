%global __find_provides ''

%global runtime node08
%global node08_rootdir /opt/rock/runtime/%{runtime}

Name:           rock-runtime-node08-core
Version:        0.8.1
Release:        1%{?dist}
Summary:        A Node.js 0.8.x runtime

Group:          Development/Languages
License:        MIT
URL:            http://nodejs.org
Source0:        http://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libevent-devel
BuildRequires:  openssl-devel

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

%changelog
* Sat Jun 30 2012 Silas Sewell <silas@sewell.org> - 0.8.1-1
- Initial build
