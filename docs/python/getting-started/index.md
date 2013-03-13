---
layout: default
title: Getting Started with Python
---

# Getting Started with Python

This guide walks you through setting up a basic Python web application with
tests.

 1. Create and switch to project directory

        $ mkdir python-example
        $ cd python-example

 1. Create `.rock.yml`

        runtime: python27

 1. Create `requirements.txt`

        Flask

 1. Build project

        $ rock build

 1. Create `helloworld.py`

        from flask import Flask

        app = Flask(__name__)

        def greeting():
            return 'Hello World'

        @app.route('/')
        def index():
            return greeting()

 1. Create `bin` directory

        $ mkdir bin

 1. Create `bin/hello-world`

        #!/usr/bin/env python

        import os
        import helloworld

        port = int(os.environ.get('PORT', 8000))

        if __name__ == '__main__':
            helloworld.app.run(port=port)

 1. Make it executable

        $ chmod 755 bin/hello-world

 1. Start `hello-world` and kill it using Ctrl+C

        $ rock run hello-world
         * Running on http://127.0.0.1:8000/
        ^C

 1. Update `.rock.yml` to include an `env` and `run` section

        runtime: python27

        env:
	  PORT: "${PORT:-9000}"

        run: exec hello-world

 1. Run and kill it using Ctrl+C

        $ rock run
         * Running on http://127.0.0.1:9000/
        ^C

 1. Create `tests` directory

        $ mkdir tests

 1. Create `tests/test_greeting.py`

        import unittest
        import helloworld

        class GreetingTestCase(unittest.TestCase):

            def test_message(self):
                self.assertTrue(helloworld.greeting(), 'Hello World')

 1. Run tests

        .
        ----------------------------------------------------------------------
        Ran 1 test in 0.000s

        OK

 1. Update `.rock.yml` to include a simple frontpage test

        runtime: python27

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
