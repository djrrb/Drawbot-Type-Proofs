"""
Get words that fit a specific line length
run in drawbot (www.drawbot.com)
"""

import os
import random
import string
from vanilla.dialogs import getFolder
from fontTools.ttLib import TTFont

# specify the word dictionary
wordPath = '/usr/share/dict/words' # use the mac’s native dictionary
#wordPath = 'italian.txt' # use a custom file

# Do we want to be promted to provide a folder of fonts
# or to specify the fonts in a list
useFolder = False

if useFolder:
    pathToFonts = getFolder('folder with fonts')[0]
    # find all the font files in a provided folder
    paths = []
    for root, dirs, files in os.walk(pathToFonts):
        for filename in files:
            basePath, ext = os.path.splitext(filename)
            if ext in ['.otf', '.ttf']:
                paths.append(os.path.join(root, filename))
else:
    # this is a list of fonts
    # can be a font name for an installed font
    # or a path to a OTF or TTF font
    paths = [
        'Verdana'
        ]

# Query options
# how many to display
quota = 20
# point size
theSize = 150
# width to fill
targetWidth = 480
# tolerance threshold (+/-)
threshold = 2

# make all caps
makeUppercase = False
# capitalize first letter
makeCapitalized = True

#use only characters in font
useFontContainsCharacters = True

openTypeFeaturesDict = {
    'ss01': False,
    }
    
fontVariationsDict = {
    #'wght': 700,
    }

# margin (for display only, does not influence results)
margin = 20


# get the words
with open(wordPath,encoding="utf-8") as wordsFile:
    words = wordsFile.readlines()
# shuffle order so it is not alphabetical
random.shuffle(words)

for fontName in paths:
    newPage(targetWidth+(margin*2), theSize*quota+(margin*2))
    matches = []
    # this section deals with tonos in greek, kinda hacky
    grekReplace = {
        u'\u0386': u'\u0391', 
        u'\u0389': u'\u0397', 
        u'\u0388': u'\u0395', 
        u'\u038a': u'\u0399', 
        u'\u03ad': u'\u03b5', 
        u'\u03ac': u'\u03b1', 
        u'\u03af': u'\u03b9', 
        u'\u03ae': u'\u03b7', 
        u'\u03cd': u'\u03c5', 
        u'\u038f': u'\u03a9', 
        u'\u038c': u'\u039f', 
        u'\u03cc': u'\u03bf', 
        u'\u038e': u'\u03a5', 
        u'\u03ce': u'\u03c9'
    }

    # loop through words
    for word in words:
        # do formatting
        word = word.strip()
        if makeCapitalized:
            word = word.title()
        if makeUppercase:
            word = word.upper()
        # this deals with tonos in greek, kinda hacky
        oldWord = word
        word = ''
        for i in oldWord:
            if i in grekReplace:
                word += grekReplace[i]
            else:
                word += i
                
        if useFontContainsCharacters:
            font(fontName)
            if not fontContainsCharacters(word):
                continue
                
        # get a formatted string and match it
        fs = FormattedString(word, font=fontName, fontSize=theSize, lineHeight=theSize, tracking=0, openTypeFeatures=openTypeFeaturesDict, fontVariations=fontVariationsDict)
        tw, th = textSize(fs)
        if abs(targetWidth - tw) < threshold:
            matches.append(word)
        if len(matches) == quota:
            break
    # sort the results (alphabetically)
    matches.sort()
    # set the results 

    # set the results in drawbot
    fs = FormattedString('\n'.join(matches),
    font=fontName,
    lineHeight=theSize,
    fontSize=theSize,
    openTypeFeatures=openTypeFeaturesDict,
    fontVariations=fontVariationsDict
    )
    textBox(fs, (margin,margin,width(), height()-margin*2), align="center")