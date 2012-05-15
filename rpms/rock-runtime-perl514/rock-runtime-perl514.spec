Name:           rock-runtime-perl514
Version:        1
Release:        1%{?dist}
Summary:        perl514 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       rock-runtime-perl514-core
Requires:       rock-runtime-perl514-cpanm
Requires:       rock-runtime-perl514-local-lib

%description
perl514 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%changelog
* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
