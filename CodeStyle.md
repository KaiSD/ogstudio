

# Introduction #

[Original issue](http://code.google.com/p/ogstudio/issues/detail?id=462)

Requirements are based on [Google C++ style guide](http://google-styleguide.googlecode.com/svn/trunk/cppguide.xml). You are advised to read it too.

# Define guards #
Format:
```
<PATH>_<FILE>_H
```
E.g., mjin2/FileSystem.h:
```
#define MJIN2_FILE_SYSTEM_H
```

# Header inclusion order #
  1. MJIN2
  1. <blank line>
  1. The rest

```
#include <mjin2/Application.h>
#include <mjin2/Window.h>

#include <stdexcept>
```

Each group of headers should also be ordered by name, as in the example.

# Visibility scope #
Do not use 'using' keyword anywhere, even in source files. Keeping namespace names simplifies understanding where certain thing comes from. It also helps to grep contents.

# Hungarian notation #
We DO NOT use Hungarian ANYWHERE.

# Work in constructors #
Do not use virtual function calls, because the calls will not get dispatched to the subclass implementations.

# Exceptions #
We use them.

# Use of const #
Class methods that return pointers / references must NOT be declared const just because they don't modify the value. The value can be modified by the caller since it gets pointer / reference. const keyword is used for human here, not compiler.

# Integer types #
We use u8, u16, u32, u64, s8, s16, s32, s64 instead of char, int, short, long long to save on typing and support different platforms (32-bit, 64-bit).

# Preprocessor macros #
We use them for very commonly used constructs to save on typing, like MJIN2\_EXCEPTION, MJIN2\_LOG, MJIN2\_STR.

# 0 and NULL #
We use 0 for integers, pointers and chars.

# sizeof #
We use sizeof(variable) instead of sizeof(struct), because it allows to change variable type later without rewriting the chunk of code where sizeof is used.

# Boost #
We don't use it, because it's big, complex, introduces additional dependencies and compile time increase.
We believe that what Boost can do we can do ourselves, because we rarely need full fledged functionality that Boost offers. Take, e.g., FileSystem class. It's only several bytes in size, but offers us all we need from FileSystem on different platforms.

# C++11 #
Everything supported by GCC 4.6 can be used, but with caution, because headers are processed by SWIG too. So only those C++11 features should be used in headers, that do not conflict with SWIG. Also, MJIN2 strives to be as simple as possible (at least from header perspective) since things like templates can't be done in target languages.

# Autocompletion #
It is considered 'bad', because it propagates your errors.

At work I saw the following example:
```
DEBUG_INFO_FOUR("timePlayChannel",playChannelTime.toString().toStdString(),"mSec",playChannelTime.msec());
DEBUG_INFO_FOUR("timeStertChannel",startChanelTime.toString().toStdString(),"mSec",startChanelTime.msec());
```
As you see, names of variables differ and they are even misspelled.
This wouldn't have happened if one would have typed variables manually each time.

# Naming #
## General naming rules ##

It's best to name correctly, unambiguously and without abbreviation if possible. Though, if file scope is pretty small, we don't mind abbreviations:
```
OGOFilmInfoPage *mFIP; // Ok in a small scope file.
```

## File names ##

Header C++ files have .h extension (not hpp).

Source files one have .cpp (not cxx, not cc).

File names with C++ classes are named in the same way as classes:

```
TileStateMoving.h/TileStateMoving.cpp for TileStateMoving class.
```

We don't use underscores in file names.

Lower case is allowed only in special cases:
```
endian.h // For endian convertions
```

## Type names ##

Classes, structs, typedefs:
```
class TileStateMoving
{
};

struct Item
{
};

typedef std::vector<Item> Items;
```

Enums:
```
enum TILE_STATE
{
    TILE_STATE_MOVING,
    TILE_STATE_HIDING
};
```

Enums should be located in Common.h like file, not nested into a class, if they are used in different files. Although, it's ok to nest Enum inside a private section if it's only used internally inside the class.

Private classes used to hide dependency should be named like ClassName\_p:
```
class RegExp_p
```

## Variable names ##

Local variables and struct ones use camel case.

Class member variables start with 'm' and then camel case.

Global variables start with 'g' and then camel case.
```
int localVariable;
```
```
struct BinFormat
{
    int           formatVersion;
    unsigned char formatMagic;
};
```
```
class TileStateMoving
{
    private:
        int mMemberVariable;
};
```
```
TileStateMoving *gTileStateMoving;
```

## Constant names ##
Uppercase with underscores:
```
const u16 MAX_STRLEN = 1024;
```

## Function names ##

Function names use camel case and should be verbs:
```
void doSomethingSpecial()
```
```
class SomethingSpecial
{
    public:
        void doItNow();
};
```

## Namespace names ##

So far they are lowercase and one word long.

Each namespace is represented by a directory in project structure:
```

namespace mj
{

class Application
{
};

} // namespace mj
```
must be located in mj/Application.h.

## Macros ##

```
#define THIS_IS_A_MACRO(X) std::cout << X << std::endl;
```

# Comments #
## File comments ##
For MJIN2, use the following copyright notice at the top of the .h and .cpp files:
```
/*
This file is part of MJIN2.

MJIN2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MJIN2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with MJIN2.  If not, see <http://www.gnu.org/licenses/>.
*/
```

## Class comments ##

Every class definition should have an accompanying comment that describes what it is for and how it should be used:
```
//! Regular expression matcher.
/*! Example:
 *  \code
 *  RegExp re("\n|\t");
 *  StringList sl;
 *  sl.push_back("A dog\nand cat");
 *  sl.push_back("A bird,\ta mole");
 *  sl.push_back("A man without a cat");
 *  for (StringList::iterator it = sl.begin(); it != sl.end(); ++it)
 *      if (re.match(*it))
 *          std::cout << *it << std::endl;
 *  \endcode
 *  The example will only print the first two lines.
 *  The third one doesn't match the specified regular expression.
 */
class RegExp
{
```

# Formatting #
## Line length ##
Maximum line length is 80 characters, because it simplifies comparison of 2 code snippets placed side by side.

Exception: URL or other data that must be preserved.

## Spaces vs. tabs ##
Only use spaces. Tab = 4 spaces.

## Function declarations and definitions ##
Return type on the same line as function name, parameters on the same line if they fit:
```
void Class::function(int param) throw ()
{
    . . .
}
```
If parameters don't fit, place them across several lines aligned:
```
void Class::method(const &param1,
                   int   param2) throw ()
{
    . . .
}
```
If even the first parameter doesn't fit, start on the next line right away:
```
void Class::method(
    int param1,
    int param2) throw (std::exception)
{
    . . .
}
```

Note:
  * The return type is always on the same line as the function name.
  * The open parenthesis is always on the same line as the function name.
  * There is never a space between the function name and the open parenthesis.
  * There is never a space between the parentheses and the parameters.
  * The open curly brace is always on its own line or at the end of the same line as the last parameter only if the definition is empty.
  * The close curly brace is either on the last line by itself or on the same line as the open curly brace if the definition is empty, in which case curly braces are separated by 1 space.
  * There should be a space between the close parenthesis and the open curly brace.
  * All parameters should be named, with identical names in the declaration and implementation.
  * All parameters should be aligned if placed across several lines.
  * Always specify what function may throw, this allows SWIG to generate correct target language exception handling.

If the function is const, the const keyword should be on the same line as the last parameter.

If some parameters are unused, comment out the variable name in the function definition, not declaration.

## Function calls ##
On one line if it fits; otherwise, wrap arguments at the parenthesis.
```
bool val = something(1.0);
```
If the arguments do not all fit on one line, they should be broken up onto multiple lines and aligned:
```
bool val = something(1.0,
                     255.38);
```
If the function signature is so long that it cannot fit within the maximum line length, you may place all arguments on subsequent lines, aligned:
```
bool val = something(
    1.0,
    255.38,
    "wh");
```

## Conditionals ##
No spaces inside parenthesis. The else keyword belongs on a new line. Space must always be present between if and open parenthesis:
```
if (condition)
{
    . . .
}
else if (. . .)
{
    . . .
}
else
{
    . . .
}
```
No conditional may be written in one line. Even the simplest if statement must span 2 lines:
```
if (true)
    doSomething();
```

## Loops and switch statements ##

Loops should use prefix ++ operator, because otherwise temporary variable is created to hold return value each cycle iteration:
```
for (StringList::iterator it = mList.begin(); it != mList.end(); ++it)
{
    . . .
```
case blocks in switch statements should only have curly braces if it's required by compilator, i.e., to create a variable, and they should be placed like shown below.
switch statements should raise exception in default case if unsupported value is provided.
```
switch (a)
{
    case 1:
        b = a;
        break;
    case 2:
    {
        RegExp re("abc");
        if (re.match("Wow"))
            b = a - 1;
        break;
    }
    default:
        MJIN2_EXCEPTION("Invalid parameter", MJIN2_STR("%u", a));
}
```

## Pointer and reference expressions ##

No spaces around period or arrow. Pointer operators do not have trailing spaces.
```
x = *p;
p = &x;
x = r.y;
x = r->y;
```
When declaring a pointer variable or argument, you should place the asterisk adjacent to the variable, not type:
```
char *c;
const string &str;
```
This is because asterisk belongs to a variable, not type:
```
char* c, d;
```
Here c is a pointer, but d is not! So we forbid such confusion in the first place.

As for returning pointers/references, they should be placed adjacent to the type:
```
const char* str()
```

## Boolean expressions ##
When boolean expression is longer than maximum line length, align variables and operators:
```
if (abc                >  other &&
    somethingDifferent == r     &&
    1                  == 1)
{
    . . .
```
Also, use &&, ||, etc. instead of and, or, etc. keywords.

## Preprocessor directives ##
# is always put at the beginning of the line:
```
if (abc)
{
#ifdef DEBUG
    std::cout << "abc called\n";
#endif
    doSomething();
    . . .
```

## Class format ##
```
class A : public B,
          public C
{
        DISALLOW_COPY_AND_ASSIGN(A);
    public:
        A();
        ~A();

        void doSomething();
        bool isSomething() const;
        void setSomething(const String &value);

    private:
        void doIt();
        
        bool mIsSomething;
};
```
Note:
  * Base classes are aligned.
  * DISALLOW\_COPY\_AND\_ASSIGN is used to forbid copy and assignment constructors.
  * Constructor and destructor are separated from public methods by a blank line.
  * Methods are ordered by name in each section (public, protected, private). The same order must be kept in source files.
  * Each public, protected, private keyword is preceded by a blank line, unless it is the first section.
  * Do not leave a blank line after these keywords.
  * The public section should be first, followed by the protected and finally the private section.
  * Do not put variables and methods into the first default private section following open curly brace. Only use it for macros.
  * If a section has both methods and variables, there's no need to duplicated the section: first, place methods inside the section, then a blank line, then the variables; see the private section in the example above.

## Constructor initializer list ##
Constructor initializer lists can be all on one or several lines:
```
SomeClass::SomeClass(int value) : mValue(a)
{
. . .
```
(Note the space at both sides of ":")
```
OtherClass::OtherClass(int value, const char *string) : mValue(value),
                                                        mString(string)
{
. . .
```
If the list starts with subsequent line,  indent is 4 spaces:
```
Class::Class(int value, const char *string) :
        mValue(value),
        mString(string)
{
. . .
```

Empty constructor body should be placed this way:
```
Class::Class() : mA(1) { }
```

## Namespace formatting ##
The contents of namespaces are not indented.
```
namespace aaa
{
namespace bbb
{

class A
{
    public:
        A();
};

} // namespace bbb
} // namespace aaa
```

# Platform dependent code #

Functions that are platform dependent (#ifdef WIN32, etc) must contain the following Doxygen comment in header file:
```
//! Platform dependent implementation.
```

# AStyle options to ease conformance to the style #
```
--style=allman
--indent-classes
--indent-switches
--indent-col1-comments
--pad-oper
--pad-header
--align-pointer=name
```