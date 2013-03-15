%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-node010
Version:        1
Release:        1%{?dist}
Summary:        node010 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-node010-core-rpmbuild
Requires:       rock-runtime-node010-core >= 0.10.0-1

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
* Thu Mar 14 2013 RockStack <packages@rockstack.org> - 1-1
- Initial build
