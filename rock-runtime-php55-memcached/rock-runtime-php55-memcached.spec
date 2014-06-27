%filter_from_provides /.*/d
%filter_from_requires /^libmemcached.*/d
%filter_setup

%global pecl_name memcached

Name:             rock-runtime-php55-memcached
Summary:          Extension to work with the Memcached caching daemon
Version:          2.1.0
Release:          8%{?dist}
License:          PHP and MIT
Group:            Development/Languages
URL:              http://pecl.php.net/package/%{pecl_name}
Source0:          http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
# https://github.com/php-memcached-dev/php-memcached/issues/25
# https://github.com/php-memcached-dev/php-memcached/commit/74542111f175fe2ec41c8bf722fc2cd3dac93eea.patch
Patch0:           %{pecl_name}-build.patch
# https://github.com/php-memcached-dev/php-memcached/pull/43
Patch1:           %{pecl_name}-info.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    autoconf
BuildRequires:    rock-runtime-php55-core-rpmbuild >= 5.4.11-1
BuildRequires:    rock-runtime-php55-libmemcached-devel >= 1.0.16-1
BuildRequires:    zlib-devel
Requires:         rock-runtime-php55-core >= 5.4.11-1
Requires:         rock-runtime-php55-libmemcached >= 1.0.16-1

%description
This extension uses libmemcached library to provide API for communicating
with memcached servers.

memcached is a high-performance, distributed memory object caching system,
generic in nature, but intended for use in speeding up dynamic web 
applications by alleviating database load.

It also provides a session handler (memcached). 

%prep 
%setup -c -q

# Chech version as upstream often forget to update this
extver=$(sed -n '/#define PHP_MEMCACHED_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_memcached.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream HTTP version is now ${extver}, expecting %{version}.
   : Update the pdover macro and rebuild.
   exit 1
fi

cp %{pecl_name}-%{version}/fastlz/LICENSE LICENSE-FastLZ

cat << EOF > %{pecl_name}.ini
extension=%{pecl_name}.so
EOF

cd %{pecl_name}-%{version}
%patch0 -p1 -b .build
%patch1 -p1 -b .info
cd ..

%build
cd %{pecl_name}-%{version}
%{php55_rootdir}%{_bindir}/phpize
./configure --enable-memcached-json \
           --prefix=%{php55_rootdir}%{_prefix} \
           --with-libmemcached-dir=%{php55_rootdir}%{_prefix} \
           --with-php-config=%{php55_rootdir}%{_bindir}/php-config
make %{?_smp_mflags}

%install
# Install the NTS extension
make install -C %{pecl_name}-%{version} INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
mkdir -p %{buildroot}%{php55_libdir}/php.d
echo 'extension = memcached.so' > %{buildroot}%{php55_libdir}/php.d/memcached.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{php55_pecl_xmldir}/%{name}.xml

%post
%{php55_pecl_install} %{php55_pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{php55_pecl_uninstall} %{pecl_name} >/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/{CREDITS,LICENSE,README.markdown,ChangeLog}
%doc LICENSE-FastLZ
%config(noreplace) %{php55_libdir}/php.d/%{pecl_name}.ini
%{php55_extdir}/%{pecl_name}.so
%{php55_pecl_xmldir}/%{name}.xml

%changelog
* Thu Nov 15 2013 RockStack <packages@rockstack.org> - 2.1.0-8
- Initial build
