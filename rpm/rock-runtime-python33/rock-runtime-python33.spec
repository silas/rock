%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-python33
Version:        1
Release:        5%{?dist}
Summary:        python33 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-python33-core-rpmbuild
Requires:       rock-runtime-python33-core >= 3.3.3-1
Requires:       rock-runtime-python33-distribute-setup >= 0.6.36-1

%description
python33 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{python33_rootdir}

cat << EOF > %{buildroot}%{python33_rootdir}/rock.yml
env:
  PATH: "%{python33_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python33_rootdir}/rock.yml

%changelog
* Thu Jan 16 2014 RockStack <packages@rockstack.org> - 1-5
- Python 3.3.3

* Sun Aug 04 2013 RockStack <packages@rockstack.org> - 1-4
- Python 3.3.2

* Tue Apr 09 2013 RockStack <packages@rockstack.org> - 1-3
- Python 3.3.1
- distribute-setup 0.6.36

* Sun Feb 03 2013 RockStack <packages@rockstack.org> - 1-2
- distribute-setup 0.6.34

* Sat Sep 29 2012 RockStack <packages@rockstack.org> - 1-1
- Initial build
