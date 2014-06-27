%filter_from_provides /.*/d
%filter_from_requires /^ruby.*/d; /^libruby.*/d
%filter_setup

%global runtime ruby20
%global ruby20_rootdir /opt/rock/runtime/%{runtime}
%global ruby20_abi 2.0.0
%global ruby20_gemdir %{ruby20_rootdir}%{_prefix}/lib/ruby/gems/%{ruby20_abi}

%global shortversion 2.0.0
%global patch 353

Name:           rock-runtime-ruby20-core
Version:        %{shortversion}.%{patch}
Release:        1%{?dist}
Summary:        A Ruby 2.0.x runtime

Group:          Development/Languages
License:        Ruby or BSD
URL:            http://ruby-lang.org
Source0:        http://ftp.ruby-lang.org/pub/ruby/2.0/ruby-%{shortversion}-p%{patch}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  chrpath

BuildRequires:  autoconf
BuildRequires:  gdbm-devel
BuildRequires:  ncurses-devel
BuildRequires:  db4-devel
BuildRequires:  libffi-devel
BuildRequires:  openssl-devel
BuildRequires:  libyaml-devel
BuildRequires:  readline-devel

%description
Ruby is an interpreter of object-oriented scripting language.

%package        rpmbuild
Summary:        RPM build files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    rpmbuild
Ruby is an interpreter of object-oriented scripting language.

This packages contains resources for building %{name} RPMs.

%prep
%setup -q -n ruby-%{shortversion}-p%{patch}

%build
./configure \
  --prefix=%{ruby20_rootdir}%{_prefix} \
  --enable-rpath \
  --enable-shared

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

chrpath -r %{ruby20_rootdir}%{_prefix}/lib %{buildroot}%{ruby20_rootdir}%{_bindir}/ruby*

# skip buildroot/rpath check
export QA_SKIP_BUILD_ROOT=1
export QA_SKIP_RPATHS=1

mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat >> %{buildroot}%{_sysconfdir}/rpm/macros.rock-ruby20 << \EOF
%%ruby20_rootdir %{ruby20_rootdir}
%%ruby20_abi %{ruby20_abi}
%%ruby20_gemdir %{ruby20_gemdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog GPL LEGAL NEWS README
%{ruby20_rootdir}%{_bindir}
%{ruby20_rootdir}%{_datarootdir}/ri/%{ruby20_abi}
%{ruby20_rootdir}%{_includedir}/ruby-%{ruby20_abi}
%{ruby20_rootdir}%{_mandir}
%{ruby20_rootdir}%{_prefix}/lib/libruby*
%{ruby20_rootdir}%{_prefix}/lib/ruby/%{ruby20_abi}
%{ruby20_gemdir}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-ruby20
%{ruby20_rootdir}%{_prefix}/lib/pkgconfig/ruby*

%changelog
* Thu Jan 16 2014 RockStack <packages@rockstack.org> - 2.0.0.353-1
- Update to patch 353

* Thu Oct 03 2013 RockStack <packages@rockstack.org> - 2.0.0.247-1
- Update to patch 247

* Fri Mar 15 2013 RockStack <packages@rockstack.org> - 2.0.0.0-1
- Initial build
