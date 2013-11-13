---
layout: default
title: Install OS X
---

# Install OS X

OS X 10.7 - 10.9 is currently supported via Homebrew.

## Automatic

 1. Run installer script

    ``` console
    $ bash -c "$(curl -fsSL https://raw.github.com/rockstack/utils/master/install)"
    ```

 1. Install whatever runtimes you'll need

    ``` console
    $ brew install rock-runtime-node010
    ```

## Manual

 1. Ensure [XCode][xcode] and the Command Line Tools are installed

 1. Ensure [Homebrew][homebrew] is installed

    ``` console
    $ ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
    ```

 1. Ensure Homebrew is up-to-date

    ``` console
    $ brew update
    ```

 1. Ensure Homebrew dupes is installed

    ``` console
    $ brew tap homebrew/dupes
    ```

 1. Add RockStack tap

    ``` console
    $ brew tap rockstack/rock
    ```

 1. Install rock command line tool

    ``` console
    $ brew install rock-cli
    ```

 1. And install whatever runtimes you'll need

    ``` console
    $ brew install rock-runtime-node010
    ```

[xcode]: http://itunes.apple.com/us/app/xcode/id497799835
[homebrew]: https://brew.sh
