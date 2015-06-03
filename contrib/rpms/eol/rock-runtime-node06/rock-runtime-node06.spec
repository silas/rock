%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-node06
Version:        1
Release:        3%{?dist}
Summary:        node06 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-node06-core-rpmbuild
Requires:       rock-runtime-node06-core >= 0.6.18-2

%description
node06 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{node06_rootdir}

cat << EOF > %{buildroot}%{node06_rootdir}/rock.yml
env:
  PATH: "%{node06_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{node06_rootdir}/rock.yml

%changelog
* Fri Jul 20 2012 RockStack <packages@rockstack.org> - 1-3
- Convert env to rock.yml

* Tue Jul 10 2012 RockStack <packages@rockstack.org> - 1-2
- Add env file
- Add explicit requires

* Mon May 14 2012 RockStack <packages@rockstack.org> - 1-1
- Initial build
