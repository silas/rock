---
layout: default
title: Getting Started with PHP
---

# Getting Started with PHP

This guide walks you through setting up a basic PHP web application with tests.

 1. Create and switch to project directory

        $ mkdir php-example
        $ cd php-example

 1. Create `.rock.yml`

        runtime: php54

 1. Create `composer.json`

        {
            "require": {
                "phpunit/phpunit": "*",
                "slim/slim": "*"
            }
        }

 1. Build project

        $ rock build

 1. Create `public` directory

        $ mkdir public

 1. Create `lib` directory

        $ mkdir lib

 1. Create `lib/web.php`

        <?php

        require __DIR__ . '/../vendor/autoload.php';

        function greeting() {
            return 'Hello World';
        }

 1. Create `public/index.php`

        <?php

        require __DIR__ . '/../lib/web.php';

        $app = new \Slim\Slim();

        $app->get('/', function () {
            echo greeting();
        });

        $app->run();

 1. Create `bin` directory

        $ mkdir bin

 1. Create `bin/hello-world`

        #!/usr/bin/env bash

        exec php -S "${HOST:-127.0.0.1}:${PORT:-8000}" -t "${ROCK_PATH}/public"

 1. Make it executable

        $ chmod 755 bin/hello-world

 1. Start `hello-world` and kill it using Ctrl+C

        $ rock run hello-world
        PHP 5.4.4 Development Server started at Wed Aug  1 18:00:00 2012
        Listening on 127.0.0.1:8000
        Document root is /home/vagrant/php-example/public
        Press Ctrl-C to quit.
        ^C

 1. Update `.rock.yml` to include an `env` and `run` section

        runtime: php54

        env:
          PORT: "${PORT:-9000}"

        run: exec hello-world

 1. Run and kill it using Ctrl+C

        $ rock run
        PHP 5.4.4 Development Server started at Wed Aug  1 18:05:00 2012
        Listening on 127.0.0.1:9000
        Document root is /home/vagrant/php-example/public
        Press Ctrl-C to quit.
        ^C

 1. Create `phpunit.xml`

        <phpunit bootstrap="vendor/autoload.php">
          <testsuites>
            <testsuite name='Simple tests'>
              <directory suffix='.php'>./tests</directory>
            </testsuite>
          </testsuites>
        </phpunit>

 1. Create `tests` directory

        $ mkdir tests

 1. Create `tests/basic.php`

        <?php

        require __DIR__ . '/../lib/web.php';

        class Test extends PHPUnit_Framework_TestCase {
            public function testGreeting() {
                $this->assertEquals('Hello World', greeting());
            }
        }

 1. Run tests

        $ rock test
        PHPUnit 3.6.10 by Sebastian Bergmann.

        Configuration read from /home/vagrant/php-example/phpunit.xml

        .

        Time: 0 seconds, Memory: 2.75Mb

        OK (1 test, 1 assertion)

 1. Update `.rock.yml` to include a simple frontpage test

        runtime: php54

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

 1. Run `frontpage` tests

        $ rock test_frontpage
        OK

 1. Clean project root, run deployment build and run tests to ensure build worked

        $ rock clean
        $ rock build --deployment
        $ rock test
