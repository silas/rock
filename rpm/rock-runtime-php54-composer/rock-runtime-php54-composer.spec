%filter_from_provides /.*/d
%filter_from_requires /^php.*/d; /^libphp.*/d
%filter_setup

%global pre alpha4

Name:           rock-runtime-php54-composer
Version:        1.0.0
Release:        0.1.%{pre}%{?dist}
Summary:        A tool to manage PHP 5.4.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://getcomposer.org
# mkdir composer-%{version}-%{pre}
# git clone git://github.com/composer/composer.git
# cd composer
# git checkout %{version}-%{pre}
# wget http://getcomposer.org/composer.phar -O /tmp/composer.phar
# php /tmp/composer.phar install
# ./bin/compile
# cp composer.phar LICENSE ../composer-%{version}-%{pre}
# cd ..
# tar -cjf composer-%{version}-%{pre}.tar.bz2 composer-%{version}-%{pre}
Source0:        composer-%{version}-%{pre}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-php54-core-rpmbuild
Requires:       rock-runtime-php54-core

%description
Composer is a package manager tracking local dependencies of your projects and
libraries.

%prep
%setup -n composer-%{version}-%{pre}

%build

%install
rm -rf %{buildroot}

install -p -D -m 755 composer.phar %{buildroot}%{php54_rootdir}%{_bindir}/composer.phar

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE
%{php54_rootdir}%{_bindir}/composer.phar

%changelog
* Sun Jul 08 2012 Silas Sewell <silas@sewell.org> - 1.0.0-0.1.alpha4
- Initial build
