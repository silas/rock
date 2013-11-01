#!/usr/bin/env bash

perl518_prefix=$1

cat << EOF > carton
#!/usr/bin/env bash

perl \
  -Mlocal::lib=$perl518_prefix/lib/carton \
  $perl518_prefix/lib/carton/bin/carton "\$@"
EOF
