---
layout: post
title: RockStack, rock 0.11 and more
---

The Rock Platform has been renamed to RockStack and URLs have changed along
with some paths.

 * New site: [www.rockstack.org][site]
 * New download site: [dl.rockstack.org][download]

The yum directory structure has changed and a testing repository has been
added, grab the updated [release rpm][release-rpm] to update.

[rock 0.11][pypi] ([diff][diff]) released.

 - Rename PROJECT\_PATH to ROCK\_PATH
 - Search directory path for .rock.yml (run rock from subdirectories)
 - Expose current working directory via ROCK\_CWD environment variable
 - Remove BUILD\_PATH, TEST\_PATH and other non-ROCK prefixed environment
   variables
 - Remove runtime\_type variable and associated configuration functionality

Runtime Changes

 - Update node08 from 0.8.11 to [0.8.14][node08]
 - Update perl516 from 5.16.1 to [5.16.2][perl516]
 - Update php54 from 5.4.7 to [5.4.8][php54], composer from alpha5 to
   [alpha6][php54-composer], enable most extensions by default in global
   php.ini, and add php54 [memcached][memcached] extension
 - Update ruby18 from patch 370 to [371][ruby18]
 - Update ruby19 from patch 194 to [327][ruby19]

[site]: http://www.rockstack.org/
[download]: http://dl.rockstack.org/
[release-rpm]: http://dl.rockstack.org/rpm/stable/el/rock-release.rpm
[pypi]: http://pypi.python.org/pypi/rock/0.11.0
[diff]: https://github.com/rockstack/rock/compare/0.9.0...0.11.0
[node08]: https://raw.github.com/joyent/node/v0.8.14/ChangeLog
[perl516]: http://search.cpan.org/dist/perl-5.16.2/pod/perldelta.pod
[php54]: http://www.php.net/ChangeLog-5.php#5.4.8
[php54-composer]: https://github.com/composer/composer/blob/935da3fdbc0bbc267a6a410a5eafb6cde3f9bd7d/CHANGELOG.md
[ruby18]: http://svn.ruby-lang.org/repos/ruby/tags/v1_8_7_371/ChangeLog
[ruby19]: http://www.ruby-lang.org/en/news/2012/11/09/ruby-1-9-3-p327-is-released/
[memcached]: http://pecl.php.net/package/memcached/2.1.0
