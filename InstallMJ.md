**INSTALL**

Michael Kapelko (kornerr AT GoogleMail)

_20110809_


Latest Mahjong should be built against the latest MJIN.

# Linux Debian 5.0.8 32/64-bit #

Put Mahjong sources into **~/src/mj**, go into
**~/src/mj/ext/linux** and run:

```
./build
```

It will copy Mahjong binary files into $OGS\_MJ\_BIN. You must define it aforehead,
the script will complain if the environment variable is not set.

# Windows XP 32-bit #

Put Mahjong sources into **C:/src/mj**, go into
**C:/src/mj/ext/cygwin** and run:

```
./build
```

It will copy Mahjong binary files into $OGS\_MJ\_BIN. You must define it aforehead,
the script will complain if the environment variable is not set.

# Debug version #

To build debug version of Mahjong, you should run the build scripts as follows:

```
./build debug
```

It will skip binary stripping stage.

# Packages #

**mj/ext/linux** contains the scripts to create packages:

  * **mkDebian**: creates deb packages suitable for Debian 6, Mint 10, Ubuntu 11.04;
  * **mkDebianMusicAddon**: creates deb package of music addon;
  * **mkStandAlone**: creates 7zip compressed archives for both Linux and Windows.

The above scripts require several environment variables to be set.
They will be listed when you run the above scripts.
