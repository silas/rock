%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-node010
Version:        1
Release:        12%{?dist}
Summary:        node010 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-node010-core-rpmbuild
Requires:       rock-runtime-node010-core >= 0.10.24-1

%description
node010 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{node010_rootdir}

cat << EOF > %{buildroot}%{node010_rootdir}/rock.yml
env:
  PATH: "%{node010_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{node010_rootdir}/rock.yml

%changelog
* Thu Jan 16 2014 RockStack <packages@rockstack.org> - 1-12
- Node 0.10.24

* Sat Oct 19 2013 RockStack <packages@rockstack.org> - 1-11
- Node 0.10.21

* Wed Sep 11 2013 RockStack <packages@rockstack.org> - 1-10
- Node 0.10.18

* Sun Aug 04 2013 RockStack <packages@rockstack.org> - 1-9
- Node 0.10.15

* Sat Jul 13 2013 RockStack <packages@rockstack.org> - 1-8
- Node 0.10.13

* Sun Jun 09 2013 RockStack <packages@rockstack.org> - 1-7
- Node 0.10.10

* Sat Apr 27 2013 RockStack <packages@rockstack.org> - 1-6
- Node 0.10.5

* Sun Apr 15 2013 RockStack <packages@rockstack.org> - 1-5
- Node 0.10.4

* Tue Apr 09 2013 RockStack <packages@rockstack.org> - 1-4
- Node 0.10.3

* Mon Apr 01 2013 RockStack <packages@rockstack.org> - 1-3
- Node 0.10.2

* Mon Mar 25 2013 RockStack <packages@rockstack.org> - 1-2
- Node 0.10.1

* Thu Mar 14 2013 RockStack <packages@rockstack.org> - 1-1
- Initial build
