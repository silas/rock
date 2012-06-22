%global __find_provides ''
%global __python_provides ''
%global __python_requires ''

Name:           rock-runtime-python27-virtualenv
Version:        1.7.1.2
Release:        1%{?dist}
Summary:        A tool to manage Python 2.7.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://www.virtualenv.org
Source0:        http://pypi.python.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  rock-runtime-python27-core-rpmbuild
Requires:       rock-runtime-python27-core

%description
virtualenv is a tool to create isolated Python environments.

%prep
%setup -q -n virtualenv-%{version}
set -i -e "1s|#!/usr/bin/env python||" virtualenv.py

%build

export PATH="%{python27_rootdir}%{_bindir}:$PATH"

python setup.py build

%install
rm -rf %{buildroot}

export PATH="%{python27_rootdir}%{_bindir}:$PATH"

python setup.py install --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc PKG-INFO AUTHORS.txt LICENSE.txt
%{python27_rootdir}/%{_bindir}/virtualenv
%{python27_sitedir}/virtualenv*

%changelog
* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 1.7.1.2-1
- Initial build
