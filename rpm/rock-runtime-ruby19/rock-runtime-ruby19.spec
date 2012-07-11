%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-ruby19
Version:        1
Release:        2%{?dist}
Summary:        ruby19 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-ruby19-core-rpmbuild
Requires:       rock-runtime-ruby19-core >= 1.9.3.194-1
Requires:       rock-runtime-ruby19-bundler >= 1.1.4-1

%description
ruby19 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{ruby19_rootdir}

cat > %{buildroot}%{ruby19_rootdir}/env << EOF
export PATH="%{ruby19_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby19_rootdir}/env

%changelog
* Tue Jul 10 2012 Silas Sewell <silas@sewell.org> - 1-2
- Add env file
- Add explicit requires

* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
