%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-python27
Version:        1
Release:        1%{?dist}
Summary:        python27 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       rock-runtime-python27-core
Requires:       rock-runtime-python27-virtualenv

%description
python27 runtime for rock.

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
