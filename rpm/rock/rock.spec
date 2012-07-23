Name:           rock
Version:        0.1.0
Release:        1%{?dist}
Summary:        Application manage tool for Rock Platform

Group:          Development/Languages
License:        MIT
URL:            https://github.com/rockplatform/python-rock
Source0:        http://pypi.python.org/packages/source/r/rock/rock-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
Requires:       PyYAML
Requires:       python-argparse

%description
This is a command line tool that simplifies building, testing, and running
applications on the Rock Platform.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/%{name}
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-%{version}-py*.egg-info

%changelog
* Mon Jul 23 2012 Silas Sewell <silas@sewell.org> - 0.1.0-1
- Update to 0.1.0

* Wed Jul 18 2012 Silas Sewell <silas@sewell.org> - 0.0.3-1
- Update to 0.0.3

* Wed Jul 11 2012 Silas Sewell <silas@sewell.org> - 0.0.2-1
- Initial build
