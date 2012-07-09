%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-php54
Version:        1
Release:        1%{?dist}
Summary:        php54 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       rock-runtime-php54-composer
Requires:       rock-runtime-php54-core

%description
php54 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%changelog
* Sun Jul 08 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
