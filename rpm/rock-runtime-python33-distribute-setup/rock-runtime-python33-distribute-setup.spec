%filter_from_provides /.*/d
%filter_from_requires /^python.*/d; /^libpython.*/d
%filter_setup

Name:           rock-runtime-python33-distribute-setup
Version:        0.6.34
Release:        1%{?dist}
Summary:        A tool to manage Python 3.3.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://packages.python.org/distribute
Source0:        https://bitbucket.org/tarek/distribute/raw/%{version}/distribute_setup.py
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-python33-core-rpmbuild

%description
Easily download, build, install, upgrade, and uninstall Python packages.

%prep

%build

%install
rm -rf %{buildroot}

%{__install} -p -m 0755 -D %{SOURCE0} %{buildroot}%{python33_rootdir}%{_bindir}/distribute-setup

sed -i 's|#!python|#!/usr/bin/env python|g' %{buildroot}%{python33_rootdir}%{_bindir}/distribute-setup

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python33_rootdir}%{_bindir}/distribute-setup

%changelog
* Sun Feb 03 2013 Silas Sewell <silas@sewell.org> - 0.6.34-1
- Update to 0.6.34

* Sat Sep 30 2012 Silas Sewell <silas@sewell.org> - 0.6.28-1
- Initial build
