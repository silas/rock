%global  root                /opt/rock/platform

Name:              rock-platform-nginx
Version:           1.2.4
Release:           1%{?dist}

Summary:           A high performance web server and reverse proxy server
Group:             System Environment/Daemons
# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:           BSD
URL:               http://nginx.org

Source0:           http://nginx.org/download/nginx-%{version}.tar.gz
Source1:           404.html
Source2:           50x.html

# removes -Werror in upstream build scripts.  -Werror conflicts with
# -D_FORTIFY_SOURCE=2 causing warnings to turn into errors.
Patch0:            nginx-auto-cc-gcc.patch

BuildRequires:     pcre-devel
BuildRequires:     zlib-devel
Requires:          pcre

%description
Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and
IMAP protocols, with a strong focus on high concurrency, performance and low
memory usage.

%prep
%setup -q -n nginx-%{version}
%patch0 -p0

%build
# nginx does not utilize a standard configure script.  It has its own
# and the standard configure options cause the nginx configure script
# to error out.  This is is also the reason for the DESTDIR environment
# variable.
export DESTDIR=%{buildroot}
./configure \
    --prefix=%{root}%{_datadir}/nginx \
    --sbin-path=%{root}%{_sbindir}/nginx \
    --conf-path=nginx.conf \
    --error-log-path=error.log \
    --http-log-path=access.log \
    --http-client-body-temp-path=tmp/client-body \
    --http-proxy-temp-path=tmp/proxy \
    --http-fastcgi-temp-path=tmp/fastcgi \
    --pid-path=nginx.pid \
    --lock-path=nginx.lock \
    --with-file-aio \
    --with-ipv6 \
    --with-http_realip_module \
    --with-http_gzip_static_module \
    --with-http_stub_status_module \
    --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
    --with-ld-opt="-Wl,-E" # so the perl module finds its symbols

make %{?_smp_mflags} 

%install
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor

find %{buildroot} -type f -empty -exec rm -f '{}' \;
find %{buildroot} -type f -iname '*.so' -exec chmod 0755 '{}' \;

install -p -d -m 0755 %{buildroot}%{root}%{_datadir}/nginx/html

install -p -m 0644 %{SOURCE1} %{SOURCE2} \
    %{buildroot}%{root}%{_datadir}/nginx/html
install -p -D -m 0644 %{SOURCE1} \
    %{buildroot}%{root}%{_datadir}/nginx/html/index.html

%files
%doc LICENSE CHANGES README
%{root}%{_datadir}/nginx
%{root}%{_sbindir}/nginx

%changelog
* Sat Oct 06 2012 Silas Sewell <silas@sewell.org> - 1.2.4-1
- Update to 1.2.4
- Namespace for rock
- Remove un-needed features

* Mon May 14 2012 Jamie Nguyen <jamie@tomoyolinux.co.uk> - 1.0.15-2
- fix postrotate script in nginx.logrotate (#705264)

* Thu Apr 19 2012 Jamie Nguyen <jamie@tomoyolinux.co.uk> - 1.0.15-1
- update to upstream release 1.0.15
- CVE-2012-2089 (#812093)

* Thu Mar 15 2012 Jamie Nguyen <jamie@tomoyolinux.co.uk> - 1.0.14-1
- update to upstream release 1.0.14
- CVE-2012-1180 (#803856)

* Wed Mar 04 2012 Jamie Nguyen <jamie@tomoyolinux.co.uk> - 1.0.13-2
- remove incorrect BR

* Tue Mar 03 2012 Jamie Nguyen <jamie@tomoyolinux.co.uk> - 1.0.13-1
- update to upstream release 1.0.13
- general spec file cleanup to match rawhide (for easier diff), including:
- replace %%define with %%global
- amend nginx.init and nginx.conf
- amend %%pre scriptlet to match with guidelines
- remove obsolete BuildRoot tag, %%clean section and %%defattr
- remove various unnecessary commands

* Sun Feb 19 2012 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.12-1
- Update to 1.0.12

* Thu Dec 14 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.10-2
- Fix Build Issue

* Thu Nov 17 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.10-1
- Bugfix: a segmentation fault might occur in a worker process if resolver got a big DNS response. Thanks to Ben Hawkes.
- Bugfix: in cache key calculation if internal MD5 implementation wasused; the bug had appeared in 1.0.4.
- Bugfix: the module ngx_http_mp4_module sent incorrect "Content-Length" response header line if the "start" argument was used. Thanks to Piotr Sikora.

* Thu Oct 27 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.8-1
- Update to new 1.0.8 stable release

* Fri Aug 26 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.5-1
- Update nginx to Latest Stable Release

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0.0-3
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0.0-2
- Perl 5.14 mass rebuild

* Wed Apr 27 2011 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.0-1
- Update to 1.0.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.53-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53.5
- Extract out default config into its own file (bug #635776)

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-4
- Revert ownership of log dir

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-3
- Change ownership of /var/log/nginx to be 0700 nginx:nginx
- update init script to use killproc -p
- add reopen_logs command to init script
- update init script to use nginx -q option

* Sun Oct 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-2
- Fix linking of perl module

* Sun Oct 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-1
- Update to new stable 0.8.53

* Sat Jul 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.67-2
- add Provides: webserver (bug #619693)

* Sun Jun 20 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.67-1
- Update to new stable 0.7.67
- fix bugzilla #591543

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.7.65-2
- Mass rebuild with perl-5.12.0

* Mon Feb 15 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.65-1
- Update to new stable 0.7.65
- change ownership of logdir to root:root
- add support for ipv6 (bug #561248)
- add random_index_module
- add secure_link_module

* Fri Dec 04 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.64-1
- Update to new stable 0.7.64

* Tue Oct 29 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.63-1
- Update to new stable 0.7.63
- reinstate zlib dependency

* Mon Sep 14 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.62-1
- Update to new stable 0.7.62
- fixes CVE-2009-2629
- fix rpmlint zlib dependency complaint

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.7.61-2
- rebuilt with new openssl

* Sun Aug 02 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.61-1
- Update to new stable 0.7.61

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.36-2
- init script updates from Gena Makhomed
- remove nginx-upstream-fair

* Sat Apr 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.36-1
-  update to 0.6.36

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.35-2
- rebuild

* Thu Feb 19 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.35-1
- update to 0.6.35

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.6.34-2
- rebuild with new openssl

* Tue Dec 30 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.34-1
- update to 0.6.34

* Thu Dec  4 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.6.33-2
- Fix inclusion of /usr/share/nginx tree => no unowned directories.

* Sun Nov 23 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.33-1
- update to 0.6.33

* Tue Jul 22 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.32-1
- update to 0.6.32
- nginx now supports DESTDIR so removed the patches that enabled it 

* Mon May 26 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.31-3
- init script fixes
- resolve 'listen 80 default' [#447873]

* Mon May 12 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.31-2
- update to 0.6.31

* Sun May 11 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.30-2
- upate to new upstream stable branch 0.6
- added 3rd party module nginx-upstream-fair
- added default webpages

* Sun Apr 20 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.5.35-2
- update init script to match recommended guidelines
- add /etc/nginx/conf.d support [#443280]
- use /etc/sysconfig/nginx to determine nginx.conf [#442708]

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.5.35-3
- add Requires for versioned perl (libperl.so)
- drop silly file Requires

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.35-2
- Autorebuild for GCC 4.3

* Sat Jan 19 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.5.35-1
- update to 0.5.35

* Sat Dec 15 2007 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.5.34-1
- update to 0.5.34

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.5.33-2
 - Rebuild for deps

* Sun Nov 11 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.33-1
- update to 0.5.33

* Mon Sep 24 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.32-1
- updated to 0.5.32
- fixed rpmlint UTF-8 complaints.

* Sat Aug 18 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.31-2
- added --with-http_stub_status_module build option.
- added --with-http_sub_module build option.
- added use of pcre-config --cflags

* Fri Aug 17 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.31-1
- Update to 0.5.31
- specify license is BSD

* Sat Aug 11 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.30-2
- Add BuildRequires: perl-devel - fixing rawhide build

* Mon Jul 30 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.30-1
- Update to 0.5.30

* Tue Jul 24 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.29-1
- Update to 0.5.29

* Wed Jul 18 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.28-1
- Update to 0.5.28

* Mon Jul 09 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.27-1
- Update to 0.5.27

* Mon Jun 18 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.26-1
- Update to 0.5.26

* Sat Apr 28 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.19-1
- Update to 0.5.19

* Mon Apr 02 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.17-1
- Update to 0.5.17

* Mon Mar 26 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.16-1
- Update to 0.5.16
- add ownership of /usr/share/nginx/html (#233950)

* Fri Mar 23 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.15-3
- fixed package review bugs (#235222) given by ruben@rubenkerkhof.com

* Thu Mar 22 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.15-2
- fixed package review bugs (#233522) given by kevin@tummy.com

* Thu Mar 22 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.15-1
- create patches to assist with building for Fedora
- initial packaging for Fedora
