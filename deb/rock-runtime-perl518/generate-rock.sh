prefix=$1

cat << EOF > rock.yml
env:
  PATH: "$prefix/bin:\${PATH}"
  PERL_ARCHNAME: "`dpkg-architecture -qDEB_BUILD_GNU_TYPE`-thread-multi"
EOF
