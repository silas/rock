---
layout: default
title: Install CentOS/RHEL
---

# Install CentOS/RHEL

Enterprise Linux 6.x is currently supported.

 1. First install the release package

    ``` console
    $ sudo rpm -i http://dl.rockstack.org/rpm/stable/el/rock-release.rpm
    ```

 1. Next install the rock command line tool and devtools

    ``` console
    $ sudo yum install rock rock-devtools
    ```

 1. And finally install whatever runtimes you'll need

    ``` console
    $ sudo yum install rock-runtime-node010
    ```

 1. Continue to [getting started](/docs/) page
