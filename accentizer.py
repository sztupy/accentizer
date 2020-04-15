#!/usr/bin/fontforge
# -*- coding: utf-8 -*-
#
# ACCENTIZER by Zsolt Sz. Sztupák (mail@sztupy.hu)
# Based on a FontForge script tutorial by George Williams
#
# Copyright © 2012 by Zsolt Sz. Sztupák (mail@sztupy.hu)
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# The name of the author may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import fontforge
import os
import re
import psMat

DOUBLE_ACUTE_COMBINING_CODEPOINT = 0x030b
DOUBLE_ACUTE_CODEPOINT = 0x02dd

DOUBLE_PRIME_MODIFIER_CODEPOINT = 0x02ba
DOUBLE_APOSTROPHE_MODIFIER_CODEPOINT = 0x02ee

SINGLE_ACUTE_MODIFIER_CODEPOINT = 0x02ca
SINGLE_ACUTE_COMBINING_CODEPOINT = 0x0301
SINGLE_ACUTE_CODEPOINT = 0x00b4

DOUBLE_ACUTE_PRIORITY = [DOUBLE_ACUTE_COMBINING_CODEPOINT, DOUBLE_ACUTE_CODEPOINT, DOUBLE_PRIME_MODIFIER_CODEPOINT, DOUBLE_APOSTROPHE_MODIFIER_CODEPOINT]
SINGLE_ACUTE_PRIORITY = [SINGLE_ACUTE_COMBINING_CODEPOINT, SINGLE_ACUTE_CODEPOINT, SINGLE_ACUTE_MODIFIER_CODEPOINT]

E_WITH_ACUTE = 0x00e9

DOUBLE_ACUTE_ACCENTS = [ 0x0150,0x0151,0x0170,0x0171 ]

# change these variables if needed
glyphs = DOUBLE_ACUTE_ACCENTS; # this is ő,Ő,ű,Ű; add other accents you wish to auto-generate here
translationFix = 40; # when duplicating the acute accent this is the amount of correction to do. The bigger the number the closer the two accents will be
forceFont = False
forceAccent = False

if len(sys.argv)<=1:
  print("ACCENTIZER")
  print
  print("Usage: ")
  print("  accentizer.py [options] {filename}")
  print("   or")
  print("  fontforge accentizer.py [options] {filename}")
  print
  print("Options:")
  print("  --ffont:    generate accented fonts even if they claim to")
  print("              exist in font")
  print("  --faccent:  generate double acute from single acute even")
  print("              if there is a double acute modifier present")
  print("  --trans=xx: translate double accents closer by xx pixels")
  print("              when double acute was generated from single")
  print("              acute. Default: 40")
  sys.exit();
else:
  while len(sys.argv)!=2:
    arg = sys.argv.pop(1)
    tr = re.match("--trans=([0-9]*)",arg)
    if arg=="--ffont":
      print("Will generate accent for all characters")
      forceFont = True
    elif arg=="--faccent":
      print("Will generate double acute even it is exists")
      forceAccent = True
    elif tr:
      translationFix = int(tr.group(1))
      print("Double acute distance modifier set to " + str(translationFix) + " when generating double acute from single acute")
    else:
      print("Invalid parameter: ") + arg
      sys.exit();

def glyphExists(font, cp):
  return len(list(font.selection.select(cp).byGlyphs))!=0

def createDoubleAcute(font):
  glyph = next((i for i in SINGLE_ACUTE_PRIORITY if glyphExists(font,i)))
  font.selection.select(glyph);
  font.copy();
  font.selection.select(DOUBLE_ACUTE_COMBINING_CODEPOINT)
  font.paste();

  glyph = font.createChar(DOUBLE_ACUTE_COMBINING_CODEPOINT);

  # duplicate the acute
  layer = glyph.foreground
  layer2 = layer.dup()
  # translate this layer left and right
  bb = layer.boundingBox()
  translation = (bb[2]-bb[0]-translationFix) / 2
  layer.transform(psMat.translate(-translation,0));
  layer2.transform(psMat.translate(translation,0));
  # mix the two layers
  layer += layer2;
  # save the modified layer
  glyph.foreground = layer

def copyDoubleAcuteFromPriorityList(font):
  glyph = next((i for i in DOUBLE_ACUTE_PRIORITY if glyphExists(font,i)))
  font.selection.select(glyph);
  font.copy();
  font.selection.select(DOUBLE_ACUTE_COMBINING_CODEPOINT);
  font.paste();

def generateAcute(font):
  # we will try to generate an acute from é.
  # é is chosen, as it's common in French, so it's probably avialable in the font
  glyph = font.createChar(E_WITH_ACUTE);
  layer = fontforge.layer()
  contour = None
  maxpos = -sys.maxsize - 1;
  # we will search for the contour which has the highest point. That's probably the accent

  # search in foreground
  char = glyph.foreground
  for cont in char:
    for point in cont:
      if point.y > maxpos:
        maxpos = point.y
        contour = cont

  # search in references
  for ref in glyph.references:
    name = ref[0]
    mat = ref[1]
    char = font.createChar(fontforge.unicodeFromName(name)).foreground;
    for cont in char:
      cont.transform(mat);
      for point in cont:
        if point.y > maxpos:
          maxpos = point.y
          contour = cont

  # only add this contour
  if not contour:
    print("é character is invalid, accent not generated")
    return

  layer.is_quadratic = contour.is_quadratic
  layer += contour
  # save layer
  glyph = font.createChar(SINGLE_ACUTE_COMBINING_CODEPOINT);
  glyph.foreground = layer

fontFileName = sys.argv[1]
fileName, fileExtension = os.path.splitext(fontFileName)

print("Loading font")

font = fontforge.open(fontFileName)

doubleAcuteAccents = DOUBLE_ACUTE_ACCENTS;

if not forceFont:
  print("Searching for non-existent glyphs")
  glyphs = [i for i in glyphs if not glyphExists(font,i)]

for daa in doubleAcuteAccents:
  if daa in glyphs: # we need to generate at least one doubleacute accent
    # check if " modifiers exists
    if not forceAccent and glyphExists(font, DOUBLE_ACUTE_COMBINING_CODEPOINT):
      print("Double acute modifier exists in font, will use that to create accented characters!")
      # we are done, autobuilding will hopefully work
      break;
    if not forceAccent and next((i for i in DOUBLE_ACUTE_PRIORITY if glyphExists(font,i)), False):
      print("No double acute modifier, but there are alternatives")
      copyDoubleAcuteFromPriorityList(font)
      break;
    if next((i for i in SINGLE_ACUTE_PRIORITY if glyphExists(font,i)), False):
      print("Single acute modifier exists in font, will generate double acute from that")
      # we need to generate double acute from single acute
      createDoubleAcute(font)
      break;
    # no acute. Try to extract one from a letter
    print("No acute accent found, trying to generate one!")
    generateAcute(font)
    createDoubleAcute(font)
    break;

for glyphId in glyphs:
  glyph = font.createChar(glyphId)
  print("Creating glyph for " + glyph.glyphname)
  glyph.build()

font.generate(fileName + "out.ttf")
