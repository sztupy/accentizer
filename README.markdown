Accentizer
==========

Accentizer is a small python script that will use FontForge's engine to add
missing accented characters to fonts. It has some additional logic to create
double acute acents for ő,ű,Ő,Ű, even if a double acute modifier is not present
in the font. 

How it works
------------

Accentizer will use FontForge's accent builder, to create the missing
characters. By default it will only create the glyphs ő,Ő,ű and Ű, ut this list
can be modified by adding your desired unicode codepoints to the `glyphs` list.

Next Accentizer will run FontForge's accent builder for all the fonts that are
mentioned. For double acute characters, it will even do some extra work, if the
"double acute modifier" codepoint is not present in the font.

In the latter case it will first try to create a "double acute modifier" glyph
from a single "acute" glyph. But if the single "acute" glyph is also not
present, it will try to create one from the "é" glyph (é was chosen, as it is
a common character in French language, so support for it in fonts is higher
then for other acute characters, like á or í). If there is no "é" glyph
however, it will silently fail.

Installation
------------

Install FontForge from http://fontforge.sourceforge.net/

Windows+cygwin builds can be found at http://www.geocities.jp/meir000/fontforge/

After installing fontforge you can run the script using fontforge. For example
on Windows you can write:

    fontforge.bat accentizer.py Lato-Black.ttf

See `Usage` for more information.

Example result
--------------

This is a result of running Accentizer on some random fonts from Google Web
Fonts

![](http://github.com/sztupy/accentizer/raw/master/example.png) 


Usage
-----

    accentizer.py [options] {filename}

or

    fontforge accentizer.py [options] {filename}

Options
-------

* `--ffont` generate accented fonts even if they claim to exist in font
* `--faccent` generate double acute from single acute even if there is a double
acute modifier present  
* `--trans=xx` translate double accents closer by xx pixels when double acute
was generated from single acute. Default: 40

Licence
-------

Copyright © 2012 by Zsolt Sz. Sztupák (mail@sztupy.hu)
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

The name of the author may not be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

