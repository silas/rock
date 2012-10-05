Name:           rock-release
Version:        1
Release:        1%{?dist}
Summary:        rock release files

Group:          System Environment/Base
License:        MIT
Source0:        rock.repo
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
yum config files for the Rock Platform.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d

cp %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d/rock.repo

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/rock.repo

%changelog
* Thu Oct 04 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial release
