---
layout: default
title: rock
---

# rock

The rock command line tool is used to build, test and run applications in
RockStack. It does this by merging configuration files, manipulating
environment variables and executing bash scripts.

## Configuration

rock uses as series of configuration files to get the environment into a state
where applications can run. It also defines defaults for things like builds and
tests.

The three main types of configuration files are:

 * runtime system configuration
 * runtime application configuration
 * project configuration

The runtime system configuration files setup runtime specific environment
variables. Normally these include the PATH variable and some architecture and
package specific variables. These configuration files are usually shipped with
the runtime package and can be found at `/opt/rock/runtime/<runtime>/rock.yml`.

    env:
      PATH: "/opt/rock/runtime/node08/usr/bin:${PATH}"

The default runtime application configuration files are shipped with the rock
command line tool, but can be extended or overridden on a system, user and
project basis. These files define how applications in a particular runtime are
built and tested. They can be found in the data/runtime directory in the rock
installation and can be extended from `/etc/rock/runtime/<runtime>.yml`,
`~/.rock/runtime/<runtime>.yml` and `.rock.yml`.

    env:
      PATH: "${ROCK_PATH}/bin:${ROCK_PATH}/node_modules/.bin:${PATH}"

    build: npm install

    test: npm test

The project configuration file sets the runtime and can extend any of the above.

    runtime: node08

    run: node app.js
    run_web: node app.js --cluster

    build: |
      {{ '{{' }} parent }}
      make static

All of these files a parsed and merged in the same way, the difference between
them is the order in which they are evaluated and the content they normally
contain.

Running the test command would evaluate to something like:

    $ rock --dry-run test
    ...
    export PATH="/example/bin:/example/node_modules/.bin:/opt/rock/runtime/node08/usr/bin:${PATH}"
    ...
    npm test

## Commands

The primary rock commands are build, test and run.
