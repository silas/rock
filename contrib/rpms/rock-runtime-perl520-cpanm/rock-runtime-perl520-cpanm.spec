%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

Name:           rock-runtime-perl520-cpanm
Version:        1.7102
Release:        1%{?dist}
Summary:        A tool to manage Perl 5.20.x dependencies

Group:          Development/Languages
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
URL:            http://search.cpan.org/~miyagawa/App-cpanminus
Source0:        https://raw.github.com/miyagawa/cpanminus/%{version}/cpanm
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-perl520-core-rpmbuild
Requires:       rock-runtime-perl520-core

%description
cpanm - get, unpack build and install modules from CPAN

%prep

%build

%install
%{__install} -p -D -m 0755 %{SOURCE0} %{buildroot}%{perl520_rootdir}%{_bindir}/cpanm

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl520_rootdir}%{_bindir}/cpanm

%changelog
* Mon Aug 11 2014 RockStack <packages@rockstack.org> - 1.7102-1
- Initial build
