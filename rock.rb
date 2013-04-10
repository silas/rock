require 'formula'

class Rock < Formula
  homepage 'http://www.rockstack.org/'
  url 'https://pypi.python.org/packages/source/r/rock/rock-0.15.0.tar.gz'
  sha1 '4b0c436329cbb13d4dd55423f12b094da6a3cc3c'

  env :std

  def install
    system 'easy_install', "setup.py"
  end
end
