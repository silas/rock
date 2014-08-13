---
layout: post
title: rock 0.20, and runtime changes
---

[rock 0.20][pypi] ([diff][diff]) released.

 - Add bare runtimes: node, perl, php, python, and ruby (sets default tasks, but uses whatever is installed in your PATH)
 - Change runtime to be optional

Runtime Changes

 - Add perl520 [5.20.0][perl520]
 - Add python34 [3.4.1][python34]
 - Update node010 [0.10.30][node010]
 - Update node08 [0.8.28][node08]
 - Update php55 [5.5.15][php55]
 - Update php54 [5.4.31][php54]
 - Update python27 [2.7.8][python27], virtualenv [1.11.6][python-virtualenv]
 - Update ruby21 [2.1.2][ruby21], bundler [1.6.5][ruby21-bundler]
 - Remove perl516
 - Remove python33
 - Remove ruby19

[diff]: https://github.com/rockstack/rock/compare/0.19.0...0.20.0
[pypi]: http://pypi.python.org/pypi/rock/0.20.0
[node010]: https://raw.github.com/joyent/node/v0.10.30/ChangeLog
[node08]: https://raw.github.com/joyent/node/v0.8.28/ChangeLog
[perl520]: http://search.cpan.org/dist/perl-5.20.0/pod/perldelta.pod
[php55]: http://www.php.net/ChangeLog-5.php#5.5.15
[php54]: http://www.php.net/ChangeLog-5.php#5.4.31
[python-virtualenv]: https://raw.githubusercontent.com/pypa/virtualenv/1.11.6/docs/news.rst
[python34]: http://hg.python.org/cpython/raw-file/v3.4.1/Misc/NEWS
[python27]: http://hg.python.org/cpython/raw-file/v2.7.8/Misc/NEWS
[ruby21]: https://www.ruby-lang.org/en/news/2014/05/09/ruby-2-1-2-is-released/
[ruby21-bundler]: https://github.com/carlhuda/bundler/blob/v1.6.5/CHANGELOG.md
