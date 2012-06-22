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

# change these variables if needed
glyphs = [0x0150,0x0151,0x0170,0x0171]; # add other accents you wish to auto-generate here
translationFix = 40; # when duplicating the acute accent this is the amount of correction to do. The bigger the number the closer the two accents will be
forceFont = False
forceAccent = False

if len(sys.argv)<=1:
  print "ACCENTIZER"
  print
  print "Usage: "
  print "  accentizer.py [options] {filename}"
  print "   or"
  print "  fontforge accentizer.py [options] {filename}"
  print
  print "Options:"
  print "  --ffont:    generate accented fonts even if they claim to"
  print "              exist in font"
  print "  --faccent:  generate double acute from single acute even"
  print "              if there is a double acute modifier present"  
  print "  --trans=xx: translate double accents closer by xx pixels"
  print "              when double acute was generated from single"
  print "              acute. Default: 40"
  sys.exit();  
else:
  while len(sys.argv)!=2:
    arg = sys.argv.pop(1)
    tr = re.match("--trans=([0-9]*)",arg)
    if arg=="--ffont":
      print "Will generate accent for all characters"
      forceFont = True
    elif arg=="--faccent":
      print "Will generate double acute even it is exists" 
      forceAccent = True
    elif tr:
      translationFix = int(tr.group(1))
      print "Double acute distance modifier set to " + str(translationFix) + " when generating double acute from single acute"
    else:
      print "Invalid parameter: " + arg
      sys.exit();

def glyphExists(font, cp):
  return len(list(font.selection.select(cp).byGlyphs))!=0

def createDoubleAcute(font):
  glyph = None;
  # copy the single acute to the double acute position
  if glyphExists(font,0x00b4):
    font.selection.select(0x00b4);
    font.copy();
    font.selection.select(0x02dd)
    font.paste();
    glyph = font.createChar(0x02dd);  
  elif glyphExists(font,0x02ca):
    font.selection.select(0x02ca);
    font.copy();
    font.selection.select(0x02dd)
    font.paste();
    glyph = font.createChar(0x02dd);
  elif glyphExists(font,0x0301):
    font.selection.select(0x0301);
    font.copy();
    font.selection.select(0x030B);
    font.paste();
    glyph = font.createChar(0x02dd);        
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

def generateAcute(font):
  # we will try to generate an acute from é.
  # é is chosen, as it's common in French, so it's probably avialable in the font
  glyph = font.createChar(0x00e9);
  layer = fontforge.layer()
  contour = None
  maxpos = -sys.maxint - 1;
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
    print "é character is invalid, accent not generated"
    return

  layer.is_quadratic = contour.is_quadratic
  layer += contour
  # save layer
  glyph = font.createChar(0x02ca);
  glyph.foreground = layer

fontFileName = sys.argv[1]
fileName, fileExtension = os.path.splitext(fontFileName)

print "Loading font"

font = fontforge.open(fontFileName)

doubleAcuteAccents = [0x0150,0x0151,0x0170,0x0171];

if not forceFont:
  print "Searching for non-existent glyphs"
  glyphs = [i for i in glyphs if not glyphExists(font,i)]

for daa in doubleAcuteAccents:
  if daa in glyphs: # we need to generate at least one doubleacute accent
    # check if " modifiers exists
    if not forceAccent and (glyphExists(font,0x02dd) or glyphExists(font,0x030B)):
      print "Double acute modifier exists in font, will use that to create accented characters!"
      # we are done, autobuilding will hopefully work
      break;
    if glyphExists(font,0x02ca) or glyphExists(font,0x0301) or glyphExists(font,0x00b4):
      print "Single acute modifier exists in font, will generate double acute from that"
      # we need to generate double acute from single acute
      createDoubleAcute(font)
      break;
    # no acute. Try to extract one from a letter
    print "No acute accent found, trying to generate one!"
    generateAcute(font)
    createDoubleAcute(font)
    break;

for glyphId in glyphs:
  glyph = font.createChar(glyphId)
  print "Creating glyph for " + glyph.glyphname
  glyph.build()

font.generate(fileName + "out.ttf") 
