%filter_from_provides /.*/d
%filter_from_requires /^ruby.*/d; /^libruby.*/d
%filter_setup

Name:           rock-runtime-ruby18-rubygems
Version:        1.8.25
Release:        1%{?dist}
Summary:        A tool to manage Ruby 1.8.x dependencies

Group:          Development/Languages
License:        MIT
URL:            http://rubygems.org
Source0:        http://production.cf.rubygems.org/rubygems/rubygems-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-ruby18-core-rpmbuild
Requires:       rock-runtime-ruby18-core

%description
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%prep
%setup -q -n rubygems-%{version}

%build

%install
rm -rf %{buildroot}

export PATH="%{ruby18_rootdir}%{_bindir}:$PATH"

mkdir -p %{buildroot}%{ruby18_rootdir}%{_bindir}
mkdir -p %{buildroot}%{ruby18_rootdir}%{_prefix}/lib/ruby/1.8

ruby setup.rb --rdoc --prefix=%{ruby18_rootdir}%{_prefix} --destdir=%{buildroot}

mv %{buildroot}%{ruby18_rootdir}%{_prefix}/lib/*.rb %{buildroot}%{ruby18_rootdir}%{_prefix}/lib/ruby/1.8
mv %{buildroot}%{ruby18_rootdir}%{_prefix}/lib/{rbconfig,rubygems} %{buildroot}%{ruby18_rootdir}%{_prefix}/lib/ruby/1.8

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ruby18_rootdir}%{_bindir}/gem
%{ruby18_rootdir}%{_prefix}/lib/ruby/1.8

%changelog
* Sun Feb 03 2013 RockStack <packages@rockstack.org> - 1.8.25-1
- Update to 1.8.25

* Fri Jun 22 2012 RockStack <packages@rockstack.org> - 1.8.24-1
- Initial build
