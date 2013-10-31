Name:           rock
Version:        0.16.0
Release:        1%{?dist}
Summary:        Build, test and run applications

Group:          Development/Languages
License:        MIT
URL:            https://github.com/rockstack/rock
Source0:        http://pypi.python.org/packages/source/r/rock/rock-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  PyYAML
BUildRequires:  python-argparse
BuildRequires:  python-devel
BuildRequires:  python-nose
BuildRequires:  python-unittest2
Requires:       PyYAML
Requires:       python-argparse

%description
This is a cli tool that allows you to easily build, test and run applications.

%prep
%setup -q

%build
%{__python} setup.py build

%check
nosetests

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/%{name}
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-%{version}-py*.egg-info

%changelog
* Sat Oct 26 2013 RockStack <packages@rockstack.org> - 0.16.0-1
- Add Python 3 support
- Make rock mount configurable
- Add ARGV array and fix escape issues in environment

* Mon Apr 01 2013 RockStack <packages@rockstack.org> - 0.15.0-1
- Add init command
- Add ROCK_RUNTIME to environment
- Change rock build for php to include --dev option
- Change rock test for php to run phpunit ./tests

* Tue Mar 26 2013 RockStack <packages@rockstack.org> - 0.14.0-1
- Fix ROCK_SHELL usage
- Improve help

* Wed Mar 20 2013 RockStack <packages@rockstack.org> - 0.13.1-1
- Fix option parsing

* Wed Mar 13 2013 RockStack <packages@rockstack.org> - 0.13.0-1
- Remove subcommands
- Add argument parsing
- Add config command
- Remove create command
- Make SHELL configurable

* Fri Mar 08 2013 RockStack <packages@rockstack.org> - 0.12.0-1
- Remove platform
- Use yaml.safe_load
- Create lockfiles in build (node, python)
- Fix bundler flag positions

* Wed Dec 12 2012 RockStack <packages@rockstack.org> - 0.11.1-1
- Fix platform hook issue

* Tue Nov 20 2012 RockStack <packages@rockstack.org> - 0.11.0-1
- Rename ROCK_PWD to ROCK_CWD
- Use PERL_ARCHNAME to generate PERL5LIB
- Use composer instead of composer.phar
- PHP test now calls bare phpunit
- Remove php.ini usage and generation

* Sun Nov 18 2012 RockStack <packages@rockstack.org> - 0.10.0-1
- Rename PROJECT_PATH to ROCK_PATH
- Search directory path for .rock.yml file
- Make "rock run" from working directory when not a section command
- Remove BUILD_PATH from yaml files
- Remove runtime_type and make configuration files explicit
- Expose working directory to sections via ROCK_PWD

* Thu Oct 18 2012 RockStack <packages@rockstack.org> - 0.9.0-1
- Platform subcommand
- Run arguments
- Verbose flags in build deployment commands
- Remove build process run
- Fix user path search

* Sun Sep 30 2012 RockStack <packages@rockstack.org> - 0.8.1-1
- Add python-bottle which defaults to python33
- Remove distribute tar on create venv
- Revert php-slim to upstream

* Sat Sep 29 2012 RockStack <packages@rockstack.org> - 0.8.0-1
- Add python33 support
- Add --version flag

* Sun Sep 23 2012 RockStack <packages@rockstack.org> - 0.7.0-1
- Add env support
- Fix non-string type coercion in env

* Wed Sep 12 2012 RockStack <packages@rockstack.org> - 0.6.1-1
- Update to 0.6.1
- Fix missing template directory

* Wed Sep 12 2012 RockStack <packages@rockstack.org> - 0.6.0-1
- Update to 0.6.0

* Sat Aug 19 2012 RockStack <packages@rockstack.org> - 0.5.0-1
- Update to 0.5.0

* Fri Aug 18 2012 RockStack <packages@rockstack.org> - 0.4.0-1
- Update to 0.4.0

* Mon Aug 06 2012 RockStack <packages@rockstack.org> - 0.3.1-1
- Update to 0.3.1

* Thu Aug 02 2012 RockStack <packages@rockstack.org> - 0.3.0-1
- Update to 0.3.0

* Mon Jul 30 2012 RockStack <packages@rockstack.org> - 0.2.0-1
- Update to 0.2.0

* Mon Jul 23 2012 RockStack <packages@rockstack.org> - 0.1.1-1
- Update to 0.1.1
- Use env instead of straight bash

* Mon Jul 23 2012 RockStack <packages@rockstack.org> - 0.1.0-1
- Update to 0.1.0

* Wed Jul 18 2012 RockStack <packages@rockstack.org> - 0.0.3-1
- Update to 0.0.3

* Wed Jul 11 2012 RockStack <packages@rockstack.org> - 0.0.2-1
- Initial build
