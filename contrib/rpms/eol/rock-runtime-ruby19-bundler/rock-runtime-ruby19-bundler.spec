%filter_from_provides /.*/d
%filter_from_requires /^ruby.*/d; /^libruby.*/d
%filter_setup

Name:           rock-runtime-ruby19-bundler
Version:        1.3.4
Release:        1%{?dist}
Summary:        A tool to manage Ruby 1.9.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://gembundler.com
Source0:        http://rubygems.org/downloads/bundler-%{version}.gem
Source1:        bundle
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-ruby19-core-rpmbuild
Requires:       rock-runtime-ruby19-core

%description
Bundler manages an application's dependencies through its entire life across
many machines systematically and repeatably.

%prep

%build

%install
rm -rf %{buildroot}

export PATH="%{ruby19_rootdir}%{_bindir}:$PATH"

mkdir -p %{buildroot}%{_bindir}

gem install --force --ignore-dependencies --no-rdoc --no-ri --local --force \
  --install-dir %{buildroot}%{ruby19_gemdir} \
  --bindir %{buildroot}%{ruby19_rootdir}%{_bindir} \
  %{SOURCE0}

rm -fr %{buildroot}%{ruby19_gemdir}/cache

mv %{buildroot}%{ruby19_rootdir}%{_bindir}/bundle \
   %{buildroot}%{ruby19_rootdir}%{_bindir}/rock-bundle

%{__install} -p -m 0755 -D %{SOURCE1} \
  %{buildroot}%{ruby19_rootdir}%{_bindir}/bundle

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby19_gemdir}/gems/bundler-%{version}
%{ruby19_gemdir}/specifications/bundler-%{version}.gemspec
%{ruby19_rootdir}%{_bindir}/bundle
%{ruby19_rootdir}%{_bindir}/rock-bundle

%changelog
* Mon Mar 18 2013 RockStack <packages@rockstack.org> - 1.3.4-1
- Update to 1.3.4

* Sun Feb 03 2013 RockStack <packages@rockstack.org> - 1.2.3-1
- Update to 1.2.3

* Fri Jul 20 2012 RockStack <packages@rockstack.org> - 1.1.5-1
- Update to version 1.1.5
- Unset RUBYOPT hack

* Fri Jun 22 2012 RockStack <packages@rockstack.org> - 1.1.4-1
- Update to 1.1.4
- Use local install

* Mon May 14 2012 RockStack <packages@rockstack.org> - 1.1.3-1
- Initial build
