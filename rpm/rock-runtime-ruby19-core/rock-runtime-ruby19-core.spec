%filter_from_provides /.*/d
%filter_from_requires /^ruby.*/d; /^libruby.*/d
%filter_setup

%global runtime ruby19
%global ruby19_rootdir /opt/rock/runtime/%{runtime}
%global ruby19_abi 1.9.1
%global ruby19_gemdir %{ruby19_rootdir}%{_prefix}/lib/ruby/gems/%{ruby19_abi}

%global shortversion 1.9.3
%global patch 392

Name:           rock-runtime-ruby19-core
Version:        %{shortversion}.%{patch}
Release:        1%{?dist}
Summary:        A Ruby 1.9.x runtime

Group:          Development/Languages
License:        Ruby or BSD
URL:            http://ruby-lang.org
Source0:        http://ftp.ruby-lang.org/pub/ruby/1.9/ruby-%{shortversion}-p%{patch}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  patchelf

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
  --prefix=%{ruby19_rootdir}%{_prefix} \
  --enable-rpath \
  --enable-shared

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

patchelf --set-rpath %{ruby19_rootdir}%{_prefix}/lib %{buildroot}%{ruby19_rootdir}%{_bindir}/ruby*

# skip buildroot/rpath check
export QA_SKIP_BUILD_ROOT=1
export QA_SKIP_RPATHS=1

mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat >> %{buildroot}%{_sysconfdir}/rpm/macros.rock-ruby19 << \EOF
%%ruby19_rootdir %{ruby19_rootdir}
%%ruby19_abi %{ruby19_abi}
%%ruby19_gemdir %{ruby19_gemdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog GPL LEGAL NEWS README
%{ruby19_rootdir}%{_bindir}
%{ruby19_rootdir}%{_datarootdir}/ri/%{ruby19_abi}
%{ruby19_rootdir}%{_includedir}/ruby-%{ruby19_abi}
%{ruby19_rootdir}%{_mandir}
%{ruby19_rootdir}%{_prefix}/lib/libruby*
%{ruby19_rootdir}%{_prefix}/lib/ruby/%{ruby19_abi}
%{ruby19_gemdir}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-ruby19
%{ruby19_rootdir}%{_prefix}/lib/pkgconfig/ruby*

%changelog
* Mon Mar 18 2013 RockStack <packages@rockstack.org> - 1.9.3.392-1
- Update to 1.9.3 p392

* Sun Feb 03 2013 RockStack <packages@rockstack.org> - 1.9.3.374-1
- Update to 1.9.3 p374

* Sun Nov 18 2012 RockStack <packages@rockstack.org> - 1.9.3.327-1
- Update to 1.9.3 p327

* Fri Jul 20 2012 RockStack <packages@rockstack.org> - 1.9.3.194-2
- Add ruby19_abi to rpmbuild

* Mon May 14 2012 RockStack <packages@rockstack.org> - 1.9.3.194-1
- Initial build
