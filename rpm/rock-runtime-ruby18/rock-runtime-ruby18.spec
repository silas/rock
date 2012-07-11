%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-ruby18
Version:        1
Release:        2%{?dist}
Summary:        ruby18 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       rock-runtime-ruby18-core-rpmbuild
Requires:       rock-runtime-ruby18-bundler >= 1.1.4-1
Requires:       rock-runtime-ruby18-core >= 1.8.7.370-1
Requires:       rock-runtime-ruby18-rubygems >= 1.8.24-1

%description
ruby18 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{ruby18_rootdir}

cat > %{buildroot}%{ruby18_rootdir}/env << EOF
export PATH="%{ruby18_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby18_rootdir}/env

%changelog
* Tue Jul 10 2012 Silas Sewell <silas@sewell.org> - 1-2
- Add env file
- Add explicit requires

* Fri Jun 22 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
