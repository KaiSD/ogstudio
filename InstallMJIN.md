**INSTALL**

Michael Kapelko (kornerr AT GoogleMail)

_20110809_


# Dependencies' versions #

Latest MJIN was built against the following versions of dependencies:

| **Dependency** | **Version** | **Newer version works** |
|:---------------|:------------|:------------------------|
| OIS | 1.2.0 | No |
| OGRE | 69c877112b1e | No |
| CEGUI | ce3f1bd08b58 | No |
| OpenAL Soft | 1.4.272 | Yes |
| ALURE | 1.1 | Yes |
| CMake Linux | 2.8.5 | Yes |
| CMake Windows | 2.8.3 | No |

# 1. Linux build environment setup (Debian 5.0.8 32/64-bit DVD1 install) #

## Install additional packages ##

Note: linux-headers is only necessary to compile VirtualBox additions, only after
installing additions do shared folders start to function.

Add the following to sources.list right after the DVD entry:

```
deb http://ftp.de.debian.org/debian lenny main
```

Install necessary packages by running:

```
aptitude install \
    automake \
    chrpath \
    freeglut3-dev \
    g++ \
    libexpat1-dev \
    libfreeimage-dev \
    libfreetype6-dev \
    libgl1-mesa-dev \
    linux-headers-`uname -r` \
    libopenal-dev \
    libpcre3-dev \
    libtool \
    libvorbis-dev \
    libxaw7-dev \
    libxrandr-dev \
    mercurial \
    make
```

## Download necessary files ##

Create a new directory **~/src**. Put MJIN sources into there, go to **~/src/mjin/ext/linux** and run:

```
./download ~/src
```

It will download all files necessary to build MJIN into **~/src**.

## Build all ##

While in the same directory (**ext/linux**), run

```
./install
```

It will build and install all necessary files, including MJIN, within **~/build**.

# 2. Windows build environment setup (XP 32-bit install) #

## CMake ##

Install [CMake-2.8.3-win32-x86.exe](http://www.cmake.org/files/v2.8/cmake-2.8.3-win32-x86.exe)

At the **Install Options** screen select

  * Add CMake to the system PATH for all users
  * Create CMake Desktop Icon

## libsndfile ##

Install [libsndfile-1.0.25-w32-setup.exe](http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.25-w32-setup.exe) to default path.

## Add C:/MinGW/bin to %PATH% ##

You must do it before launching **install** script later.

## Cygwin ##

Install [Cygwin](http://cygwin.com/setup.exe) without selecting additional
packages, but selecting at least 2 mirrors from which to download packages later.

After that, install additional packages by running the following command:

```
setup.exe -P bz2,gz,mercurial,patch,subversion,vim,wget,unzip
```

It will run the same sequence of dialogs. Just keep on pressing "Next",
and it will install everything as needed.

Cygwin is used as a UNIX shell, and MinGW as a compiler.

## Download necessary files ##

Create a new directory **C:/src**. Put MJIN sources into there, go to **C:/src/mjin/ext/cygwin** and run the script from within Cygwin shell:

```
./download C:/src
```

It will download all files necessary to build MJIN into **C:/src**.

## Build all ##

While in the same directory (**ext/cygwin**), run

```
./install
```

It will build and install all necessary files, including MJIN, within **C:/build**.

# 3. Addition packages for Linux distributions #

## Fedora 14 ##

openal-soft freeimage

## openSUSE 11.4 ##

openal-soft libpcreposix0

FreeImage:

  * 32-bit: http://download.opensuse.org/repositories/games/openSUSE_11.4/i586/libfreeimage3-3.10.0-2.1.i586.rpm
  * 64-bit: http://download.opensuse.org/repositories/games/openSUSE_11.4/x86_64/libfreeimage3-3.10.0-2.1.x86_64.rpm

## Mandriva 2010.02 ##

openal (libfreeimage3 or lib64freeimage3)

## Arch 2010.05 ##

openal freeimage libvorbis xdg-utils glut

## Slackware 13.37 ##

openal freeimage
