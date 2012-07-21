%filter_from_provides /.*/d
%filter_from_requires /^ruby.*/d; /^libruby.*/d
%filter_setup

%global runtime ruby18
%global ruby18_rootdir /opt/rock/runtime/%{runtime}
%global ruby18_abi 1.8
%global ruby18_gemdir %{ruby18_rootdir}%{_prefix}/lib/ruby/gems/%{ruby18_abi}

%global shortversion 1.8.7
%global patch 370

Name:           rock-runtime-ruby18-core
Version:        %{shortversion}.%{patch}
Release:        2%{?dist}
Summary:        A Ruby 1.8.x runtime

Group:          Development/Languages
License:        Ruby or BSD
URL:            http://ruby-lang.org
Source0:        http://ftp.ruby-lang.org/pub/ruby/1.8/ruby-%{shortversion}-p%{patch}.tar.gz
Patch0:         ruby-%{shortversion}-p%{patch}-ext-dl.patch
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
%patch0 -p1

%build
./configure \
  --prefix=%{ruby18_rootdir}%{_prefix} \
  --enable-rpath \
  --enable-shared

%{__make}

%install
rm -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

patchelf --set-rpath %{ruby18_rootdir}%{_prefix}/lib %{buildroot}%{ruby18_rootdir}%{_bindir}/ruby*

# skip buildroot/rpath check
export QA_SKIP_BUILD_ROOT=1
export QA_SKIP_RPATHS=1

mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat >> %{buildroot}%{_sysconfdir}/rpm/macros.rock-ruby18 << \EOF
%%ruby18_rootdir %{ruby18_rootdir}
%%ruby18_abi %{ruby18_abi}
%%ruby18_gemdir %{ruby18_gemdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog GPL LEGAL NEWS README
%{ruby18_rootdir}%{_bindir}
%{ruby18_rootdir}%{_mandir}
%{ruby18_rootdir}%{_prefix}/lib/libruby*
%{ruby18_rootdir}%{_prefix}/lib/ruby/%{ruby18_abi}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-ruby18

%changelog
* Fri Jul 20 2012 Silas Sewell <silas@sewell.org> - 1.8.7.370-2
- Add ruby18_abi to rpmbuild

* Sat Jul 07 2012 Silas Sewell <silas@sewell.org> - 1.8.7.370-1
- Update to patch 370

* Fri Jun 22 2012 Silas Sewell <silas@sewell.org> - 1.8.7.358-1
- Initial build
