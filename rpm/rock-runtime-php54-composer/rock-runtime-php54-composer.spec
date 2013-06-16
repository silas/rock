%filter_from_provides /.*/d
%filter_from_requires /^php.*/d; /^libphp.*/d
%filter_setup

%global pre alpha7

Name:           rock-runtime-php54-composer
Version:        1.0.0
Release:        0.4.%{pre}%{?dist}
Summary:        A tool to manage PHP 5.4.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://getcomposer.org
Source0:        http://getcomposer.org/download/%{version}-%{pre}/composer.phar
Source1:        https://raw.github.com/composer/composer/%{version}-%{pre}/LICENSE
Source2:        https://raw.github.com/composer/composer/%{version}-%{pre}/CHANGELOG.md
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-php54-core-rpmbuild
Requires:       rock-runtime-php54-core
Requires:       unzip

%description
Composer is a package manager tracking local dependencies of your projects and
libraries.

%prep

%build

%install
rm -rf %{buildroot}

install -p -D -m 755 %{SOURCE0} %{buildroot}%{php54_rootdir}%{_bindir}/composer.phar
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_docdir}/%{name}-%{version}/CHANGELOG.md
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_docdir}/%{name}-%{version}/LICENSE

pushd %{buildroot}%{php54_rootdir}%{_bindir}
  ln -s composer.phar composer
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}/CHANGELOG.md
%doc %{_docdir}/%{name}-%{version}/LICENSE
%{php54_rootdir}%{_bindir}/composer.phar
%{php54_rootdir}%{_bindir}/composer

%changelog
* Sat Jun 15 2013 RockStack <packages@rockstack.org> - 1.0.0-0.4.alpha7
- Update to alpha7

* Sat Nov 17 2012 RockStack <packages@rockstack.org> - 1.0.0-0.3.alpha6
- Update to alpha6
- Reduces memory usage
- Link composer to composer.phar

* Thu Aug 23 2012 RockStack <packages@rockstack.org> - 1.0.0-0.2.alpha5
- Update to alpha5
- Unzip requirement

* Sun Jul 08 2012 RockStack <packages@rockstack.org> - 1.0.0-0.1.alpha4
- Initial build
