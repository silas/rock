%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-node08
Version:        1
Release:        8%{?dist}
Summary:        node08 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-node08-core-rpmbuild
Requires:       rock-runtime-node08-core >= 0.8.22-1

%description
node08 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{node08_rootdir}

cat << EOF > %{buildroot}%{node08_rootdir}/rock.yml
env:
  PATH: "%{node08_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{node08_rootdir}/rock.yml

%changelog
* Sun Mar 17 2013 RockStack <packages@rockstack.org> - 1-8
- Node 0.8.22

* Sun Feb 03 2013 RockStack <packages@rockstack.org> - 1-7
- Node 0.8.18

* Sat Nov 17 2012 RockStack <packages@rockstack.org> - 1-6
- Update to node 0.8.14

* Sat Sep 29 2012 RockStack <packages@rockstack.org> - 1-5
- Update to node 0.8.11

* Wed Sep 12 2012 RockStack <packages@rockstack.org> - 1-4
- Update to node 0.8.9

* Fri Jul 20 2012 RockStack <packages@rockstack.org> - 1-3
- Convert env to rock.yml

* Tue Jul 10 2012 RockStack <packages@rockstack.org> - 1-2
- Add env file
- Add explicit requires

* Sat Jun 30 2012 RockStack <packages@rockstack.org> - 1-1
- Initial build
