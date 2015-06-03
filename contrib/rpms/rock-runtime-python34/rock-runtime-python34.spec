%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-python34
Version:        1
Release:        1%{?dist}
Summary:        python34 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-python34-core-rpmbuild
Requires:       rock-runtime-python34-core >= 3.4.1-1
Requires:       rock-runtime-python34-virtualenv >= 1.11.6-1

%description
python34 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{python34_rootdir}

cat << EOF > %{buildroot}%{python34_rootdir}/rock.yml
env:
  PATH: "%{python34_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python34_rootdir}/rock.yml

%changelog
* Mon Aug 11 2014 RockStack <packages@rockstack.org> - 1-1
- Initial build
