#!/usr/bin/env bash

perl516_prefix=$1

cat << EOF > carton
#!/usr/bin/env bash

perl \
  -Mlocal::lib=$perl516_prefix/lib/carton \
  $perl516_prefix/lib/carton/bin/carton "\$@"
EOF
