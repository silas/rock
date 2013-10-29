---
layout: post
title: rock 0.16 and runtime updates
---

[rock 0.16][pypi] ([diff][diff]) released.

 - Make rock mount configurable
 - Add ARGV array and fix escape issues in environment
 - Client should support Python 3 now

Runtime Changes

 - No longer supported: node04, node06
 - Update node08 to [0.8.26][node08]
 - Update node010 to [0.10.21][node010]
 - Update php54 to [5.4.16][php54], virtualenv to [1.10][python27-virtualenv]
 - Update python27 to [2.7.5][python27]
 - Update python33 to [3.3.2][python33]
 - Update ruby20 to [2.0.0 p247][ruby20]

[diff]: https://github.com/rockstack/rock/compare/0.15.0...0.16.0
[node08]: https://raw.github.com/joyent/node/v0.8.26/ChangeLog
[node010]: https://raw.github.com/joyent/node/v0.10.21/ChangeLog
[php54]: http://www.php.net/ChangeLog-5.php#5.4.11
[pypi]: http://pypi.python.org/pypi/rock/0.16.0
[python27-virtualenv]: https://raw.github.com/pypa/virtualenv/1.10/docs/news.rst
[python27]: http://www.python.org/getit/releases/2.7.5/
[python33]: http://www.python.org/getit/releases/3.3.2/
[ruby20]: https://www.ruby-lang.org/en/news/2013/06/27/ruby-2-0-0-p247-is-released/
