%filter_from_provides /.*/d
%filter_setup

Name:           rock-platform
Version:        1
Release:        1%{?dist}
Summary:        Rock Platform

Group:          System Environment/Base
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       rock-platform-supervisor >= 3.0-0.3

%description
This package provides tools for running rock projects.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/rock/platform \
         %{buildroot}/opt/rock/platform/usr

ln -s %{_sysconfdir}/rock/platform %{buildroot}/opt/rock/platform/etc
ln -s %{_sysconfdir}/rock/platform %{buildroot}/opt/rock/platform/usr/etc

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sysconfdir}/rock/platform
/opt/rock/platform/etc
/opt/rock/platform/usr/etc

%changelog
* Sat Oct 06 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
