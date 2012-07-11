%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-node08
Version:        1
Release:        2%{?dist}
Summary:        node08 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-node08-core-rpmbuild
Requires:       rock-runtime-node08-core >= 0.8.1-2

%description
node08 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{node08_rootdir}

cat > %{buildroot}%{node08_rootdir}/env << EOF
export PATH="%{node08_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{node08_rootdir}/env

%changelog
* Tue Jul 10 2012 Silas Sewell <silas@sewell.org> - 1-2
- Add env file
- Add explicit requires

* Sat Jun 30 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
