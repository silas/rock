require "formula"

class RockRuntimeNode08 < Formula
  homepage "http://nodejs.org/"
  url "http://nodejs.org/dist/v0.8.28/node-v0.8.28.tar.gz"
  sha256 "50e9a4282a741c923bd41c3ebb76698edbd7b1324024fe70cedc1e34b782d44f"

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
    runtime += "node08"
    system "rm", "-fr", runtime if runtime.exist?

    File.symlink(prefix, runtime)
  end
end
