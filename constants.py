import os

# Experiment parameters
STIM = {'go':'dog', 'nogo':'turd'}
STIMTIME = 2000 # ms
ISI = 300 # ms
TASKTIME = 60000 # ms
GORATE = 0.75
TARSIZE = 200 # pixels
POINTS = {'go':5,'nogo':-5} # credits
MINDIFF = 200 # pixels
SOUNDS = [ \
	{'go':'bark', 'nogo':'fart'}, \
	{'go':'kaching', 'nogo':'noise'}, \
	{'go':None, 'nogo':None} \
	]
SOUNDVERSION = None
while SOUNDVERSION not in range(len(SOUNDS)):
	SOUNDVERSION = input("What sounds? (0=bark, 1=kaching, 2=None) ")

# Folders
DIR = os.path.dirname(os.path.abspath(__file__))
RESDIR = os.path.join(DIR, 'resources')
DATADIR = os.path.join(DIR, 'data')
if not os.path.isdir(RESDIR):
	raise Exception("ERROR: Resources directory not found at '%s'")
if not os.path.isdir(DATADIR):
	os.mkdir(DATADIR)

# Files
PLAYER = raw_input("Who is playing? ")
if PLAYER:
	HIGHSCORE = os.path.join(DATADIR, 'highscores.pickle')
else:
	HIGHSCORE = None
LOGFILENAME = "demo_%s" % (str(len(os.listdir(DATADIR))).zfill(3))
LOGFILE = os.path.join(DATADIR, LOGFILENAME)
SNDFILES = { \
	'kaching':os.path.join(RESDIR, 'kaching.wav'), \
	'meow':os.path.join(RESDIR, 'cat_meow.wav'), \
	'bark':os.path.join(RESDIR, 'dog_bark.wav'), \
	'fart':os.path.join(RESDIR, 'fart_01.wav') \
	}
IMGFILES = { \
	'dog':os.path.join(RESDIR, 'dog_emoticon.png'), \
	'hamster':os.path.join(RESDIR, 'hamster_emoticon.png'), \
	'turd':os.path.join(RESDIR, 'turd_emoticon.png'), \
	'cat_neutral':os.path.join(RESDIR, 'cat_neutral_emoticon.png'), \
	'cat_happy':os.path.join(RESDIR, 'cat_happy_emoticon.png'), \
	}

# Display
DISPSIZE = (1920, 1080)
DISPCENTRE = (int(DISPSIZE[0]/2), int(DISPSIZE[1]/2))
SCREENSIZE = (55.0,28.4)
SCREENDIST = 67.0
DISPTYPE = 'psychopy'
FONTSIZE = 50
FGC = (255, 255, 255)
BGC = (128, 128, 128)

# Eye tracking
TRACKERTYPE = 'eyetribe'
DUMMYMODE = ''
while DUMMYMODE not in ['y', 'n']:
	DUMMYMODE = raw_input("Use DUMMY mode? (y/n) ")
DUMMYMODE = DUMMYMODE == 'y'
