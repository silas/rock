---
layout: default
title: Getting Started with PHP
---

# Getting Started with PHP

 1. Create and switch to project directory

        $ mkdir php-example
        $ cd php-example

 1. Create `.rock.yml`

        runtime: php54

 1. Create `php.ini`

        extension=dom.so

 1. Create `composer.json`

        {
            "require": {
                "EHER/PHPUnit": "*",
                "slim/slim": "*"
            }
        }

 1. Build project

        $ rock build

 1. Create `public` directory

        $ mkdir public

 1. Create `public/web.php`

        <?php

        require __DIR__ . '/../vendor/autoload.php';

        function greeting() {
            return 'Hello World';
        }

        function app() {
            $app = new Slim();

            $app->get('/', function () {
                echo greeting();
            });

            return $app;
        }

 1. Create `public/index.php`

        <?php

        require __DIR__ . '/web.php';

        app()->run();

 1. Create `bin` directory

        $ mkdir bin

 1. Create `bin/hello-world`

        #!/usr/bin/env bash

        exec php -S "${HTTP_HOST-127.0.0.1}:${HTTP_PORT-8000}" -c "${PROJECT_PATH}/php.ini" -t "${PROJECT_PATH}/public"

 1. Make it executable

        $ chmod 755 bin/hello-world

 1. Start `hello-world` and kill it using Ctrl+C

        $ rock run hello-world
        PHP 5.4.4 Development Server started at Wed Aug  1 18:00:00 2012
        Listening on 127.0.0.1:8000
        Document root is /home/vagrant/php-example/public
        Press Ctrl-C to quit.
        ^C

 1. Update `.rock.yml` to include a run alias that defaults to port 9000

        runtime: php54

        run_web: HTTP_PORT=${HTTP_PORT-9000} hello-world

 1. Run `web` and kill it using Ctrl+C

        $ rock run web
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

        require __DIR__ . '/../public/web.php';

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

        run_web: HTTP_PORT=${HTTP_PORT-9000} hello-world

        test_frontpage: |

          # start server
          rock run web &>/dev/null &

          # give it a little time to start
          sleep 0.2

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

        $ rock test frontpage
        OK

 1. Clean project root, run deployment build and run tests to ensure build worked

        $ rock clean
        $ rock build deployment
        $ rock test
