%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

Name:           rock-runtime-perl518-local-lib
Version:        1.008023
Release:        1%{?dist}
Summary:        A tool to manage Perl 5.18.x dependencies

Group:          Development/Languages
License:        GPL+ or Artistic
URL:            http://search.cpan.org/~apeiron/local-lib
Source0:        http://www.cpan.org/authors/id/E/ET/ETHER/local-lib-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-perl518-core-rpmbuild >= 5.18.1-1
Requires:       rock-runtime-perl518-core >= 5.18.1-1

%description
Create and use a local-lib for Perl modules with PERL5LIB.

%prep
%setup -q -n local-lib-%{version}

%build
export PATH="%{perl518_rootdir}%{_bindir}:$PATH"

perl Makefile.PL INSTALLDIRS=vendor

%install
rm -rf %{buildroot}

export PATH="%{perl518_rootdir}%{_bindir}:$PATH"

make install PERL_INSTALL_ROOT=%{buildroot}

rm -fr %{buildroot}%{perl518_rootdir}%{_prefix}/man

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes
%{perl518_vendorlib}
%{perl518_vendorarch}

%changelog
* Thu Oct 31 2013 RockStack <packages@rockstack.org> - 1.008023-1
- Initial build
