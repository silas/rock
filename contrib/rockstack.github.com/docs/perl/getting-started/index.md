---
layout: default
title: Getting Started with Perl
---

# Getting Started with Perl

This guide walks you through setting up a basic Perl web application with
tests.

 1. Create and switch to project directory

    ``` console
    $ mkdir perl-example
    $ cd perl-example
    ```

 1. Initialize the project

    ``` console
    $ rock --runtime=perl516 init
    ```

 1. Edit `cpanfile`

    ``` perl
    requires 'Dancer';
    ```

 1. Build project

    ``` console
    $ rock build
    ```

 1. Create `lib` directory

    ``` console
    $ mkdir lib
    ```

 1. Create `lib/HelloWorld.pm`

    ``` perl
    package HelloWorld;

    use strict;
    use warnings;

    use Dancer qw{get setting};

    sub greeting {
        return 'Hello World';
    }

    get '/' => sub {
        greeting
    };

    1;
    ```

 1. Create `bin` directory

    ``` console
    $ mkdir bin
    ```

 1. Create `bin/hello-world`

    ``` perl
    #!/usr/bin/env perl

    use strict;
    use warnings;

    use Dancer qw{dance setting};

    use HelloWorld ();

    my $port = defined $ENV{PORT} ? int($ENV{PORT}) : 0;

    setting('port', $port || 8000);

    dance;
    ```

 1. Make it executable

    ``` console
    $ chmod 755 bin/hello-world
    ```

 1. Start `hello-world` and kill it using Ctrl+C

    ``` console
    $ rock run hello-world
    >> Dancer 1.3098 server 9820 listening on http://0.0.0.0:8000
    == Entering the development dance floor ...
    ^C
    ```

 1. Update `.rock.yml` to include an `env` and `run` section

    ``` yaml
    runtime: perl516

    env:
      PORT: "${PORT:-9000}"

    run: exec hello-world
    ```

 1. Run and kill it using Ctrl+C

    ``` console
    $ rock run
    >> Dancer 1.3098 server 9821 listening on http://0.0.0.0:9000
    == Entering the development dance floor ...
    ^C
    ```

 1. Create `t` directory

    ``` console
    $ mkdir t
    ```

 1. Create `t/01_port.t`

    ``` perl
    use Test::More tests => 2;

    use strict;
    use warnings;

    use_ok 'HelloWorld';

    is HelloWorld::greeting(), 'Hello World';
    ```

 1. Run tests

    ``` console
    $ rock test
    t/01_port.t .. ok   
    All tests successful.
    Files=1, Tests=2,  0 wallclock secs ( 0.02 usr  0.00 sys +  0.10 cusr  0.01 csys =  0.13 CPU)
    Result: PASS
    ```

 1. Update `.rock.yml` to include a simple frontpage test

    ``` yaml
    runtime: perl516

    env:
      PORT: "${PORT:-9000}"

    run: exec hello-world

    test_frontpage: |

      # start server
      rock run &>/dev/null &

      # give it a second to start
      sleep 1

      # get frontpage body
      body="$( curl -s 'http://127.0.0.1:9000/' )"

      # kill server
      kill %1

      # check response body
      if [[ "$body" != 'Hello World' ]]; then
        die "ERROR: '$body' != 'Hello World'"
      else
        echo 'OK'
      fi
    ```

 1. Run `frontpage` tests

    ``` console
    $ rock test_frontpage
    OK
    ```

 1. Clean project root, run deployment build and run tests to ensure build worked

    ``` console
    $ rock clean
    $ rock build --deployment
    $ rock test
    ```
