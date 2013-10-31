%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-php54
Version:        1
Release:        12%{?dist}
Summary:        php54 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-php54-core-rpmbuild
Requires:       rock-runtime-php54-composer >= 1.0.0-0.4
Requires:       rock-runtime-php54-core >= 5.4.16-1
Requires:       rock-runtime-php54-libmemcached >= 1.0.16-1
Requires:       rock-runtime-php54-memcached >= 2.1.0-8

%description
php54 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{php54_rootdir}

cat << EOF > %{buildroot}%{php54_rootdir}/rock.yml
env:
  PATH: "%{php54_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{php54_rootdir}/rock.yml

%changelog
* Sat Jun 15 2013 RockStack <packages@rockstack.org> - 1-12
- PHP 5.4.16
- Composer 1.0.0 alpha7

* Sun Feb 03 2013 RockStack <packages@rockstack.org> - 1-11
- PHP 5.4.11

* Thu Nov 22 2012 RockStack <packages@rockstack.org> - 1-10
- Use php.d

* Wed Nov 21 2012 RockStack <packages@rockstack.org> - 1-9
- Fix pear/pecl macros

* Wed Nov 21 2012 RockStack <packages@rockstack.org> - 1-8
- Fix provides and requires for memcache

* Sun Nov 18 2012 RockStack <packages@rockstack.org> - 1-7
- PHP 5.4.8
- Add PHP memcached

* Sat Sep 29 2012 RockStack <packages@rockstack.org> - 1-6
- PHP 5.4.7

* Thu Aug 23 2012 RockStack <packages@rockstack.org> - 1-5
- Composer 1.0.0 alpha5
- PHP 5.4.6

* Fri Jul 20 2012 RockStack <packages@rockstack.org> - 1-4
- Convert env to rock.yml

* Tue Jul 17 2012 RockStack <packages@rockstack.org> - 1-3
- Fix various issues with core package

* Tue Jul 10 2012 RockStack <packages@rockstack.org> - 1-2
- Add env file
- Add explicit requires

* Sun Jul 08 2012 RockStack <packages@rockstack.org> - 1-1
- Initial build
