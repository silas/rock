---
layout: default
title: Install CentOS/RHEL
---

# Install CentOS/RHEL

Enterprise Linux 6.x is currently supported.

## Automatic

 1. Run installer script

    ``` console
    $ bash -c "$(curl -fsSL https://raw.github.com/rockstack/utils/master/install)"
    ```

 1. Install whatever runtimes you'll need

    ``` console
    $ sudo yum install rock-runtime-node010
    ```

## Manual

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
