from kboard import KBoard, KbKey
from pysinewave import SineWave
from pynput import keyboard
from curses import wrapper
from keylog import KeyLog
from settings import *
import curses
import os
import time
import math

os.environ["TERM"] = "xterm-256color"
os.environ["TERMINFO"] = "/usr/share/terminfo"


# ---------- NOT CURRENTLY IN USE ----------

# populates pitchClasses with frequencies from octaves 0 to 7
# AFreq = 440
# exponent = -4
# octaves = 7
# pitchClasses = {name : [] for name in keyNames}

# for octave in range(octaves):
# 	freqA = AFreq*math.pow(2,exponent)
# 	for num in range(12):
# 		index = (9+num) % len(keyNames)
# 		pitchClasses[keyNames[index]].append(freqA*(2**(num/12)))
# 	exponent += 1

# ---------- NOT CURRENTLY IN USE ----------
		

def main(stdscr):
	
	stdscr.nodelay(True)

	kLog = KeyLog()
	listener = keyboard.Listener(
				on_press=kLog.on_press,
				on_release=kLog.on_release)
	listener.start()
	stdscr.clear()

	kb = KBoard()

	width = stdscr.getmaxyx()[1]
	height = stdscr.getmaxyx()[0]

	# set keyboard's bounds
	kb.boardXBounds = [int(width*0.2), int(width*0.8)]
	kb.boardYBounds = [int(height*0.2), int(height*0.8)]

	kb.keyWidth = (kb.boardXBounds[1]-kb.boardXBounds[0])//kb.numKeys

	whiteKeyWidth = (kb.boardXBounds[1]-kb.boardXBounds[0])//7
	whiteKeyHeight = kb.boardYBounds[1]-kb.boardYBounds[0]
	blackKeyWidth = int((0.66)*whiteKeyWidth)
	blackKeyHeight = int((0.5)*(whiteKeyHeight))

	# set each key's bounds
	keyStart = kb.boardXBounds[0]
	lastBlackKey = None
	lastWhiteKey = None

	for key in kb.keyList:
		if key.name in whiteKeyNames:
			if lastWhiteKey == None:
				key.xBounds = [keyStart, keyStart + whiteKeyWidth]
			else:
				key.xBounds = [lastWhiteKey.xBounds[1], lastWhiteKey.xBounds[1] + whiteKeyWidth]

			key.yBounds = [kb.boardYBounds[0]+blackKeyHeight, kb.boardYBounds[1]]
			lastWhiteKey = key

		elif key.name in blackKeyNames:
			if lastWhiteKey == None:
				key.xBounds = [keyStart, keyStart + blackKeyWidth]
			else:
				blackKeyStart = int((2/3)*(lastWhiteKey.xBounds[1] - lastWhiteKey.xBounds[0])) + lastWhiteKey.xBounds[0]
				key.xBounds = [blackKeyStart, blackKeyStart + blackKeyWidth]

			key.yBounds = [kb.boardYBounds[0], kb.boardYBounds[0]+blackKeyHeight]
			lastBlackKey = key


	while(True):
		stdscr.clear()

		for num, key in enumerate(kb.keyList):
			key.drawKey(stdscr)

		for key, value in KeyLog.activeKeys.items():
			keyNum = KeyLog.keyboardKeysDict_Rev[key]
			kb.keyList[keyNum].isPressed = value

		time.sleep(0.05)
		stdscr.refresh()


wrapper(main)