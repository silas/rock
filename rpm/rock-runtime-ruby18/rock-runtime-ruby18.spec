%filter_from_provides /.*/d
%filter_setup

%global bundler_version 1.1.5

Name:           rock-runtime-ruby18
Version:        1
Release:        3%{?dist}
Summary:        ruby18 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-ruby18-core-rpmbuild >= 1.8.7.370-2
Requires:       rock-runtime-ruby18-bundler >= %{bundler_version}-1
Requires:       rock-runtime-ruby18-core >= 1.8.7.370-2
Requires:       rock-runtime-ruby18-rubygems >= 1.8.24-1

%description
ruby18 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{ruby18_rootdir}

cat << EOF > %{buildroot}%{ruby18_rootdir}/rock.yml
env:
  PATH: "%{ruby18_rootdir}/usr/bin:\${PATH}"
  RUBY_ABI: "%{ruby18_abi}"
  RUBYOPT: "-I%{ruby18_gemdir}/gems/bundler-%{bundler_version}/lib -rbundler/setup"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby18_rootdir}/rock.yml

%changelog
* Fri Jul 20 2012 Silas Sewell <silas@sewell.org> - 1-3
- Convert env to rock.yml
- Update to bundler 1.1.5

* Tue Jul 10 2012 Silas Sewell <silas@sewell.org> - 1-2
- Add env file
- Add explicit requires

* Fri Jun 22 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
