%filter_from_provides /.*/d
%filter_from_requires /^python.*/d; /^libpython.*/d
%filter_setup

Name:           rock-runtime-python34-virtualenv
Version:        1.11.6
Release:        1%{?dist}
Summary:        A tool to manage Python 3.4.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://www.virtualenv.org
Source0:        https://pypi.python.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-python34-core-rpmbuild
Requires:       rock-runtime-python34-core

%description
virtualenv is a tool to create isolated Python environments.

%prep
%setup -q -n virtualenv-%{version}
set -i -e "1s|#!/usr/bin/env python||" virtualenv.py

%build

export PATH="%{python34_rootdir}%{_bindir}:$PATH"

python setup.py build

%install
rm -rf %{buildroot}

export PATH="%{python34_rootdir}%{_bindir}:$PATH"

python setup.py install --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc PKG-INFO AUTHORS.txt LICENSE.txt
%{python34_rootdir}%{_bindir}/virtualenv*
%{python34_sitedir}/*

%changelog
* Mon Aug 11 2014 RockStack <packages@rockstack.org> - 1.11.6-1
- Initial build
