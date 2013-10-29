---
layout: default
title: Install OS X
---

OS X 10.7 - 10.9 is currently supported via Homebrew.

# Run the setup script

 1. Ensure you have [XCode][xcode] and the Command Line Tools installed

 1. Run the setup script

    ``` console
    $ bash -c "$( curl -fsSL https://raw.github.com/rockstack/homebrew-rock/master/go )"
    ```

 1. And install whatever runtimes you'll need

    ``` console
    $ brew install rock-runtime-node010
    ```

 1. Continue to [getting started](/docs/) page

[xcode]: http://itunes.apple.com/us/app/xcode/id497799835
