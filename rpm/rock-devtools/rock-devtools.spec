Name:           rock-devtools
Version:        1
Release:        2%{?dist}
Summary:        Build and development tools

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       gcc
Requires:       gcc-c++
Requires:       git
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
* Tue Nov 20 2012 RockStack <packages@rockstack.org> - 1-2
- Add git

* Wed Jul 18 2012 RockStack <packages@rockstack.org> - 1-1
- Initial build
