%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-perl518
Version:        1
Release:        1%{?dist}
Summary:        perl518 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-perl518-core-rpmbuild >= 5.18.1-1
Requires:       rock-runtime-perl518-core >= 5.18.1-1
Requires:       rock-runtime-perl518-cpanm >= 1.7001-1
Requires:       rock-runtime-perl518-local-lib >= 1.008023-1
Requires:       rock-runtime-perl518-carton >= 1.0.12-1

%description
perl518 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{perl518_rootdir}

cat << EOF > %{buildroot}%{perl518_rootdir}/rock.yml
env:
  PATH: "%{perl518_rootdir}/usr/bin:\${PATH}"
  PERL_ARCHNAME: "%{perl518_archname}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl518_rootdir}/rock.yml

%changelog
* Thu Oct 31 2013 RockStack <packages@rockstack.org> - 1-1
- Initial build
