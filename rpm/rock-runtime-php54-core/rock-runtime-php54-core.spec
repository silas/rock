%filter_from_provides /.*/d
%filter_from_requires /^php.*/d; /^libphp.*/d
%filter_setup

%global junk .{channels,depdb,depdblock,filemap,lock,registry}

%global libname %(basename %{_libdir})
%global mysql_config %{_libdir}/mysql/mysql_config
%global mysql_sock %(mysql_config --socket || echo /var/lib/mysql/mysql.sock)

%global runtime php54
%global php54_rootdir /opt/rock/runtime/%{runtime}

Name:           rock-runtime-php54-core
Version:        5.4.4
Release:        1%{?dist}
Summary:        A PHP 5.4.x runtime

Group:          Development/Languages
License:        PHP
URL:            http://www.php.net
Source0:        http://us.php.net/distributions/php-%{version}.tar.bz2
Patch0:         php-5.4.4-shebang.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  bison
BuildRequires:  bzip2
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel >= 7.9
BuildRequires:  db4-devel
BuildRequires:  gmp-devel
BuildRequires:  libedit-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libtool >= 1.4.3
BuildRequires:  libtool-ltdl-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel >= 6.6
BuildRequires:  perl
BuildRequires:  smtpdaemon
BuildRequires:  sqlite-devel >= 3.6.0
BuildRequires:  zlib-devel

# imap
BuildRequires:  libc-client-devel

# ldap
BuildRequires:  cyrus-sasl-devel
BuildRequires:  openldap-devel

# mysql
BuildRequires:  mysql-devel >= 4.1.0

# pgsql
BuildRequires:  postgresql-devel

# soap
BuildRequires:  libxml2-devel

# snmp
BuildRequires:  net-snmp-devel

# xml
BuildRequires:  libxml2-devel >= 2.4.14-1
BuildRequires:  libxslt-devel >= 1.0.18-1

# gd
BuildRequires:  freetype-devel
BuildRequires:  libXpm-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  t1lib-devel

# mcrypt
BuildRequires:  libmcrypt-devel

# tidy
BuildRequires:  libtidy-devel

# pspell
BuildRequires:  aspell-devel >= 0.50.0

# intl
BuildRequires:  libicu-devel >= 3.6

# enchant
BuildRequires:  enchant-devel >= 1.2.4

%description
PHP is an HTML-embedded scripting language.

PHP attempts to make it easy for developers to write dynamically generated web
pages. PHP also offers built-in database integration for several commercial and
non-commercial database management systems, so writing a database-enabled
webpage with PHP is fairly simple.

%package        rpmbuild
Summary:        RPM build files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    rpmbuild
PHP is an HTML-embedded scripting language.

This packages contains resources for building %{name} RPMs.

%prep
%setup -q -n php-%{version}
%patch0 -p1

%build
./configure \
  --prefix=%{php54_rootdir}%{_prefix} \
  --sbindir=%{php54_rootdir}%{_bindir} \
  --with-libdir=%{libname} \
  --disable-debug \
  --disable-static \
  --with-pic \
  --with-bz2 \
  --with-freetype-dir=%{_prefix} \
  --with-png-dir=%{_prefix} \
  --with-xpm-dir=%{_prefix} \
  --enable-gd-native-ttf \
  --with-t1lib=%{_prefix} \
  --with-gettext \
  --with-gmp \
  --with-iconv \
  --with-jpeg-dir=%{_prefix} \
  --with-openssl \
  --with-pcre-regex=%{_prefix} \
  --with-zlib \
  --enable-exif \
  --enable-ftp \
  --enable-sockets \
  --enable-ucd-snmp-hack \
  --enable-shmop \
  --enable-calendar \
  --with-libxml-dir=%{_prefix} \
  --enable-xml \
  --with-system-tzdata \
  --with-mhash \
  --enable-pcntl \
  --with-imap=shared --with-imap-ssl \
  --enable-mbstring=shared \
  --enable-mbregex \
  --with-gd=shared \
  --enable-bcmath=shared \
  --enable-dba=shared --with-db4=%{_prefix} \
  --with-xmlrpc=shared \
  --with-ldap=shared --with-ldap-sasl \
  --with-mysql=shared,mysqlnd \
  --with-mysqli=shared,mysqlnd \
  --with-mysql-sock=%{mysql_sock} \
  --with-pdo-mysql=shared,%{mysql_config} \
  --with-pdo-sqlite=shared,%{_prefix} \
  --enable-dom=shared \
  --with-pgsql=shared \
  --enable-wddx=shared \
  --with-snmp=shared,%{_prefix} \
  --enable-soap=shared \
  --with-xsl=shared,%{_prefix} \
  --enable-xmlreader=shared --enable-xmlwriter=shared \
  --with-curl=shared,%{_prefix} \
  --with-sqlite3=shared,%{_prefix} \
  --enable-json=shared \
  --with-libzip \
  --with-libedit \
  --with-pspell=shared \
  --enable-phar=shared \
  --with-mcrypt=shared,%{_prefix} \
  --with-kerberos \
  --with-tidy=shared,%{_prefix} \
  --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
  --enable-posix=shared \
  --enable-fileinfo=shared \
  --enable-intl=shared \
  --with-icu-dir=%{_prefix} \
  --with-enchant=shared,%{_prefix} \
  --enable-pdo=shared \
  --disable-cgi \
  --enable-fpm \
  --without-pear

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{__make} install INSTALL_ROOT=%{buildroot}

rm -fr %{php54_rootdir}/%{junk} \
       %{php54_rootdir}%{_prefix}/lib/php/%{junk}

mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat > %{buildroot}%{_sysconfdir}/rpm/macros.rock-php54 << EOF
%%php54_rootdir %{php54_rootdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE
%{php54_rootdir}

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-php54

%changelog
* Sun Jul 08 2012 Silas Sewell <silas@sewell.org> - 5.4.3-1
- Initial build
