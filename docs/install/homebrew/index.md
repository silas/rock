---
layout: default
title: Install (Homebrew)
---

# Install (Homebrew)

 1. Ensure you have the requirements

    * An Intel CPU
    * OS X 10.6 or higher
    * [XCode](http://itunes.apple.com/us/app/xcode/id497799835)

 1. Install base

        $ curl -sL https://raw.github.com/rockstack/homebrew-rock/master/go | bash

 1. Install runtimes

        $ brew install \
            rock-runtime-node04 \
            rock-runtime-node06 \
            rock-runtime-node08 \
            rock-runtime-perl516 \
            rock-runtime-php54 \
            rock-runtime-python27 \
            rock-runtime-python33 \
            rock-runtime-ruby18 \
            rock-runtime-ruby19

 1. Continue to [getting started](/docs/) page
