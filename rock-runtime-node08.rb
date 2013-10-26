require 'formula'

class RockRuntimeNode08 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.8.26/node-v0.8.26.tar.gz'
  sha1 '2ec960bcc8cd38da271f83c1b2007c12da5153b3'

  keg_only 'rock'

  def patches
    DATA
  end

  def install
    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'

    src_yml = prefix + 'rock.yml'
    src_yml.write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS

    dst_yml = var + 'rock/opt/rock/runtime/node08'
    dst_yml.mkpath
    dst_yml += 'rock.yml'
    dst_yml.unlink if dst_yml.exist?

    File.symlink(src_yml, dst_yml)
  end
end

__END__
--- ./deps/v8/src/spaces.h.orig	2013-10-03 15:05:55.000000000 -0700
+++ ./deps/v8/src/spaces.h	2013-10-03 15:06:35.000000000 -0700
@@ -321,7 +321,8 @@
   Space* owner() const {
     if ((reinterpret_cast<intptr_t>(owner_) & kFailureTagMask) ==
         kFailureTag) {
-      return reinterpret_cast<Space*>(owner_ - kFailureTag);
+      return reinterpret_cast<Space*>(reinterpret_cast<intptr_t>(owner_) -
+                                      kFailureTag);
     } else {
       return NULL;
     }
