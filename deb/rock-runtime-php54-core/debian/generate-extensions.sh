#!/bin/sh

php54_libdir=$1

for path in `find $php54_libdir/php/extensions -name '*.so' -type f` ; do
  file=`basename $path | sed 's/\.so//'`
  echo "Create extension file: $file.ini"
  echo "extension = $file.so" > "$php54_libdir/php.d/$file.ini"
done
