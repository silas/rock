%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-ruby18
Version:        1
Release:        1%{?dist}
Summary:        ruby18 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       rock-runtime-ruby18-bundler
Requires:       rock-runtime-ruby18-core
Requires:       rock-runtime-ruby18-rubygems

%description
ruby18 runtime for rock.

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
