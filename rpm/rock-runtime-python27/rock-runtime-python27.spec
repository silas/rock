%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-python27
Version:        1
Release:        2%{?dist}
Summary:        python27 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-python27-core-rpmbuild
Requires:       rock-runtime-python27-core >= 2.7.3-1
Requires:       rock-runtime-python27-virtualenv >= 1.7.1.2-1

%description
python27 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{python27_rootdir}

cat > %{buildroot}%{python27_rootdir}/env << EOF
export PATH="%{python27_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python27_rootdir}/env

%changelog
* Tue Jul 10 2012 Silas Sewell <silas@sewell.org> - 1-2
- Add env file
- Add explicit requires

* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
