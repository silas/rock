%filter_from_provides /.*/d
%filter_from_requires /^libhashkit.*/d; /^libmemcached.*/d
%filter_setup

%global with_tests       %{?_with_tests:1}%{!?_with_tests:0}
%global with_sasl        0

Name:      rock-runtime-php55-libmemcached
Summary:   Client library and command line tools for memcached server
Version:   1.0.16
Release:   1%{?dist}
License:   BSD
Group:     System Environment/Libraries
URL:       http://libmemcached.org/
Source0:   http://launchpad.net/libmemcached/1.0/%{version}/+download/libmemcached-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{with_sasl}
BuildRequires: cyrus-sasl-devel
%endif
BuildRequires: rock-runtime-php55-core-rpmbuild
BuildRequires: flex
BuildRequires: bison
BuildRequires: python-sphinx
%if %{with_tests}
BuildRequires: memcached
%endif
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildRequires: systemtap-sdt-devel
%endif
BuildRequires: libevent-devel


%description
libmemcached is a C/C++ client library and tools for the memcached server
(http://memcached.org/). It has been designed to be light on memory
usage, and provide full access to server side methods.

It also implements several command line tools:

memcapable  Checking a Memcached server capibilities and compatibility
memcat      Copy the value of a key to standard output
memcp       Copy data to a server
memdump     Dumping your server
memerror    Translate an error code to a string
memexist    Check for the existance of a key
memflush    Flush the contents of your servers
memparse    Parse an option string
memping     Test to see if a server is available.
memrm       Remove a key(s) from the server
memslap     Generate testing loads on a memcached cluster
memstat     Dump the stats of your servers to standard output
memtouch    Touches a key


%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
%if %{with_sasl}
Requires: cyrus-sasl-devel%{?_isa}
%endif

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.


%prep
%setup -q -n libmemcached-%{version}

mkdir examples
cp -p tests/*.{cc,h} examples/

%if 0%{?fedora} > 9 || 0%{?rhel} > 5
%if 0%{?fedora} < 18 && 0%{?rhel} < 7
# Will be regenerated during build
# Only works with bison 2.4 - 2.5
rm -f libmemcached/csl/{parser,scanner}.cc
%endif
%endif

%if %{with_sasl}
# Temporary fix for SASL detection
sed -i -e s/ax_cv_sasl/ac_enable_sasl/ configure
%endif


%build
# option --with-memcached=false to disable server binary check (as we don't run test)
./configure \
  --disable-static \
  --prefix=%{php55_rootdir}%{_prefix} \
%if ! %{with_tests}
   --with-memcached=false
%endif

%if 0%{?fedora} < 14 && 0%{?rhel} < 7
# for warning: unknown option after '#pragma GCC diagnostic' kind
sed -e 's/-Werror//' -i Makefile
%endif

make %{_smp_mflags}


%install
rm -rf %{buildroot}
make install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""

%check
%if %{with_tests}
# test suite cannot run in mock (same port use for memcache servers on all arch)
# diff output.res output.cmp fails but result depend on server version
# ======================
# All 25 tests passed
# (3 tests were not run)
# ======================
# Tests completed
make test
%else
: 'Test suite disabled (missing "--with tests" option)'
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig
 

%files
%defattr (-,root,root,-) 
%doc AUTHORS COPYING README THANKS TODO ChangeLog
%{php55_rootdir}%{_bindir}/mem*
%exclude %{php55_libdir}/lib*.la
%{php55_libdir}/libhashkit.so.2*
%{php55_libdir}/libmemcached.so.11*
%{php55_libdir}/libmemcachedutil.so.2*


%files devel
%defattr (-,root,root,-) 
%doc examples
%{php55_rootdir}%{_includedir}/libmemcached
%{php55_rootdir}%{_includedir}/libmemcached-1.0
%{php55_rootdir}%{_includedir}/libhashkit
%{php55_rootdir}%{_includedir}/libhashkit-1.0
%{php55_rootdir}%{_includedir}/libmemcachedutil-1.0
%{php55_libdir}/libhashkit.so
%{php55_libdir}/libmemcached.so
%{php55_libdir}/libmemcachedutil.so
%{php55_libdir}/pkgconfig/libmemcached.pc
%{php55_rootdir}%{_datadir}/aclocal/ax_libmemcached.m4
%if !0%{?el6}
%{php55_rootdir}%{_mandir}
%endif


%changelog
* Thu Nov 14 2013 RockStack <packages@rockstack.org> - 1.0.16-1
- Initial buidl
