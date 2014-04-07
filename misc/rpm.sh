yum clean all

yum install -y \
  createrepo \
  curl \
  fedora-packager \
  mock \
  python-pip

pip install ops

usermod vagrant -G mock

echo '#!/usr/bin/env python' > /usr/local/bin/brpm

curl -s https://raw.github.com/silas/brpm/master/brpm.py >> /usr/local/bin/brpm

chmod 755 /usr/local/bin/brpm
