%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

%global runtime perl516
%global perl516_rootdir /opt/rock/runtime/%{runtime}

Name:           rock-runtime-perl516-core
Version:        5.16.0
Release:        1%{?dist}
Summary:        A Perl 5.16.x runtime

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
  -Dprefix=%{perl516_rootdir}%{_prefix} \
  -Dman3ext=3pm

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/rpm

# FIXME: hack to get strip working
find %{buildroot}%{perl516_rootdir} -type f -exec chmod u+rw {} \;

# Remove .0 files
find %{buildroot} -name '*.0' -type f -delete

cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-perl516 << EOF
%%perl516_rootdir %{perl516_rootdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Artistic AUTHORS Copying README Changes
%{perl516_rootdir}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-perl516

%changelog
* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 5.16.0-1
- Initial build
