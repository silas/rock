Name:           rock
Version:        0.7.0
Release:        1%{?dist}
Summary:        Build, test and run tool

Group:          Development/Languages
License:        MIT
URL:            https://github.com/rockplatform/rock
Source0:        http://pypi.python.org/packages/source/r/rock/rock-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  PyYAML
BUildRequires:  python-argparse
BuildRequires:  python-devel
BuildRequires:  python-nose
BuildRequires:  python-unittest2
Requires:       PyYAML
Requires:       python-argparse

%description
This is a build, test and run tool for the Rock Platform.

%prep
%setup -q

%build
%{__python} setup.py build

%check
nosetests

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/%{name}
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-%{version}-py*.egg-info

%changelog
* Sun Sep 23 2012 Silas Sewell <silas@sewell.org> - 0.7.0-1
- Add env support
- Fix non-string type coercion in env

* Wed Sep 12 2012 Silas Sewell <silas@sewell.org> - 0.6.1-1
- Update to 0.6.1
- Fix missing template directory

* Wed Sep 12 2012 Silas Sewell <silas@sewell.org> - 0.6.0-1
- Update to 0.6.0

* Sat Aug 19 2012 Silas Sewell <silas@sewell.org> - 0.5.0-1
- Update to 0.5.0

* Fri Aug 18 2012 Silas Sewell <silas@sewell.org> - 0.4.0-1
- Update to 0.4.0

* Mon Aug 06 2012 Silas Sewell <silas@sewell.org> - 0.3.1-1
- Update to 0.3.1

* Thu Aug 02 2012 Silas Sewell <silas@sewell.org> - 0.3.0-1
- Update to 0.3.0

* Mon Jul 30 2012 Silas Sewell <silas@sewell.org> - 0.2.0-1
- Update to 0.2.0

* Mon Jul 23 2012 Silas Sewell <silas@sewell.org> - 0.1.1-1
- Update to 0.1.1
- Use env instead of straight bash

* Mon Jul 23 2012 Silas Sewell <silas@sewell.org> - 0.1.0-1
- Update to 0.1.0

* Wed Jul 18 2012 Silas Sewell <silas@sewell.org> - 0.0.3-1
- Update to 0.0.3

* Wed Jul 11 2012 Silas Sewell <silas@sewell.org> - 0.0.2-1
- Initial build
