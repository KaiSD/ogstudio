# Introduction #

This is how OGS toolset should look like in 2014.

# MJIN2 #

  * Is written in C++ without exposing its dependencies like MJIN1 does.
    1. Removes the burden of dependencies from the end game.
    1. Allows to completely control the interface: no more different styles of code formatting imposed by dependencies.
  * Python interface is provided by SWIG.
    1. Allows to generate interface to Lua, Java, C# and many other languages.
    1. Uses low level binding, e.g., Python.h for Python which means SWIG is only compile time dependency, not runtime one (like Boost.Python).
    1. SWIG2 also has “-builtin” compile flag which gives about 2X speed up compared to the default method (and all other existing Python bindings).
  * Lightweight X11/WinAPI GUI that allows to display Splash, MessageBox with translations [(Issue)](http://code.google.com/p/ogstudio/issues/detail?id=149)
  * Indirect-free code: don't use singletons, pass necessary things explicitly [(Issue)](http://code.google.com/p/ogstudio/issues/detail?id=304)
  * Explicitly forbid unused constructor and copy-constructor [(Issue)](http://code.google.com/p/ogstudio/issues/detail?id=465)
  * Render within Qt [(Issue)](http://code.google.com/p/ogstudio/issues/detail?id=379)
  * Soft shadow mapping [(Issue)](http://code.google.com/p/ogstudio/issues/detail?id=59)
  * Compressed resources [(Issue)](http://code.google.com/p/ogstudio/issues/detail?id=420)
  * Create a simple GUI test to find out if Nouveau on old GeForce is working now [(Issue)](http://code.google.com/p/ogstudio/issues/detail?id=468)
  * Check if OSG has OGRE problems of hidden window [(Issue)](http://code.google.com/p/ogstudio/issues/detail?id=253)

# Game (Mahjong 2.0, Shuan 1.0) #

  * Is written entirely in Python, if possible.
  * May use C++ as a base for critical Python modules. Although, if possible, it should be placed to MJIN2 code base.
  * Should be able to be instantiated from inside the Editor to allow realtime editing.

# Editor #

  * Python + Qt (PyQt4 or PySide).
  * Directly uses MJIN2 through Python interface.
  * Should be able to instantiate Game to allow realtime editing.