%filter_from_provides /.*/d
%filter_from_requires /^php.*/d; /^libphp.*/d
%filter_setup

%global runtime php54
%global php43_rootdir /opt/rock/runtime/%{runtime}

Name:           rock-runtime-php54-core
Version:        5.4.4
Release:        1%{?dist}
Summary:        A PHP 5.4.x runtime

Group:          Development/Languages
License:        PHP
URL:            http://www.php.net
Source0:        http://us.php.net/distributions/php-%{version}.tar.bz2
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

%build
%configure

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{__make} install INSTALL_ROOT=%{buildroot}%{php54_rootdir}

mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat >> %{buildroot}%{_sysconfdir}/rpm/macros.rock-php54 << \EOF
%%php54_rootdir %{php54_rootdir}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.rock-php54

%changelog
* Sun Jul 08 2012 Silas Sewell <silas@sewell.org> - 5.4.3-1
- Initial build
