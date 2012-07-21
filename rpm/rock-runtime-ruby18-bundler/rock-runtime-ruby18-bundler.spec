%filter_from_provides /.*/d
%filter_from_requires /^ruby.*/d; /^libruby.*/d
%filter_setup

Name:           rock-runtime-ruby18-bundler
Version:        1.1.5
Release:        1%{?dist}
Summary:        A tool to manage Ruby 1.8.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://gembundler.com
Source0:        http://rubygems.org/downloads/bundler-%{version}.gem
Source1:        bundle
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-ruby18-core-rpmbuild
BuildRequires:  rock-runtime-ruby18-rubygems
Requires:       rock-runtime-ruby18-core
Requires:       rock-runtime-ruby18-rubygems

%description
Bundler manages an application's dependencies through its entire life across
many machines systematically and repeatably.

%prep

%build

%install
rm -rf %{buildroot}

export PATH="%{ruby18_rootdir}%{_bindir}:$PATH"
export GEM_HOME=%{ruby18_gemdir}

mkdir -p %{buildroot}%{_bindir}

gem install --force --ignore-dependencies --no-rdoc --no-ri --local --force \
  --install-dir %{buildroot}%{ruby18_gemdir} \
  --bindir %{buildroot}%{ruby18_rootdir}%{_bindir} \
  %{SOURCE0}

rm -fr %{buildroot}%{ruby18_gemdir}/cache

mv %{buildroot}%{ruby18_rootdir}%{_bindir}/bundle \
   %{buildroot}%{ruby18_rootdir}%{_bindir}/rock-bundle

%{__install} -p -m 0755 -D %{SOURCE1} \
  %{buildroot}%{ruby18_rootdir}%{_bindir}/bundle

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby18_gemdir}/gems/bundler-%{version}
%{ruby18_gemdir}/specifications/bundler-%{version}.gemspec
%{ruby18_rootdir}%{_bindir}/bundle
%{ruby18_rootdir}%{_bindir}/rock-bundle

%changelog
* Fri Jul 20 2012 Silas Sewell <silas@sewell.org> - 1.1.5-1
- Update to version 1.1.5
- Unset RUBYOPT hack

* Fri Jun 22 2012 Silas Sewell <silas@sewell.org> - 1.1.4-1
- Initial build
