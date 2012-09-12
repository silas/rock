%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

Name:           rock-runtime-perl516-cpanm
Version:        1.5017
Release:        1%{?dist}
Summary:        A tool to manage Perl 5.16.x dependencies

Group:          Development/Languages
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
URL:            http://search.cpan.org/~miyagawa/App-cpanminus
Source0:        https://raw.github.com/miyagawa/cpanminus/%{version}/cpanm
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-perl516-core-rpmbuild
Requires:       rock-runtime-perl516-core

%description
cpanm - get, unpack build and install modules from CPAN

%prep

%build

%install
%{__install} -p -D -m 0755 %{SOURCE0} %{buildroot}%{perl516_rootdir}%{_bindir}/cpanm

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl516_rootdir}%{_bindir}/cpanm

%changelog
* Tue Sep 11 2012 Silas Sewell <silas@sewell.org> - 1.5017-1
- Update to 1.5017

* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 1.5014-1
- Initial build
