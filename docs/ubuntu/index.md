---
layout: default
title: Install Ubuntu LTS
---

*NOTE: Ubuntu is no longer supported.*

# Install Ubuntu LTS

Ubuntu 12.04 is currently supported.

## Automatic

 1. Run installer script

    ``` console
    $ bash -c "$(curl -fsSL https://raw.github.com/rockstack/utils/master/install)"
    ```

 1. Install whatever runtimes you'll need

    ``` console
    $ sudo apt-get install rock-runtime-node010
    ```

## Manual

 1. First install the release package

    ``` console
    $ curl http://dl.rockstack.org/deb/rock-release-precise.deb -o rock-release.deb
    $ sudo dpkg -i rock-release.deb
    $ sudo apt-get update
    ```

 1. Next install the rock command line tool and devtools

    ``` console
    $ sudo apt-get install rock rock-devtools
    ```

 1. And finally install whatever runtimes you'll need

    ``` console
    $ sudo apt-get install rock-runtime-node010
    ```
