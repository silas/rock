require "formula"

class RockRuntimeNode010 < Formula
  homepage "http://nodejs.org/"
  url "http://nodejs.org/dist/v0.10.32/node-v0.10.32.tar.gz"
  sha256 "c2120d0e3d2d191654cb11dbc0a33a7216d53732173317681da9502be0030f10"

  keg_only "rock"

  def install
    system "./configure", "--prefix=#{prefix}"
    system "make", "install"

    (prefix + "rock.yml").write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS

    runtime = var + "rock/opt/rock/runtime"
    runtime.mkpath
    runtime += "node010"
    system "rm", "-fr", runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
