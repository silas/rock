Name:           rock-runtime-node04
Version:        1
Release:        1%{?dist}
Summary:        node04 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       rock-runtime-node04-core
Requires:       rock-runtime-node04-npm

%description
node04 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%changelog
* Fri Jun 22 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
