require 'formula'

class RockCli < Formula
  homepage 'http://www.rockstack.org/'
  url 'https://pypi.python.org/packages/source/r/rock/rock-0.18.1.tar.gz'
  sha1 '643940afc92cc2a90323dfd09482bd82d2ee296e'

  depends_on :python
  depends_on 'libyaml'

  resource 'virtualenv' do
    url 'https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.11.tar.gz'
    sha1 '1f61baf4963a4bbea116049f6970962d6add641f'
  end

  def install
    resource('virtualenv').stage { |r|
      python do
          system 'python', 'virtualenv.py', 'venv'
          system ". venv/bin/activate ; pip install '#{cached_download}'"
          system 'python', 'virtualenv.py', 'venv', '--relocatable'
          prefix.install 'venv'
      end
    }

    mount_path = var + 'rock'
    opt_path = mount_path + 'opt'

    opt_path.mkpath

    (bin + 'rock').write <<-EOS.undent
      #!/usr/bin/env bash
      export ROCK_MOUNT_PATH='#{mount_path}'
      exec #{prefix}/venv/bin/rock "$@"
    EOS
  end
end
