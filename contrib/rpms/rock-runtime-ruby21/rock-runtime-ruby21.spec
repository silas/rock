%filter_from_provides /.*/d
%filter_setup

%global bundler_version 1.7.3

Name:           rock-runtime-ruby21
Version:        1
Release:        3%{?dist}
Summary:        ruby21 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-ruby21-core-rpmbuild
Requires:       rock-runtime-ruby21-bundler >= %{bundler_version}-1
Requires:       rock-runtime-ruby21-core >= 2.1.3-1

%description
ruby21 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{ruby21_rootdir}

cat << EOF > %{buildroot}%{ruby21_rootdir}/rock.yml
env:
  PATH: "%{ruby21_rootdir}/usr/bin:\${PATH}"
  RUBY_ABI: "%{ruby21_abi}"
  RUBYOPT: "-I%{ruby21_gemdir}/gems/bundler-%{bundler_version}/lib -rbundler/setup"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby21_rootdir}/rock.yml

%changelog
* Mon Sep 22 2014 RockStack <packages@rockstack.org> - 1-3
- Ruby 2.1.3
- Bundler 1.7.3

* Wed Aug 06 2014 RockStack <packages@rockstack.org> - 1-2
- Ruby 2.1.2
- Bundler 1.6.5

* Sat Feb 01 2014 RockStack <packages@rockstack.org> - 1-1
- Initial build
