%filter_from_provides /.*/d
%filter_setup

%global bundler_version 1.3.4

Name:           rock-runtime-ruby19
Version:        1
Release:        6%{?dist}
Summary:        ruby19 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-ruby19-core-rpmbuild
Requires:       rock-runtime-ruby19-bundler >= %{bundler_version}-1
Requires:       rock-runtime-ruby19-core >= 1.9.3.392-1

%description
ruby19 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{ruby19_rootdir}

cat << EOF > %{buildroot}%{ruby19_rootdir}/rock.yml
env:
  PATH: "%{ruby19_rootdir}/usr/bin:\${PATH}"
  RUBY_ABI: "%{ruby19_abi}"
  RUBYOPT: "-I%{ruby19_gemdir}/gems/bundler-%{bundler_version}/lib -rbundler/setup"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby19_rootdir}/rock.yml

%changelog
* Mon Mar 18 2013 RockStack <packages@rockstack.org> - 1-6
- Ruby 1.9.3 p392
- Bundler 1.2.3

* Sun Feb 03 2013 RockStack <packages@rockstack.org> - 1-5
- Ruby 1.9.3 p374
- Bundler 1.2.3

* Sun Nov 18 2012 RockStack <packages@rockstack.org> - 1-4
- Update ruby 1.9.3 p327

* Fri Jul 20 2012 RockStack <packages@rockstack.org> - 1-3
- Convert env to rock.yml
- Update to bundler 1.1.5

* Tue Jul 10 2012 RockStack <packages@rockstack.org> - 1-2
- Add env file
- Add explicit requires

* Mon May 14 2012 RockStack <packages@rockstack.org> - 1-1
- Initial build
