%filter_from_provides /.*/d
%filter_setup

%global bundler_version 1.3.4

Name:           rock-runtime-ruby20
Version:        1
Release:        1%{?dist}
Summary:        ruby20 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-ruby20-core-rpmbuild
Requires:       rock-runtime-ruby20-bundler >= %{bundler_version}-1
Requires:       rock-runtime-ruby20-core >= 2.0.0.0-1

%description
ruby20 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{ruby20_rootdir}

cat << EOF > %{buildroot}%{ruby20_rootdir}/rock.yml
env:
  PATH: "%{ruby20_rootdir}/usr/bin:\${PATH}"
  RUBY_ABI: "%{ruby20_abi}"
  RUBYOPT: "-I%{ruby20_gemdir}/gems/bundler-%{bundler_version}/lib -rbundler/setup"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby20_rootdir}/rock.yml

%changelog
* Fri Mar 15 2013 RockStack <packages@rockstack.org> - 1-1
- Initial build
