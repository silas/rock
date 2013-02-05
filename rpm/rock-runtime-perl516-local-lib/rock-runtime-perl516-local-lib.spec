%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

Name:           rock-runtime-perl516-local-lib
Version:        1.008004
Release:        3%{?dist}
Summary:        A tool to manage Perl 5.16.x dependencies

Group:          Development/Languages
License:        GPL+ or Artistic
URL:            http://search.cpan.org/~apeiron/local-lib
Source0:        http://search.cpan.org/CPAN/authors/id/A/AP/APEIRON/local-lib-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-perl516-core-rpmbuild >= 5.12.2-2
Requires:       rock-runtime-perl516-core >= 5.12.2-2

%description
Create and use a local-lib for Perl modules with PERL5LIB.

%prep
%setup -q -n local-lib-%{version}

%build
export PATH="%{perl516_rootdir}%{_bindir}:$PATH"

perl Makefile.PL INSTALLDIRS=vendor

%install
rm -rf %{buildroot}

export PATH="%{perl516_rootdir}%{_bindir}:$PATH"

make install PERL_INSTALL_ROOT=%{buildroot}

rm -fr %{buildroot}%{perl516_rootdir}%{_prefix}/man

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes
%{perl516_vendorlib}
%{perl516_vendorarch}

%changelog
* Tue Nov 20 2012 RockStack <packages@rockstack.org> - 1.008004-3
- Fix paths for Perl 5.16.2

* Tue Sep 11 2012 RockStack <packages@rockstack.org> - 1.008004-2
- Rebuild for Perl 5.16.1

* Mon May 14 2012 RockStack <packages@rockstack.org> - 1.008004-1
- Initial build
