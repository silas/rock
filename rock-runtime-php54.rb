require 'formula'

class RockRuntimePhp54 < Formula
  homepage 'http://www.php.net/'
  url 'http://us.php.net/distributions/php-5.4.7.tar.bz2'
  sha1 'e634fbbb63818438636bf83a5f6ea887d4569943'

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
  depends_on 'libpng'
  depends_on 'libxml2' unless MacOS.version >= :mountain_lion
  depends_on 'mcrypt'
  depends_on 'mysql'
  depends_on 'pcre'
  depends_on 'unixodbc'

  def install_composer
    phar_version = '1.0.0'
    phar_pre = 'alpha5'

    system 'curl', '-Lo', "#{bin}/composer.phar", "http://getcomposer.org/download/#{phar_version}-#{phar_pre}/composer.phar"
    system 'chmod', '755', "#{bin}/composer.phar"
  end

  def install
    rock = Pathname.new('/opt/rock')

    unless rock.directory? && rock.writable?
      onoe "#{rock} must be a directory and writable"
      exit 1
    end

    args = [
      "--prefix=#{prefix}",
      "--sbindir=#{prefix}/bin",
      '--with-libdir=lib',
      '--disable-debug',
      '--disable-static',
      '--with-pic',
      '--with-bz2',
      "--with-freetype-dir=#{Formula.factory('freetype').prefix}",
      "--with-png-dir=#{Formula.factory('libpng').prefix}",
      '--with-xpm-dir=/usr',
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
      '--without-pe',
    ]

    unless MacOS.version >= :mountain_lion
      args << "--with-libxml-dir=#{Formula.factory('libxml2').prefix}"
    end

    system './configure', *args
    system 'make'
    ENV.deparallelize
    system 'make', 'install'

    (lib + 'php.ini').write <<-EOS.undent
      extension = json.so
      extension = phar.so
    EOS

    ENV['PATH'] = "#{bin}:#{ENV['PATH']}"

    install_composer

    runtime = rock + 'runtime/php54'
    runtime.mkpath
    runtime += 'rock.yml'
    runtime.unlink if runtime.exist?
    runtime.write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS
  end
end
