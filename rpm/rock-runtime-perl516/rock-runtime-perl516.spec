%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-perl516
Version:        1
Release:        6%{?dist}
Summary:        perl516 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-perl516-core-rpmbuild >= 5.12.2-2
Requires:       rock-runtime-perl516-core >= 5.16.2-2
Requires:       rock-runtime-perl516-cpanm >= 1.5017-1
Requires:       rock-runtime-perl516-local-lib >= 1.008004-3
Requires:       rock-runtime-perl516-carton >= 1:0.9.7-0.1

%description
perl516 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{perl516_rootdir}

cat << EOF > %{buildroot}%{perl516_rootdir}/rock.yml
env:
  PATH: "%{perl516_rootdir}/usr/bin:\${PATH}"
  PERL_ARCHNAME: "%{perl516_archname}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl516_rootdir}/rock.yml

%changelog
* Sun Nov 18 2012 Silas Sewell <silas@sewell.org> - 1-6
- Update paths
- Expose archname

* Sun Nov 18 2012 Silas Sewell <silas@sewell.org> - 1-5
- Update to Perl 5.16.2

* Wed Sep 12 2012 Silas Sewell <silas@sewell.org> - 1-4
- Update to Perl 5.16.1
- Rebuild and update dependency management tools

* Fri Jul 20 2012 Silas Sewell <silas@sewell.org> - 1-3
- Convert env to rock.yml

* Tue Jul 10 2012 Silas Sewell <silas@sewell.org> - 1-2
- Add env file
- Add explicit requires

* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
