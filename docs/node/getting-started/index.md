---
layout: default
title: Getting Started with Node
---

# Getting Started with Node

This guide walks you through setting up a basic Node.js web application with
tests.

 1. Create and switch to project directory

        $ mkdir node-example
        $ cd node-example

 1. Create `.rock.yml`

        runtime: node08

 1. Create `package.json`

        {
          "name": "helloworld",
          "description": "hello world test server",
          "version": "0.0.1",
          "private": true,
          "dependencies": {
            "express": "*"
          }
        }

 1. Build project

        $ rock build

 1. Create `server.js`

        var express = require('express');

        var app = express();

        app.greeting = function() {
          return 'Hello World';
        }

        app.get('/', function(req, res) {
          res.send(app.greeting());
        });

        module.exports = app;

 1. Create `bin` directory

        $ mkdir bin

 1. Create `bin/hello-world`

        #!/usr/bin/env node

        var server = require('../server');

        var port = parseInt(process.env.PORT) || 8000;

        server.listen(port);

        console.log('Listening on port ' + port);

 1. Make it executable

        $ chmod 755 bin/hello-world

 1. Start `hello-world` and kill it using Ctrl+C

        $ rock run hello-world
        Listening on port 8000
        ^C

 1. Update `.rock.yml` to include an `env` and `run` section

        runtime: node08

        env:
          PORT: "${PORT:-9000}"

        run: exec hello-world

 1. Run and kill it using Ctrl+C

        $ rock run
        Listening on port 9000
        ^C

 1. Create `test.js`

        var assert = require('assert');
        var server = require('./server');

        assert.equal(server.greeting(), 'Hello World');

 1. Update `package.json` to include test script

        {
          "name": "helloworld",
          "description": "hello world test server",
          "version": "0.0.1",
          "private": true,
          "dependencies": {
            "express": "*"
          },
          "scripts": {
            "test": "node test.js"
          }
        }

 1. Run tests

        $ rock test

        > helloworld@0.0.1 test /home/vagrant/node-example
        > node test.js

 1. Update `.rock.yml` to include a simple frontpage test

        runtime: node08

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
