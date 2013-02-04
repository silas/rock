%filter_from_provides /.*/d
%filter_from_requires /^libmemcached.*/d
%filter_setup

%global pecl_name memcached

Name:             rock-runtime-php54-memcached
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
BuildRequires:    rock-runtime-php54-core-rpmbuild >= 5.4.11-1
BuildRequires:    rock-runtime-php54-libmemcached-devel >= 1.0.16-1
BuildRequires:    zlib-devel
Requires:         rock-runtime-php54-core >= 5.4.11-1
Requires:         rock-runtime-php54-libmemcached >= 1.0.16-1

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
%{php54_rootdir}%{_bindir}/phpize
./configure --enable-memcached-json \
           --prefix=%{php54_rootdir}%{_prefix} \
           --with-libmemcached-dir=%{php54_rootdir}%{_prefix} \
           --with-php-config=%{php54_rootdir}%{_bindir}/php-config
make %{?_smp_mflags}

%install
# Install the NTS extension
make install -C %{pecl_name}-%{version} INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
mkdir -p %{buildroot}%{php54_libdir}/php.d
echo 'extension = memcached.so' > %{buildroot}%{php54_libdir}/php.d/memcached.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{php54_pecl_xmldir}/%{name}.xml

%post
%{php54_pecl_install} %{php54_pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{php54_pecl_uninstall} %{pecl_name} >/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/{CREDITS,LICENSE,README.markdown,ChangeLog}
%doc LICENSE-FastLZ
%config(noreplace) %{php54_libdir}/php.d/%{pecl_name}.ini
%{php54_extdir}/%{pecl_name}.so
%{php54_pecl_xmldir}/%{name}.xml

%changelog
* Sun Feb 03 2013 Silas Sewell <silas@sewell.org> - 2.1.0-8
- Bump for libmemcached 1.0.16

* Thu Nov 22 2012 Silas Sewell <silas@sewell.org> - 2.1.0-7
- Use new php.d directory
- Remove zts references

* Wed Nov 21 2012 Silas Sewell <silas@sewell.org> - 2.1.0-6
- Use new pecl macros

* Wed Nov 21 2012 Silas Sewell <silas@sewell.org> - 2.1.0-5
- Filter provides

* Sat Nov 17 2012 Silas Sewell <silas@sewell.org> - 2.1.0-4
- Namespace for rock runtime php54

* Fri Oct 19 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-3
- improve comment in configuration about session.

* Sat Sep 22 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- rebuild for new libmemcached
- drop sasl support

* Tue Aug 07 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0
- add patch to lower libmemcached required version

* Tue Jul 31 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-4
- bump release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-3
- enable ZTS extension

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.1736623
- update to git snapshot (post 2.0.0b2) for php 5.4 build

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 17 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-7
- rebuild against libmemcached 0.52
- adapted filter
- clean spec

* Thu Jun 02 2011  Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-6
- rebuild against libmemcached 0.49

* Thu Mar 17 2011  Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-5
- rebuilt with igbinary support
- add arch specific provides/requires

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 23 2010  Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-3
- add filter_provides to avoid private-shared-object-provides memcached.so

* Fri Oct 01 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-2
- rebuild against libmemcached 0.44 with SASL support

* Tue May 04 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-1
- update to 1.0.2 for libmemcached 0.40

* Sat Mar 13 2010 Remi Collet <fedora@famillecollet.com> - 1.0.1-1
- update to 1.0.1 for libmemcached 0.38

* Sun Feb 07 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3.1
- bump release

* Sat Feb 06 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3
- rebuilt against new libmemcached
- add minimal %%check

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <fedora@famillecollet.com> - 1.0.0-1
- Update to 1.0.0 (First stable release)

* Sat Jun 27 2009 Remi Collet <fedora@famillecollet.com> - 0.2.0-1
- Update to 0.2.0 + Patch for HAVE_JSON constant

* Sun Apr 29 2009 Remi Collet <fedora@famillecollet.com> - 0.1.5-1
- Initial RPM

