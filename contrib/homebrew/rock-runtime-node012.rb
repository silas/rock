require "formula"

class RockRuntimeNode012 < Formula
  homepage "http://nodejs.org/"
  url "http://nodejs.org/dist/v0.12.0/node-v0.12.0.tar.gz"
  sha256 "9700e23af4e9b3643af48cef5f2ad20a1331ff531a12154eef2bfb0bb1682e32"

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
    runtime += "node012"
    system "rm", "-fr", runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
