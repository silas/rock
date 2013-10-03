require 'formula'

class RockRuntimeNode010 < Formula
  homepage 'http://nodejs.org/'
  url 'http://nodejs.org/dist/v0.10.10/node-v0.10.10.tar.gz'
  sha1 'c21643a57b1ec9eca56e6deac22fe075616e0e9c'

  keg_only 'rock'

  def patches
    DATA
  end

  def install
    rock = Pathname.new('/opt/rock')

    unless rock.directory? && rock.writable?
      onoe "#{rock} must be a directory and writable"
      exit 1
    end

    system './configure', "--prefix=#{prefix}"
    system 'make', 'install'

    runtime = rock + 'runtime/node010'
    runtime.mkpath
    runtime += 'rock.yml'
    runtime.unlink if runtime.exist?
    runtime.write <<-EOS.undent
      env:
        PATH: "#{bin}:${PATH}"
    EOS
  end
end

__END__
--- ./deps/v8/src/spaces.h.orig	2013-10-03 15:11:58.000000000 -0700
+++ ./deps/v8/src/spaces.h	2013-10-03 15:12:14.000000000 -0700
@@ -320,7 +320,8 @@
   Space* owner() const {
     if ((reinterpret_cast<intptr_t>(owner_) & kFailureTagMask) ==
         kFailureTag) {
-      return reinterpret_cast<Space*>(owner_ - kFailureTag);
+      return reinterpret_cast<Space*>(reinterpret_cast<intptr_t>(owner_) -
+                                      kFailureTag);
     } else {
       return NULL;
     }
