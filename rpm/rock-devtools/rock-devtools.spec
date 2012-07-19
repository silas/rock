Name:           rock-devtools
Version:        1
Release:        1%{?dist}
Summary:        Build and development tools

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       gcc
Requires:       gcc-c++
Requires:       make

%description
Rock devtools is a collection of tools for building and developing
applications.

%prep

%build

%install
rm -rf %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%changelog
* Wed Jul 18 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
