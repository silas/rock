#!/usr/bin/env bash

php55_libdir=$1

for path in $( find "${php55_libdir}/php/extensions" -name '*.so' -type f ); do
  file=$( basename $path )
  ext='extension'
  if [[ ${file} == 'opcache.so' ]]; then
    ext="zend_${ext}"
  fi
  echo "${ext} = ${file}" > "${php55_libdir}/php.d/${file%.*}.ini"
done
