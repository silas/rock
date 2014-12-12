require "formula"

class RockCli < Formula
  homepage "http://www.rockstack.org/"
  url "https://pypi.python.org/packages/source/r/rock/rock-0.20.1.tar.gz"
  sha256 "18f6d441a5794aed2c6c724073bd9f8526cb211ce04ef8284e047d9badc560b6"

  depends_on :python
  depends_on "libyaml"

  resource "PyYAML" do
    url "https://pypi.python.org/packages/source/P/PyYAML/PyYAML-3.11.tar.gz"
    sha256 "c36c938a872e5ff494938b33b14aaa156cb439ec67548fcab3535bb78b0846e8"
  end

  def install
    mount_path = var + 'rock'
    opt_path = mount_path + 'opt'

    opt_path.mkpath

    ENV.prepend_create_path "PYTHONPATH", libexec + "lib/python2.7/site-packages"
    ENV.prepend_create_path "PYTHONPATH", prefix + "lib/python2.7/site-packages"

    install_args = "setup.py", "install", "--prefix=#{libexec}"
    resource("PyYAML").stage { system "python", *install_args }

    system "python", "setup.py", "install", "--prefix=#{libexec}"

    (bin/"rock").write_env_script libexec/"bin/rock", :PYTHONPATH => ENV["PYTHONPATH"], :ROCK_MOUNT_PATH => mount_path
  end
end
