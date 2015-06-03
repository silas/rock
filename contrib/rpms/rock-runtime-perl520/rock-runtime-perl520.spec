%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-perl520
Version:        1
Release:        2%{?dist}
Summary:        perl520 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-perl520-core-rpmbuild >= 5.20.1-1
Requires:       rock-runtime-perl520-core >= 5.20.1-1
Requires:       rock-runtime-perl520-cpanm >= 1.7102-1
Requires:       rock-runtime-perl520-local-lib >= 2.000012-1
Requires:       rock-runtime-perl520-carton >= 1.0.12-1

%description
perl520 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{perl520_rootdir}

cat << EOF > %{buildroot}%{perl520_rootdir}/rock.yml
env:
  PATH: "%{perl520_rootdir}/usr/bin:\${PATH}"
  PERL_ARCHNAME: "%{perl520_archname}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl520_rootdir}/rock.yml

%changelog
* Mon Sep 22 2014 RockStack <packages@rockstack.org> - 1-2
- Perl 5.20.1

* Mon Aug 11 2014 RockStack <packages@rockstack.org> - 1-1
- Initial build
