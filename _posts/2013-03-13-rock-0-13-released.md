---
layout: post
title: rock 0.13 released
---

[rock 0.13][pypi] ([diff][diff]) released.

 - Remove subcommands
 - Add argument parsing
 - Add config command
 - Remove create command
 - Make SHELL configurable

## Subcommands

Sections defined as `rock_web` were run as

``` console
$ rock run web
```

are now run as

``` console
$ rock run_web
```

## Build Deployment

The build deployment command has changed from

``` console
$ rock build deployment
```

to

``` console
$ rock build --deployment
```

This also means that if you extended the `build` or `build_deployment` sections
you'll need to update these from something like

``` yaml
build: |
  {{ '{{' }} parent }}
  make dev
  make static

build_deployment: |
  {{ '{{' }} parent }}
  make prod
  make static
```

to

``` yaml
build: |
  {{ '{{' }} parent }}
  if [[ "${ROCK_ARGS_DEPLOYMENT}" == "true" ]]; then
    make deployment
  else
    make dev
  fi
  make static
```

## Argument Parsing

rock now automatically parses and exposes command line arguments via environment
variables.

``` console
$ rock test one --two three --four=4 five
...
export ROCK_ARGV='one --two three --four=4 five'
export ROCK_ARGS='one three five'
export ROCK_ARG0='test'
export ROCK_ARG1='one'
export ROCK_ARG2='three'
export ROCK_ARG3='five'
export ROCK_ARGS_FOUR="4"
export ROCK_ARGS_TWO="true"
export ROCK_OPTS='TWO FOUR'
...
```

This works for any section except `run`, which just executes the run arguments
in your environment.

You can still define a `run` section, but it will only be executed if you type
`rock run` without any arguments.

[diff]: https://github.com/rockstack/rock/compare/0.12.0...0.13.0
[pypi]: http://pypi.python.org/pypi/rock/0.13.0
