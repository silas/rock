require 'formula'

class RockCli < Formula
  homepage 'http://www.rockstack.org/'
  url 'https://pypi.python.org/packages/source/r/rock/rock-0.19.0.tar.gz'
  sha1 '4c5e1cdd7c109a4913386c5319dbe6fdf78c766c'

  depends_on :python
  depends_on 'libyaml'

  resource 'virtualenv' do
    url 'https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.11.6.tar.gz'
    sha1 'd3f8e94bf825cc999924e276c8f1c63b8eeb0715'
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
