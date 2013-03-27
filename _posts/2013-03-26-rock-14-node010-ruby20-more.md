---
layout: post
title: rock 0.14, node 0.10, ruby 2.0 and more
---

[rock 0.14][pypi] ([diff][diff]) released.

 - Fix ROCK\_SHELL usage ([diff][diff-rock-shell])
 - Improve help
 - Remove single character cli options (ex: -v, -h, etc...)

Runtime Changes

 - Add node010 [0.10.1][node010]
 - Add ruby20 [2.0.0 p0][ruby20]
 - Update node08 from 0.8.14 to [0.8.22][node08]
 - Update perl516 from 5.16.2 to [5.16.3][perl516], local::lib 1.008004 to
   [1.008009][perl516-local-lib], cpanm 1.5017 to [1.6008][perl516-cpanm],
   carton 0.9.7 to [0.9.10][perl516-carton]
 - Update ruby18 bundler from 1.2.3 to [1.3.4][ruby18-bundler]
 - Update ruby19 from patch 374 to [392][ruby19], bundler 1.2.3 to
   [1.3.4][ruby19-bundler]

[diff-rock-shell]: https://github.com/rockstack/rock/compare/0.13.1...0.14.0#diff-11
[diff]: https://github.com/rockstack/rock/compare/0.13.1...0.14.0
[node010]: https://raw.github.com/joyent/node/v0.10.1/ChangeLog
[node08]: https://raw.github.com/joyent/node/v0.8.22/ChangeLog
[perl516-carton]: http://cpansearch.perl.org/src/MIYAGAWA/carton-v0.9.10/Changes
[perl516-cpanm]: http://cpansearch.perl.org/src/MIYAGAWA/App-cpanminus-1.6008/Changes
[perl516-local-lib]: http://cpansearch.perl.org/src/APEIRON/local-lib-1.008009/Changes
[perl516]: http://search.cpan.org/dist/perl-5.16.3/pod/perldelta.pod
[pypi]: http://pypi.python.org/pypi/rock/0.14.0
[ruby18-bundler]: https://github.com/carlhuda/bundler/blob/v1.3.4/CHANGELOG.md
[ruby19-bundler]: https://github.com/carlhuda/bundler/blob/v1.3.4/CHANGELOG.md
[ruby19]: http://www.ruby-lang.org/en/news/2013/02/22/ruby-1-9-3-p392-is-released/
[ruby20]: http://www.ruby-lang.org/en/news/2013/02/24/ruby-2-0-0-p0-is-released/
