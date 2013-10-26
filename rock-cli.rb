require 'formula'

class RockCli < Formula
  homepage 'http://www.rockstack.org/'
  url 'https://pypi.python.org/packages/source/r/rock/rock-0.15.0.tar.gz'
  sha1 '4b0c436329cbb13d4dd55423f12b094da6a3cc3c'

  depends_on 'libyaml'

  resource 'virtualenv' do
    url 'https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz'
    sha1 '0c441553f97a1ed68bb2032c9ab65e6c3bc38e24'
  end

  def install
    resource('virtualenv').stage { |r|
      system 'python', 'virtualenv.py', 'venv'
      system ". venv/bin/activate ; pip install '#{cached_download}'"
      system 'python', 'virtualenv.py', 'venv', '--relocatable'
      system 'mv', 'venv', prefix + 'venv'
    }

    (bin + 'rock').write <<-EOS.undent
      #!/usr/bin/env bash
      exec #{prefix}/venv/bin/rock "$@"
    EOS
  end
end
