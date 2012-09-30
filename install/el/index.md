---
layout: default
title: Install (Enterprise Linux)
---

# Install (Enterprise Linux)

 1. Add YUM repo

        $ sudo cat << EOF > /etc/yum.repos.d/rock.repo
        [rock]
        name=EL \$releasever - \$basearch - Rock
        baseurl=http://dl.rockplatform.org/rp0/rpm/el/\$releasever/\$basearch
        gpgcheck=0
        EOF

 1. Install `rock` and runtimes (also see [Puppet module](https://github.com/rockplatform/puppet-rock))

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

 1. Continue to [getting started](/getting-started/) page
