%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

Name:           rock-runtime-perl518-cpanm
Version:        1.7001
Release:        1%{?dist}
Summary:        A tool to manage Perl 5.16.x dependencies

Group:          Development/Languages
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
URL:            http://search.cpan.org/~miyagawa/App-cpanminus
Source0:        https://raw.github.com/miyagawa/cpanminus/%{version}/cpanm
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-perl518-core-rpmbuild
Requires:       rock-runtime-perl518-core

%description
cpanm - get, unpack build and install modules from CPAN

%prep

%build

%install
%{__install} -p -D -m 0755 %{SOURCE0} %{buildroot}%{perl518_rootdir}%{_bindir}/cpanm

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl518_rootdir}%{_bindir}/cpanm

%changelog
* Thu Oct 31 2013 RockStack <packages@rockstack.org> - 1.7001-1
- Initial build
