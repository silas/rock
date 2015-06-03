%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

Name:           rock-runtime-perl520-local-lib
Version:        2.000012
Release:        1%{?dist}
Summary:        A tool to manage Perl 5.20.x dependencies

Group:          Development/Languages
License:        GPL+ or Artistic
URL:            https://github.com/Perl-Toolchain-Gang/local-lib
Source0:        http://search.cpan.org/CPAN/authors/id/H/HA/HAARG/local-lib-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-perl520-core-rpmbuild >= 5.20.0-1
Requires:       rock-runtime-perl520-core >= 5.20.0-1

%description
Create and use a local-lib for Perl modules with PERL5LIB.

%prep
%setup -q -n local-lib-%{version}

%build
export PATH="%{perl520_rootdir}%{_bindir}:$PATH"

perl Makefile.PL INSTALLDIRS=vendor

%install
rm -rf %{buildroot}

export PATH="%{perl520_rootdir}%{_bindir}:$PATH"

make install PERL_INSTALL_ROOT=%{buildroot}

rm -fr %{buildroot}%{perl520_rootdir}%{_prefix}/man

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes
%{perl520_vendorlib}
%{perl520_vendorarch}

%changelog
* Mon Aug 11 2014 RockStack <packages@rockstack.org> - 2.000012-1
- Initial build
