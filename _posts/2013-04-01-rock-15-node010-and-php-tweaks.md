---
layout: post
title: rock 0.15, node 0.10.2 and php tweaks
---

[rock 0.15][pypi] ([diff][diff]) released.

 - Add init command
 - Add ROCK\_RUNTIME to environment
 - Change rock build for php to include --dev option
 - Change rock test for php to run phpunit ./tests

Runtime Changes

 - Update node010 from 0.10.1 to [0.10.2][node010]

[diff]: https://github.com/rockstack/rock/compare/0.14.0...0.15.0
[node010]: https://raw.github.com/joyent/node/v0.10.2/ChangeLog
[pypi]: http://pypi.python.org/pypi/rock/0.15.0
