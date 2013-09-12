prefix=$1

cat << EOF > rock.yml
env:
  PATH: "$prefix/bin:\${PATH}"
EOF
