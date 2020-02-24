import unicodedata
import datetime
import os

########################
# SETUP
## Let’s set some variables.

# the exported font we are using, OTF or TTF
# this can be a path like /path/to/MyFont.otf
# you can drag a font onto the text window to get the path
# OR this can also be the exact name of an installed font
myFontPath = 'Verdana'

myFallbackFont = 'AdobeBlank.otf'

# the character set we are proofing
charset = """ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvxyz
0123456789
.,:; \'" ?! & () [] $#
"""

sampleText = 'Alpha Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliet Kilo Lima Mike November Oscar Papa Quebec Romeo Sierra Tango Uniform Victor Whiskey Xylophone Yankee Zulu. Jackdaws love my big sphinx of quartz. Victors flank gypsy who mixed up on job quiz. Wolves exit quickly as fanged zoo chimps jabber. Five jumbo oxen graze quietly with packs of dogs. Grumpy wizards make toxic brew for the evil queen and jack. Lazy movers quit hard packing of jewelry boxes. Ban foul, toxic smogs which quickly jeopardize lives. Hark! Toxic jungle water vipers quietly drop on zebras for meals! New farm hand, picking just six quinces, proves strong but lazy. Back in my quaint garden, jaunty zinnias vie with flaunting phlox. Waltz, nymph, for quick jigs vex Bud. Crazy Fredericka bought many very exquisite opal jewels. Jolly housewives made inexpensive meals using quick-frozen vegetables. Sixty zippers were quickly picked from the woven jute bag. Call 1 (800) 435 8293 Jaded zombies acted quaintly but kept driving their oxen forward. Six big juicy steaks sizzled in a pan as five workmen left the quarry. Will Major Douglas be expected to take this true-false quiz very soon? A mad boxer shot a quick, gloved jab to the jaw of his dizzy opponent. Jimmy and Zack, the police explained, were last seen diving into a field of buttered quahogs. Monique, the buxom coed, likes to fight for Pez with the junior varsity team. The jukebox music puzzled a gentle visitor from a quaint valley town. Just work for improved basic techniques to maximize your typing skills. When we go back to Juarez, Mexico, do we fly over picturesque Arizona? Murky haze enveloped a city as jarring quakes broke forty-six windows. Nancy Bizal exchanged vows with Robert J. Kumpf at Quincy Temple. The quick brown fox jumps over the lazy dog.'

# font sizes
charsetFontSize = 48
spacingFontSize = 36
largeTextFontSize = 36

# our page dimensions and margin
inch = 72 
pageDimensions = 11*inch, 8.5*inch
margin = inch/2

# column information (for spacing proof)
columnWidth = (pageDimensions[0]-margin*3)/2

# define a function for drawing a simple footer
def drawFooter(title):
    with savedState():
        # get date and font name
        today = datetime.date.today()
        fontName = os.path.split(myFontPath)[1]
        
        # assemble footer text
        footerText = '{date} | {fontName} | {title}'.format(date=today, fontName=fontName, title=title)
        
        # and display formatted string
        footer = FormattedString(footerText,
            font='Courier',
            fontSize=9,
            lineHeight=9
        )
        folio = FormattedString(str(pageCount()),
            font='Courier',
            fontSize=9,
            lineHeight=9,
            align="right"
        )
        textBox(footer, (margin, margin-6, width()-margin*2, 9))
        textBox(folio, (margin, margin-6, width()-margin*2, 9))


#####################
# DRAW
## Let’s build this proof.

#####################
# charset proof
newPage(*pageDimensions)
charsetString = FormattedString(charset,
    font=myFontPath,
    fallbackFont=myFallbackFont,
    fontSize=charsetFontSize,
    align="center")
textBox(charsetString, (margin, margin, width()-margin*2, height()-margin*2))

drawFooter('Character set proof')

#####################
# spacing proof
newPage(*pageDimensions)
drawFooter('Spacing proof')

# create empty formatted string that we will fill with spacing strings
fs = FormattedString('HH HOHO OO\n',
    font=myFontPath,
    fallbackFont=myFallbackFont,
    fontSize=spacingFontSize,
)

# loop through all of the characters in our character set
for char in charset:
    # determine control characters for each character
    # ignoring linebreaks and space characters
    if char not in ['\n', ' ']:
        # by default, use H and O
        control1 = 'H'
        control2 = 'O'
        # if the char is lowercase, use n and o
        if unicodedata.category(char) == 'Ll':
            control1 = 'n'
            control2 = 'o' 
        # if the char is a number
        elif unicodedata.category(char) == 'Nd':
            control1 = '0'
            control2 = '1'
        # set up our spacing string in HHXHOHOXOO format
        # using the control characters
        spacingString = '{control1}{control1}{char}{control1}{control2}{control1}{control2}{char}{control2}{control2}\n'.format(control1=control1, control2=control2, char=char)
        fs.append(spacingString)
# now, use a while loop to draw each column
# until we run out of text
xoffset = 0
while fs:
    if xoffset+columnWidth > width():
        newPage(*pageDimensions)
        drawFooter('Spacing proof')
        xoffset = 0
    fs = textBox(fs, (margin+xoffset, margin, width()-margin*2, height()-margin*2))   
    xoffset += columnWidth + margin
 
#####################   
# text proof
# for text fonts, proofs can be much more involved than this
# but this is a start

newPage(*pageDimensions)
drawFooter('Text proof')

fs = FormattedString(sampleText,
    font=myFontPath,
    fallbackFont=myFallbackFont,
    fontSize=largeTextFontSize,
)
textBox(fs, (margin, margin, width()*1.25, height()-margin*2))   

#######################
# Okay, we’re done.

# if you want to save to your desktop automatically
# otherwise use File > Save PDF
#saveImage('~/desktop/proof.pdf')