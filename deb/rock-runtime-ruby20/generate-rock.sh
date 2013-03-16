prefix=$1
bundler_version=1.3.4
abi=2.0.0

cat << EOF > rock.yml
env:
  PATH: "$prefix/bin:\${PATH}"
  RUBY_ABI: "$abi"
  RUBYOPT: "-I$prefix/lib/ruby/gems/$abi/gems/bundler-$bundler_version/lib -rbundler/setup"
EOF
