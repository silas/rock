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

The primary rock commands are build, test, run and clean.

### build

The build command is used to get the project into a state where it can run.

There are two primary types of builds, a developer build (`rock build`) and a
deployment build (`rock build --deployment`). In most runtimes the primary
difference between the builds is that the deployment build requires a lock file
(ex: `Gemfile.lock`, `npm-shrinkwrap.json`, etc..), but the distinction can
also be exploited to setup things like commit hooks or build static resources.

    runtime: node08

    build: |
      {{ '{{' }} parent }}

      if [[ "${ROCK_ARGS_DEPLOYMENT}" == "true" ]]; then
        make static
      else
        ./misc/setup-git-hooks
      fi

### test

The test command is used to test the project, using a built-in (or the most
normal) tool.

In many projects this section will be overridden to use whatever framework,
tool or options the project requires.

To figure out what gets run use the `--dry-run` option.

    $ rock --dry-run test
    ...
    python -m unittest discover ./tests

And define a `test` section in the `.rock.yml` file to change it.

    runtime: python27

    test: exec nosetests ${ROCK_ARGV}

### run

The run command has two to primary functions, the first is to document how the
application should be run in development mode, and the second is to allow the
running of arbitrary commands in the project environment.

Unlike the other primary commands the run command doesn't come with a default
definition; it's up to the developer to define one.

    runtime: php54

    run: exec php -S "${HOST:-127.0.0.1}:${PORT:-8000}" -t ./public

Also unlike the other commands, you can't pass arguments to the run command.
Instead if the run command is called with arguments rock assumes your running a
command in the project environment.

    $ rock run php --version

### clean

The clean command simply removes the files created by the build command.

    runtime: ruby19

    clean: |
      {{ '{{' }} parent }}

      rm -fr ./tmp/*
