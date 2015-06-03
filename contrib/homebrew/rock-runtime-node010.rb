require "formula"

class RockRuntimeNode010 < Formula
  homepage "http://nodejs.org/"
  url "http://nodejs.org/dist/v0.10.36/node-v0.10.36.tar.gz"
  sha256 "b9d7d1d0294bce46686b13a05da6fc5b1e7743b597544aa888e8e64a9f178c81"

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
