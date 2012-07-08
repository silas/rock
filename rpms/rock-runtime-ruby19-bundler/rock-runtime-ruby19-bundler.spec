%global __find_provides %{nil}
%global __ruby_provides %{nil}
%global __ruby_requires %{nil}
%global __provides_exclude .*
%global __requires_exclude ruby

Name:           rock-runtime-ruby19-bundler
Version:        1.1.4
Release:        1%{?dist}
Summary:        A tool to manage Ruby 1.9.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://gembundler.com
Source0:        http://rubygems.org/downloads/bundler-%{version}.gem
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby19_gemdir}/gems/bundler-%{version}
%{ruby19_gemdir}/specifications/bundler-%{version}.gemspec
%{ruby19_rootdir}%{_bindir}/bundle

%changelog
* Fri Jun 22 2012 Silas Sewell <silas@sewell.org> - 1.1.4-1
- Update to 1.1.4
- Use local install

* Mon May 14 2012 Silas Sewell <silas@sewell.org> - 1.1.3-1
- Initial build
