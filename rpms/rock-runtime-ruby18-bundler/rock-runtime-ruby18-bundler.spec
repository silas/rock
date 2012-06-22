%global __find_provides ''
%global __ruby_provides ''
%global __ruby_requires ''

Name:           rock-runtime-ruby18-bundler
Version:        1.1.4
Release:        1%{?dist}
Summary:        A tool to manage Ruby 1.8.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://gembundler.com
Source0:        http://rubygems.org/downloads/bundler-%{version}.gem
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby18_gemdir}/gems/bundler-%{version}
%{ruby18_gemdir}/specifications/bundler-%{version}.gemspec
%{ruby18_rootdir}%{_bindir}/bundle

%changelog
* Fri Jun 22 2012 Silas Sewell <silas@sewell.org> - 1.1.4-1
- Initial build
