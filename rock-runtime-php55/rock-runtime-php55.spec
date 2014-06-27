%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-php55
Version:        1
Release:        13%{?dist}
Summary:        php55 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-php55-core-rpmbuild
Requires:       rock-runtime-php55-composer >= 1.0.0-0.5
Requires:       rock-runtime-php55-core >= 5.5.8-1
Requires:       rock-runtime-php55-libmemcached >= 1.0.16-1
Requires:       rock-runtime-php55-memcached >= 2.1.0-8

%description
php55 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{php55_rootdir}

cat << EOF > %{buildroot}%{php55_rootdir}/rock.yml
env:
  PATH: "%{php55_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{php55_rootdir}/rock.yml

%changelog
* Thu Jan 16 2014 RockStack <packages@rockstack.org> - 1-13
- PHP 5.5.8
- Composer 1.0.0 alpha8

* Thu Nov 15 2013 RockStack <packages@rockstack.org> - 1-12
- Initial build
