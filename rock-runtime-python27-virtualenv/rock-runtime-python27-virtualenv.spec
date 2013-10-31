%filter_from_provides /.*/d
%filter_from_requires /^python.*/d; /^libpython.*/d
%filter_setup

Name:           rock-runtime-python27-virtualenv
Version:        1.10
Release:        1%{?dist}
Summary:        A tool to manage Python 2.7.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://www.virtualenv.org
Source0:        https://pypi.python.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

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
%{python27_rootdir}/%{_bindir}/virtualenv*
%{python27_sitedir}/virtualenv*

%changelog
* Sun Aug 04 2013 RockStack <packages@rockstack.org> - 1.10-1
- Update 1.10

* Tue Apr 09 2013 RockStack <packages@rockstack.org> - 1.9.1-1
- Update 1.9.1

* Sun Feb 03 2013 RockStack <packages@rockstack.org> - 1.8.4-1
- Update 1.8.4

* Tue Sep 11 2012 RockStack <packages@rockstack.org> - 1.8.2-1
- Update 1.8.2

* Tue Jul 17 2012 RockStack <packages@rockstack.org> - 1.7.2-1
- Update 1.7.2

* Mon May 14 2012 RockStack <packages@rockstack.org> - 1.7.1.2-1
- Initial build
