# Python Bindings for Raylib

This uses CFFI API static bindings rather than ctypes.  Hopefully this will be faster, the static type knowledge from the C
headers will result in fewer bugs, and using the original headers will make it easier to maintain.

Currently the goal is make usage as similar to the original C as CFFI will allow.  There are a few differences
you can see in the examples.  Making a 'Pythonic' library would be an additional layer on top which hasn't been
done yet.

See test_static.py and examples/*.py for how to use.

# Installing

MacOS: Python 3.7: we distribute a statically linked Raylib library, so in theory the only thing you need to do is install
us from Pypi.

    pip3 install raylib

Linux: Python 3.6: we dont distribute Raylib, so you must have Raylib 2.5dev already installed on your system.  Currently we are building from the github version, specifically https://github.com/raysan5/raylib/commit/f325978b26ea934095f74ac628e6578ebbc2b7a0 although I guess any 2.5 build should work. First follow the instructions here: https://github.com/raysan5/raylib/wiki/Working-on-GNU-Linux Then do:

    pip3 install raylib

If you're using a different version of Python, or using Windows, or maybe a Linux/Mac with incompatible libraries
you will have to build.  The specific version we built against is https://github.com/raysan5/raylib/commit/f325978b26ea934095f74ac628e6578ebbc2b7a0 but we should soon try to synchronize with a proper released version of Raylib.

    cd raylib
    python3 build_linux.py
    python3 build_mac.py

# Platforms tested

 * MacOS 10.12.6 - Python 3.7
 * Ubuntu 18.04 LTS - Python 3.6

# HELP WANTED

 * converting more examples from C to python
 * testing and building on more platforms
 
### Dynamic bindings

I have attempted to do CFFI ABI dynamic bindings too in order to avoid the need to compile a C extension module,
but they don't work properly.  They fail in the same place the ctypes binding fails, accessing
materials of a model, because Python can't dynamically tell the difference between a pointer and an array. There's probably
  some way to specify this (e.g. in raylib_modified.h) but it's difficult to be sure we fixed them all because the errors
 are often completely silent.
 
 See test_dynamic.py for the non-working example.