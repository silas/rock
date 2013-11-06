require 'formula'

class RockCli < Formula
  homepage 'http://www.rockstack.org/'
  url 'https://pypi.python.org/packages/source/r/rock/rock-0.17.0.tar.gz'
  sha1 '51c941d740d71586d31ba307936f0122f6803d52'

  depends_on :python
  depends_on 'libyaml'

  resource 'virtualenv' do
    url 'https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz'
    sha1 '0c441553f97a1ed68bb2032c9ab65e6c3bc38e24'
  end

  def install
    resource('virtualenv').stage { |r|
      python do
          system 'python', 'virtualenv.py', 'venv'
          system ". venv/bin/activate ; pip install '#{cached_download}'"
          system 'python', 'virtualenv.py', 'venv', '--relocatable'
          system 'mv', 'venv', prefix + 'venv'
      end
    }

    mount_path = var + 'rock'
    opt_path = mount_path + 'opt'
    opt_rock = opt_path + 'rock'

    opt_path.mkpath

    (bin + 'rock').write <<-EOS.undent
      #!/usr/bin/env bash
      export ROCK_MOUNT_PATH='#{mount_path}'
      exec #{prefix}/venv/bin/rock "$@"
    EOS
  end
end
