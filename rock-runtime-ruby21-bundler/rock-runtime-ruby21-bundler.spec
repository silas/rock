%filter_from_provides /.*/d
%filter_from_requires /^ruby.*/d; /^libruby.*/d
%filter_setup

Name:           rock-runtime-ruby21-bundler
Version:        1.7.3
Release:        1%{?dist}
Summary:        A tool to manage Ruby 2.1.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://gembundler.com
Source0:        http://rubygems.org/downloads/bundler-%{version}.gem
Source1:        bundle
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-ruby21-core-rpmbuild
Requires:       rock-runtime-ruby21-core

%description
Bundler manages an application's dependencies through its entire life across
many machines systematically and repeatably.

%prep

%build

%install
rm -rf %{buildroot}

export PATH="%{ruby21_rootdir}%{_bindir}:$PATH"

mkdir -p %{buildroot}%{_bindir}

gem install --force --ignore-dependencies --no-rdoc --no-ri --local --force \
  --install-dir %{buildroot}%{ruby21_gemdir} \
  --bindir %{buildroot}%{ruby21_rootdir}%{_bindir} \
  %{SOURCE0}

rm -fr %{buildroot}%{ruby21_gemdir}/cache

mv %{buildroot}%{ruby21_rootdir}%{_bindir}/bundle \
   %{buildroot}%{ruby21_rootdir}%{_bindir}/rock-bundle

%{__install} -p -m 0755 -D %{SOURCE1} \
  %{buildroot}%{ruby21_rootdir}%{_bindir}/bundle

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby21_gemdir}/gems/bundler-%{version}
%{ruby21_gemdir}/specifications/bundler-%{version}.gemspec
%{ruby21_rootdir}%{_bindir}/bundle
%{ruby21_rootdir}%{_bindir}/bundler
%{ruby21_rootdir}%{_bindir}/rock-bundle

%changelog
* Mon Sep 22 2014 RockStack <packages@rockstack.org> - 1.7.3-1
- Update to 1.7.3

* Wed Aug 06 2014 RockStack <packages@rockstack.org> - 1.6.5-1
- Update to 1.6.5

* Sat Feb 01 2014 RockStack <packages@rockstack.org> - 1.5.2-1
- Initial build
