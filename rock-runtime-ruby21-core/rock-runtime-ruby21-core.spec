%filter_from_provides /.*/d
%filter_from_requires /^ruby.*/d; /^libruby.*/d
%filter_setup

%global runtime ruby21
%global ruby21_rootdir /opt/rock/runtime/%{runtime}
%global ruby21_abi 2.1.0
%global ruby21_gemdir %{ruby21_rootdir}%{_prefix}/lib/ruby/gems/%{ruby21_abi}

%global shortversion 2.1.2
%global patch 0

Name:           rock-runtime-ruby21-core
Version:        %{shortversion}
Release:        1%{?dist}
Summary:        A Ruby 2.1.x runtime

Group:          Development/Languages
License:        Ruby or BSD
URL:            http://ruby-lang.org
Source0:        http://ftp.ruby-lang.org/pub/ruby/2.1/ruby-%{shortversion}.tar.gz
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
%setup -q -n ruby-%{shortversion}

%build
./configure \
  --prefix=%{ruby21_rootdir}%{_prefix} \
  --enable-rpath \
  --enable-shared

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

chrpath -r %{ruby21_rootdir}%{_prefix}/lib %{buildroot}%{ruby21_rootdir}%{_bindir}/ruby*

# skip buildroot/rpath check
export QA_SKIP_BUILD_ROOT=1
export QA_SKIP_RPATHS=1

mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat >> %{buildroot}%{_sysconfdir}/rpm/macros.rock-ruby21 << \EOF
%%ruby21_rootdir %{ruby21_rootdir}
%%ruby21_abi %{ruby21_abi}
%%ruby21_gemdir %{ruby21_gemdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog GPL LEGAL NEWS README
%{ruby21_rootdir}%{_bindir}
%{ruby21_rootdir}%{_datarootdir}/ri/%{ruby21_abi}
%{ruby21_rootdir}%{_includedir}/ruby-%{ruby21_abi}
%{ruby21_rootdir}%{_mandir}
%{ruby21_rootdir}%{_prefix}/lib/libruby*
%{ruby21_rootdir}%{_prefix}/lib/ruby/%{ruby21_abi}
%{ruby21_gemdir}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-ruby21
%{ruby21_rootdir}%{_prefix}/lib/pkgconfig/ruby*

%changelog
* Wed Aug 06 2014 RockStack <packages@rockstack.org> - 2.1.2-1
- Update to 2.1.2

* Sat Feb 01 2014 RockStack <packages@rockstack.org> - 2.1.0-1
- Initial package
