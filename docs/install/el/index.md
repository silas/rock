---
layout: default
title: Install (Enterprise Linux)
---

# Install (Enterprise Linux)

 1. Add YUM repo

        $ sudo rpm -i http://dl.rockstack.org/rpm/stable/el/rock-release.rpm

 1. Install `rock` and runtimes

        $ sudo yum install -y \
            rock \
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
