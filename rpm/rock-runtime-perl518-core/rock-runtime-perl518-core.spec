%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

%global runtime perl518
%global perl518_rootdir /opt/rock/runtime/%{runtime}

%global privlib %{perl518_rootdir}%{_prefix}/share/perl5
%global archlib %{perl518_rootdir}%{_prefix}/lib/perl5

%global perl518_vendorlib  %{privlib}/vendor_perl
%global perl518_vendorarch %{archlib}/vendor_perl

%global perl518_arch_stem -thread-multi
%global perl518_archname %{_arch}-%{_os}%{perl518_arch_stem}

Name:           rock-runtime-perl518-core
Version:        5.18.1
Release:        1%{?dist}
Summary:        A Perl 5.18.x runtime

Group:          Development/Languages
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
URL:            http://www.perl.org
Source0:        http://www.cpan.org/src/5.0/perl-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  bzip2-devel
BuildRequires:  tcsh
BuildRequires:  zlib-devel

%description
Perl is a high-level programming language with roots in C, sed, awk and shell
scripting.

%package        rpmbuild
Summary:        RPM build files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    rpmbuild
Perl is a high-level programming language with roots in C, sed, awk and shell
scripting.

This packages contains resources for building %{name} RPMs.

%prep
%setup -q -n perl-%{version}

%build
./Configure -des \
  -Doptimize="$RPM_OPT_FLAGS" \
  -Dprefix=%{perl518_rootdir}%{_prefix} \
  -Dvendorprefix=%{perl518_rootdir}%{_prefix} \
  -Dsiteprefix=%{perl518_rootdir}%{_prefix}/local \
  -Dsitelib="%{perl518_rootdir}%{_prefix}/local/share/perl5" \
  -Dsitearch="%{perl518_rootdir}%{_prefix}/local/lib/perl5" \
  -Dprivlib="%{privlib}" \
  -Dvendorlib="%{perl518_vendorlib}" \
  -Darchlib="%{archlib}" \
  -Dvendorarch="%{perl518_vendorarch}" \
  -Darchname=%{perl518_archname} \
  -Dman3ext=3pm \
  -Dusethreads \
  -Duseithreads \
  -Duselargefiles \
  -Duseperlio

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/rpm

# FIXME: hack to get strip working
find %{buildroot}%{perl518_rootdir} -type f -exec chmod u+rw {} \;

# Remove .0 files
find %{buildroot} -name '*.0' -type f -delete

cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-perl518 << EOF
%%perl518_rootdir %{perl518_rootdir}
%%perl518_vendorlib  %{privlib}/vendor_perl
%%perl518_vendorarch %{archlib}/vendor_perl
%%perl518_arch_stem -thread-multi
%%perl518_archname %{_arch}-%{_os}%{perl518_arch_stem}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Artistic AUTHORS Copying README Changes
%{perl518_rootdir}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-perl518

%changelog
* Thu Oct 31 2013 RockStack <packages@rockstack.org> - 5.18.1-1
- Initial build
