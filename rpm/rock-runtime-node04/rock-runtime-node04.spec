%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-node04
Version:        1
Release:        2%{?dist}
Summary:        node04 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-node04-core-rpmbuild
Requires:       rock-runtime-node04-core >= 0.4.12-2
Requires:       rock-runtime-node04-npm >= 1.0.106-1

%description
node04 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{node04_rootdir}

cat > %{buildroot}%{node04_rootdir}/env << EOF
export PATH="%{node04_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{node04_rootdir}/env

%changelog
* Tue Jul 10 2012 Silas Sewell <silas@sewell.org> - 1-2
- Add env file
- Add explicit requires

* Fri Jun 22 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
