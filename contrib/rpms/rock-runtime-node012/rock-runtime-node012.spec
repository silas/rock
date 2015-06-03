%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-node012
Version:        1
Release:        1%{?dist}
Summary:        node012 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-node012-core-rpmbuild
Requires:       rock-runtime-node012-core >= 0.12.0-1

%description
node012 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{node012_rootdir}

cat << EOF > %{buildroot}%{node012_rootdir}/rock.yml
env:
  PATH: "%{node012_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{node012_rootdir}/rock.yml

%changelog
* Mon Feb 16 2015 RockStack <packages@rockstack.org> - 1-1
- Initial build
