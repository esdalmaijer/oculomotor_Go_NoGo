import pickle
import random

from constants import *
from pygaze.display import Display
from pygaze.screen import Screen
from pygaze.sound import Sound
from pygaze.keyboard import Keyboard
from pygaze.eyetracker import EyeTracker
import pygaze.libtime as timer
from pygaze._misc.misc import pos2psychopos

import numpy


# # # # #
# INITIALISE

# visuals
disp = Display()

# sound
sound = {}
for key in ['go', 'nogo']:
	if SOUNDS[SOUNDVERSION][key] == None:
		sound[key] = None
	elif SOUNDS[SOUNDVERSION][key] == 'noise':
		sound[key] = Sound(osc='whitenoise', length=250)
	else:
		sound[key] = Sound(soundfile=SNDFILES[SOUNDS[SOUNDVERSION][key]])

# input
tracker = EyeTracker(disp)
kb = Keyboard(keylist=['escape'], timeout=1)

# Screens
scr = Screen()
stimscr = {'go':Screen(), 'nogo':Screen()}
stimindex = {'go':None, 'nogo':None}
pointindex = {'go':None, 'nogo':None}
crosshairindex = {'go':[], 'nogo':[]}
for key in stimscr.keys():
	# Target
	stimindex[key] = len(stimscr[key].screen)
	stimscr[key].draw_image(IMGFILES[STIM[key]], pos=DISPCENTRE)
	# Point total
	pointindex[key] = len(stimscr[key].screen)
	stimscr[key].draw_text(text='0', pos=(DISPSIZE[0]-200,200), fontsize=FONTSIZE)
	# Crosshair
	crosshairindex[key] = range(len(stimscr[key].screen), len(stimscr[key].screen) + 3)
	stimscr[key].draw_fixation(fixtype='cross', pos=DISPCENTRE, pw=3, diameter=40)
	stimscr[key].draw_circle(pos=DISPCENTRE, r=10, pw=3, fill=False)


# # # # #
# RUN GAME

# total score
total = 0
x = random.randint(100, DISPSIZE[0]-100)
y = random.randint(100, DISPSIZE[1]-100)

# start the tracker
tracker.start_recording()

# run until a key is pressed
stop = False
gamestart = None
while not stop:

	# randomly select target properties
	nx = x; ny = y
	while abs(x-nx) < MINDIFF and abs(y-ny) < MINDIFF:
		nx = random.randint(100, DISPSIZE[0]-100)
		ny = random.randint(100, DISPSIZE[1]-100)
	x = nx
	y = ny
	rand = random.random()
	if rand < GORATE:
		tartype = 'go'
	else:
		tartype = 'nogo'
	
	# update target position
	stimscr[tartype].screen[stimindex[tartype]].setPos(pos2psychopos((x,y)))
	disp.fill(stimscr[tartype])
	
	# get starting timestamp
	t0 = disp.show()
	tracker.log("TARGET_ONSET: t=%d, tartype=%s, x=%d, y=%d" % (t0, tartype, x, y))
	tartime = None
	runinteraction = True
	if gamestart == None:
		gamestart = t0 + 0

	# run until timeout or a target hit	
	tarhit = False
	while runinteraction:
		
		# get sample
		gazepos = tracker.sample()
		
		# draw target
		if not tarhit:
			stimscr[tartype].screen[stimindex[tartype]].opacity = 1
		else:
			stimscr[tartype].screen[stimindex[tartype]].opacity = 0

		# update the point total
		stimscr[tartype].screen[pointindex[tartype]].text = str(total)
		
		# update the crosshair
		stimscr[tartype].screen[crosshairindex[tartype][0]].setPos(pos2psychopos(gazepos))
		stimscr[tartype].screen[crosshairindex[tartype][1]].setPos(pos2psychopos(gazepos))
		stimscr[tartype].screen[crosshairindex[tartype][2]].setPos(pos2psychopos(gazepos))
		
		# update display
		disp.fill(stimscr[tartype])
		t1 = disp.show()
		
		# check whether the target is hit
		if not tarhit and ((gazepos[0]-x)**2 + (gazepos[1]-y)**2)**0.5 < TARSIZE/1.5:
			# Add points
			total += POINTS[tartype]
			# save the timestamp
			tartime = timer.get_time()
			# log to the tracker
			tracker.log("TARGET_FIXATED: t=%d, total=%d" % (tartime, total))
			# if the target is hit, play the appropriate sound
			tarhit = True
			if sound[tartype] != None:
				sound[tartype].play()

		# check timing
		if tartime == None:
			if t1 - t0 >= STIMTIME:
				runinteraction = False
		elif t1 - tartime >= ISI:
			runinteraction = False
		
		# check if a key was pressed
		key, keytime = kb.get_key(timeout=1, flush=False)
		if key:
			stop = True
			break
		
		# Check if a timeout occurred
		if t1 - gamestart > TASKTIME:
			stop = True
			break


# # # # #
# CLOSE

# close connection to the tracker
tracker.stop_recording()
tracker.close()

# show earnings
scr.clear()
scr.draw_text(text="You scored %d points!" % total, fontsize=FONTSIZE)
disp.fill(scr)
disp.show()

# wait for a keypress
kb.get_key(keylist=None, timeout=None, flush=True)

# High score
if HIGHSCORE is not None:
	# Load the pickle (if available).
	if os.path.isfile(HIGHSCORE):
		with open(HIGHSCORE, 'rb') as pfile:
			highscores = pickle.load(pfile)
	else:
		highscores = {}
	# Store the player's high score.
	highscores[PLAYER] = total
	# Save the high score
	with open(HIGHSCORE, 'wb') as pfile:
		pickle.dump(highscores, pfile)
	# Sort the scores.
	names = numpy.array(highscores.keys())
	scores = numpy.array(highscores.values())
	indices = numpy.argsort(scores)
	indices = indices[-1::-1]
	names = names[indices]
	scores = scores[indices]
	# Show the scores.
	scr.clear()
	scr.draw_text(text="HIGHSCORES", pos=(DISPCENTRE[0], 100), fontsize=FONTSIZE)
	for i in range(min(8, len(names))):
		if names[i] == PLAYER:
			col = (0,255,0)
		else:
			col = FGC
		scr.draw_text(text="%s: %s" % (names[i], scores[i]), fontsize=FONTSIZE, colour=col, pos=(DISPCENTRE[0], 200+i*100))
	disp.fill(scr)
	disp.show()
	kb.get_key(keylist=None, timeout=None, flush=True)

# close display
disp.close()
