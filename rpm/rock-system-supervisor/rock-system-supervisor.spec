%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global real_name supervisor
%global rev b1
%global root /opt/rock/system

Name:             rock-system-supervisor
Version:          3.0
Release:          0.3%{?rev:.%{rev}}%{?dist}
Summary:          A System for Allowing the Control of Process State on UNIX

Group:            System Environment/Base
License:          ZPLv2.1 and BSD and MIT
URL:              http://supervisord.org
Source0:          http://pypi.python.org/packages/source/s/supervisor/supervisor-%{version}%{?rev}.tar.gz
Source1:          %{name}d.init
Source2:          supervisord.conf
Source3:          %{name}.logrotate
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:        noarch

BuildRequires:    python-devel
BuildRequires:    python-setuptools
BuildRequires:    python-meld3 >= 0.6.7
BuildRequires:    python-mock

Requires:         python-meld3 >= 0.6.7
Requires:         python-setuptools
Requires:         logrotate
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description
The supervisor is a client/server system that allows its users to control a
number of processes on UNIX-like operating systems.

%prep
%setup -q -n %{real_name}-%{version}%{?rev}

%build
CFLAGS="%{optflags}" python setup.py build

%install
rm -rf %{buildroot}

python setup.py install --skip-build --root %{buildroot} --prefix %{root}%{_prefix}

mkdir -p %{buildroot}%{_sysconfdir}/rock/system/supervisord.d

install -p -m 770 -d %{buildroot}%{_localstatedir}/log/%{name}
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}d
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rock/system/supervisord.conf
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

sed -i s'/^#!.*//' $( find %{buildroot}%{root}%{python_sitelib}/supervisor -type f)

touch %{buildroot}%{root}%{python_sitelib}/%{real_name}/__init__.py

rm -f %{buildroot}%{_prefix}/doc/*.txt

cat << EOF > %{buildroot}%{root}%{_bindir}/supervisorctl
#!/usr/bin/env python
import sys
sys.path.insert(0, '%{root}%{python_sitelib}')
from supervisor.supervisorctl import main
main()
EOF

cat << EOF > %{buildroot}%{root}%{_bindir}/supervisord
#!/usr/bin/env python
import sys
sys.path.insert(0, '%{root}%{python_sitelib}')
from supervisor.supervisord import main
main()
EOF

%clean
rm -rf %{buildroot}

%check
python setup.py test -q

%post
/sbin/chkconfig --add %{name}d || :

%preun
if [ $1 = 0 ]; then
  /sbin/service %{name}d stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}d || :
fi

%files
%defattr(-,root,root,-)
%doc README.rst LICENSES.txt TODO.txt CHANGES.txt COPYRIGHT.txt
%config(noreplace) %{_sysconfdir}/rock/system/supervisord.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %{_sysconfdir}/rock/system/supervisord.d
%dir %{_localstatedir}/log/%{name}
%{_initrddir}/%{name}d
%{root}%{python_sitelib}/*
%{root}%{_bindir}/supervisor*
%{root}%{_bindir}/echo_supervisord_conf
%{root}%{_bindir}/pidproxy

%changelog
* Sat Oct 06 2012 Silas Sewell <silas@sewell.org> - 3.0-0.3.b1
- Update to b1
- Namespace for rock

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.0-0.2.a8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 13 2010 Nils Philippsen <nils@redhat.com> - 3.0-0.1.a8
- add BR: python-setuptools

* Mon Apr 12 2010 Nils Philippsen <nils@redhat.com>
- bundle updated config file

* Sat Apr 10 2010 Nils Philippsen <nils@redhat.com>
- version 3.0a8
- update URLs
- versionize python-meld3 dependency

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.1-6
- Rebuild for Python 2.6

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1-5
- fix license tag

* Mon Jan 07 2008 Toshio Kuratomi <toshio@fedoraproject.org>  2.1-4
- Include egginfo files when python generates them.

* Sun Apr 22 2007 Mike McGrath <mmcgrath@redhat.com> 2.1-3
- Added BuildRequires of python-devel

* Fri Apr 20 2007 Mike McGrath <mmcgrath@redhat.com> 2.1-2
- Added patch suggested in #153225

* Fri Apr 20 2007 Mike McGrath <mmcgrath@redhat.com> 2.1-1
- Initial packaging

