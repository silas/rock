%global __find_provides ''
%global __perl_provides ''
%global __perl_requires ''

Name:           rock-runtime-perl514-cpanm
Version:        1.5013
Release:        1%{?dist}
Summary:        A tool to manage Perl 5.14.x dependencies

Group:          Development/Languages
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
URL:            http://search.cpan.org/~miyagawa/App-cpanminus
Source0:        https://raw.github.com/miyagawa/cpanminus/%{version}/cpanm
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  rock-runtime-perl514-core-rpmbuild
Requires:       rock-runtime-perl514-core

%description
cpanm - get, unpack build and install modules from CPAN

%prep

%build

%install
%{__install} -p -D -m 0755 %{SOURCE0} %{buildroot}%{perl514_rootdir}%{_bindir}/cpanm

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl514_rootdir}%{_bindir}/cpanm

%changelog
* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 1.5013-1
- Initial build
