---
layout: default
title: Install Ubuntu LTS
---

# Install Ubuntu LTS

Ubuntu 12.04 is currently supported.

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

 1. Continue to [getting started](/docs/) page
