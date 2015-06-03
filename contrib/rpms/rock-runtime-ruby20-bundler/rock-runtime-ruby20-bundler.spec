%filter_from_provides /.*/d
%filter_from_requires /^ruby.*/d; /^libruby.*/d
%filter_setup

Name:           rock-runtime-ruby20-bundler
Version:        1.3.4
Release:        1%{?dist}
Summary:        A tool to manage Ruby 2.0.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://gembundler.com
Source0:        http://rubygems.org/downloads/bundler-%{version}.gem
Source1:        bundle
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-ruby20-core-rpmbuild
Requires:       rock-runtime-ruby20-core

%description
Bundler manages an application's dependencies through its entire life across
many machines systematically and repeatably.

%prep

%build

%install
rm -rf %{buildroot}

export PATH="%{ruby20_rootdir}%{_bindir}:$PATH"

mkdir -p %{buildroot}%{_bindir}

gem install --force --ignore-dependencies --no-rdoc --no-ri --local --force \
  --install-dir %{buildroot}%{ruby20_gemdir} \
  --bindir %{buildroot}%{ruby20_rootdir}%{_bindir} \
  %{SOURCE0}

rm -fr %{buildroot}%{ruby20_gemdir}/cache

mv %{buildroot}%{ruby20_rootdir}%{_bindir}/bundle \
   %{buildroot}%{ruby20_rootdir}%{_bindir}/rock-bundle

%{__install} -p -m 0755 -D %{SOURCE1} \
  %{buildroot}%{ruby20_rootdir}%{_bindir}/bundle

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby20_gemdir}/gems/bundler-%{version}
%{ruby20_gemdir}/specifications/bundler-%{version}.gemspec
%{ruby20_rootdir}%{_bindir}/bundle
%{ruby20_rootdir}%{_bindir}/rock-bundle

%changelog
* Fri Mar 15 2013 RockStack <packages@rockstack.org> - 1.3.4-1
- Initial build
