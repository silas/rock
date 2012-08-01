---
layout: default
title: Getting Started with Node
---

# Getting Started with Node

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

        app.get('/', function(req, res){
          res.send('Hello World');
        });

        app.set('port', 8000);

        module.exports = app;

 1. Create `bin` directory

        $ mkdir bin

 1. Create `bin/hello-world`

        #!/usr/bin/env node

        var server = require('../server');

        var port = parseInt(process.env.HTTP_PORT);

        if (port) {
          server.set('port', port);
        }

        server.listen(server.get('port'));

        console.log('Listening on port ' + server.get('port'));

 1. Make it executable

        $ chmod 755 bin/hello-world

 1. Start `hello-world` and kill it using Ctrl+C

        $ rock run hello-world
        Listening on port 8000
        ^C

 1. Update `.rock.yml` to include a run alias that defaults to port 9000

        runtime: node08

        run_web: HTTP_PORT=${HTTP_PORT-9000} hello-world

 1. Run `web` and kill it using Ctrl+C

        $ rock run web
        Listening on port 9000
        ^C

 1. Create `test.js`

        var assert = require('assert');
        var server = require('./server');

        assert.equal(server.get('port'), 8000);

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

 1. Create deployment build requirements

        $ rock run npm shrinkwrap

 1. Clean project root, run deployment build and run tests to ensure build worked

        $ rock clean
        $ rock build deployment
        $ rock test
