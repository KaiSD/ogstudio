import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
                      "packages": ["pyglet"]
                      }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Shuan2d",
        version = "0.6",
        description = "Shuan gameplay prototype",
        options = {"build_exe": build_exe_options},
        executables = [Executable("game.py", base=base)])