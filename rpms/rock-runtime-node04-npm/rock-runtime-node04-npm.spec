%global __find_provides ''

Name:           rock-runtime-node04-npm
Version:        1.0.106
Release:        1%{?dist}
Summary:        A tool to manage Node 0.4.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://npmjs.org
Source0:        http://registry.npmjs.org/npm/-/npm-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-node04-core-rpmbuild
Requires:       rock-runtime-node04-core

%description
npm is a package manager for node. You can use it to install and publish your
node programs. It manages dependencies and does other cool stuff.

%prep
%setup -q -n package

%build
mkdir -p %{buildroot}%{node04_rootdir}%{_prefix}

./configure --prefix=%{buildroot}%{node04_rootdir}%{_prefix}

%install
rm -rf %{buildroot}

export PATH="%{node04_rootdir}%{_bindir}:$PATH"

make install

echo 'prefix = %{node04_rootdir}%{_prefix}' > %{buildroot}%{node04_rootdir}%{_prefix}/lib/node_modules/npm/npmrc

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.md
%{node04_rootdir}%{_bindir}/npm*
%{node04_rootdir}%{_prefix}/lib/node_modules/npm
%{node04_rootdir}%{_mandir}/man*/npm*

%changelog
* Fri Jun 22 2012 Silas Sewell <silas@sewell.org> - 1.0.106-1
- Initial build
