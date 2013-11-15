require 'formula'

def postgres_installed?
  `which pg_config`.length > 0
end

class RockRuntimePhp55 < Formula
  homepage 'http://www.php.net/'
  url 'http://us.php.net/distributions/php-5.5.6.tar.bz2'
  sha1 '02a30f72b1d6876a41b48548d4f95bf2b4761147'

  env :std
  keg_only 'rock'

  skip_clean ['bin', 'sbin']

  depends_on 'berkeley-db'
  depends_on 'curl'
  depends_on 'enchant'
  depends_on 'freetype'
  depends_on 'gettext'
  depends_on 'gmp'
  depends_on 'homebrew/dupes/zlib'
  depends_on 'icu4c'
  depends_on 'imap-uw'
  depends_on 'jpeg'
  depends_on 'libmemcached'
  depends_on 'libpng'
  depends_on 'libxml2' unless MacOS.version >= :mountain_lion
  depends_on 'mcrypt'
  depends_on 'mysql'
  depends_on 'pcre'
  depends_on 'postgresql' unless postgres_installed?
  depends_on 't1lib'
  depends_on 'unixodbc'

  # extensions
  depends_on 'autoconf' => :build

  resource 'composer' do
    url 'http://getcomposer.org/download/1.0.0-alpha7/composer.phar'
    sha1 '4f8513bea6daa4f70007e4344944c2fe458650ac'
  end

  resource 'memcached' do
    url 'http://pecl.php.net/get/memcached-2.1.0.tgz'
    sha1 '16fac6bfae8ec7e2367fda588b74df88c6f11a8e'
  end

  def install_composer
    resource('composer').stage { |r|
      system 'cp', r.cached_download, "#{bin}/composer.phar"
    }
    system 'chmod', '755', "#{bin}/composer.phar"
    system 'ln', '-s', "#{bin}/composer.phar", "#{bin}/composer"
  end

  def install_memcached
    resource('memcached').stage { |r|
      system "curl -s 'https://gist.github.com/silas/7131202/raw' | patch -p1"
      Dir.chdir "memcached-#{r.version}"
      system "#{bin}/phpize"
      system './configure',
        '--enable-memcached-json',
        "--prefix=#{prefix}",
        "--with-php-config=#{bin}/php-config",
        "--with-libmemcached-dir=#{Formula.factory('libmemcached').prefix}"
      system 'make'
      system 'make', 'install'
      system "echo 'extension = memcached.so' > #{lib}/php.d/memcached.ini"
    }
  end

  def install
    args = [
      "--prefix=#{prefix}",
      "--sbindir=#{prefix}/bin",
      '--with-libdir=lib',
      '--disable-debug',
      '--disable-static',
      "--with-config-file-scan-dir=#{lib}/php.d",
      '--with-pic',
      '--with-bz2',
      "--with-freetype-dir=#{Formula.factory('freetype').prefix}",
      "--with-png-dir=#{Formula.factory('libpng').prefix}",
      '--enable-gd-native-ttf',
      "--with-t1lib=#{Formula.factory('t1lib').prefix}",
      "--with-gettext=#{Formula.factory('gettext').prefix}",
      '--with-gmp',
      '--with-iconv',
      "--with-jpeg-dir=#{Formula.factory('jpeg').prefix}",
      '--with-openssl=/usr',
      "--with-pcre-regex=#{Formula.factory('pcre').prefix}",
      "--with-zlib=#{Formula.factory('zlib').prefix}",
      '--enable-exif',
      '--enable-ftp',
      '--enable-sockets',
      '--enable-ucd-snmp-hack',
      '--enable-shmop',
      '--enable-calendar',
      '--enable-xml',
      '--with-system-tzdata',
      '--with-mhash',
      '--enable-pcntl',
      '--with-imap=shared',
      '--with-imap-ssl',
      '--enable-mbstring=shared',
      '--enable-mbregex',
      '--with-gd=shared',
      '--enable-bcmath=shared',
      '--enable-dba=shared',
      "--with-db4=#{Formula.factory('berkeley-db').prefix}",
      '--with-xmlrpc=shared',
      '--with-ldap=shared',
      '--with-ldap-sasl',
      '--with-mysql=shared,mysqlnd',
      '--with-mysqli=shared,mysqlnd',
      '--with-mysql-sock=/tmp/mysql.sock',
      "--with-pdo-mysql=#{Formula.factory('mysql').bin}/mysql_config",
      '--with-pdo-sqlite=/usr',
      '--enable-dom=shared',
      '--with-pgsql=shared',
      '--enable-wddx=shared',
      '--with-snmp=shared,/usr',
      '--enable-soap=shared',
      '--with-xsl=shared,/usr',
      '--enable-xmlreader=shared',
      '--enable-xmlwriter=shared',
      "--with-curl=shared,#{Formula.factory('curl').prefix}",
      '--with-sqlite3=shared,/usr',
      '--enable-json=shared',
      '--with-libzip',
      '--with-libedit',
      '--with-pspell=shared',
      '--enable-phar=shared',
      '--with-mcrypt=shared,/usr',
      '--with-kerberos=/usr',
      '--with-tidy=shared,/usr',
      '--enable-sysvmsg=shared',
      '--enable-sysvshm=shared',
      '--enable-sysvsem=shared',
      '--enable-posix=shared',
      '--enable-fileinfo=shared',
      '--enable-intl',
      "--with-icu-dir=#{Formula.factory('icu4c').prefix}",
      "--with-enchant=shared,#{Formula.factory('enchant').prefix}",
      '--enable-pdo',
      '--disable-cgi',
      '--enable-fpm',
      '--with-pear',
    ]

    unless MacOS.version >= :mountain_lion
      args << "--with-libxml-dir=#{Formula.factory('libxml2').prefix}"
    end

    if postgres_installed?
      if File.directory?(Formula.factory('postgresql').opt_prefix.to_s)
        args << "--with-pgsql=#{Formula.factory('postgresql').opt_prefix}"
        args << "--with-pdo-pgsql=#{Formula.factory('postgresql').opt_prefix}"
      else
        args << "--with-pgsql=#{`pg_config --includedir`}"
        args << "--with-pdo-pgsql=#{`which pg_config`}"
      end
    end

    system './configure', *args
    system 'make'
    ENV.deparallelize
    system 'make', 'install'

    system "
      echo 'date.timezone = UTC' > '#{lib}/php.ini'
      mkdir -p #{lib}/php.d
      for path in $( find '#{lib}/php/extensions' -name '*.so' -type f ); do
        file=$( basename $path )
        ext=extension
        if [[ ${file} == opcache.so ]]; then
          ext=zend_${ext}
        fi
        echo \"${ext} = ${file}\" > \"#{lib}/php.d/${file%.*}.ini\"
      done
    "

    ENV['PATH'] = "#{bin}:#{ENV['PATH']}"

    install_composer
    install_memcached

    (prefix + 'rock.yml').write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS

    runtime = var + 'rock/opt/rock/runtime'
    runtime.mkpath
    runtime += 'php55'
    system 'rm', '-fr', runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
