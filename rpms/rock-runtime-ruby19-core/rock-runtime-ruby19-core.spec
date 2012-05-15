%global __find_provides ''
%global __ruby_provides ''
%global __ruby_requires ''

%global runtime ruby19
%global ruby19_rootdir /opt/rock/runtime/%{runtime}
%global ruby19_gemdir %{ruby19_rootdir}%{_prefix}/lib/ruby/gems/1.9.1

%global shortversion 1.9.3
%global patch 194

Name:           rock-runtime-ruby19-core
Version:        %{shortversion}.%{patch}
Release:        1%{?dist}
Summary:        A Ruby 1.9.x runtime

Group:          Development/Languages
License:        Ruby or BSD
URL:            http://ruby-lang.org
Source0:        http://ftp.ruby-lang.org/pub/ruby/1.9/ruby-%{shortversion}-p%{patch}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
  --disable-rpath \
  --enable-shared
%{__make}

%install
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat >> %{buildroot}%{_sysconfdir}/rpm/macros.rock-ruby19 << \EOF
%%ruby19_rootdir %{ruby19_rootdir}
%%ruby19_gemdir %{ruby19_gemdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog GPL LEGAL NEWS README
%{ruby19_rootdir}%{_bindir}
%{ruby19_rootdir}%{_datarootdir}/ri/1.9.1
%{ruby19_rootdir}%{_includedir}/ruby-1.9.1
%{ruby19_rootdir}%{_mandir}
%{ruby19_rootdir}%{_prefix}/lib/libruby*
%{ruby19_rootdir}%{_prefix}/lib/ruby/1.9.1
%{ruby19_gemdir}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-ruby19
%{ruby19_rootdir}%{_prefix}/lib/pkgconfig/ruby*

%changelog
* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 1.9.3.194-1
- Initial build
