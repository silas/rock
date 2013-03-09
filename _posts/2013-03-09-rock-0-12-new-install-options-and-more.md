---
layout: post
title: rock 0.12, new install options and more
---

[rock 0.12][pypi] ([diff][diff]) released.

 - Remove platform
 - Use yaml.safe_load instead of yaml.load
 - Create lockfiles in builds for node and python
 - Fix bundler flag usage

Install Changes

 - Install on [Debian/Ubuntu][deb] (big thanks to [Phi Reichenberger][preichenberger])
 - Install on [OS X][homebrew]
 - Remove Vagrant option

Runtime Changes

 - Update python27 virtualenv to 1.8.4, distribute to 0.6.34
 - Update node08 from 0.8.14 to [0.8.18][node08]
 - Update php54 from 5.4.8 to [5.4.11][php54]
 - Update ruby18 bundler to 1.2.3, rubygems to 1.8.25
 - Update ruby19 from patch 194 to [374][ruby19], bundler to 1.2.3

[deb]: http://www.rockstack.org/docs/install/deb/
[diff]: https://github.com/rockstack/rock/compare/0.11.0...0.12.0
[homebrew]: http://www.rockstack.org/docs/install/homebrew/
[node08]: https://raw.github.com/joyent/node/v0.8.14/ChangeLog
[php54]: http://www.php.net/ChangeLog-5.php#5.4.11
[preichenberger]: https://github.com/preichenberger
[pypi]: http://pypi.python.org/pypi/rock/0.12.0
[ruby19]: http://www.ruby-lang.org/en/news/2013/01/17/ruby-1-9-3-p374-is-released/
