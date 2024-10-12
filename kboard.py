from pysinewave import SineWave
from pynput import keyboard
from settings import *


class KBoard(object):
	"""
	Defines a keyboard object containing KbKey Objects
	"""
	boardXBounds = [0,0]
	boardYBounds = [0,0]

	keyWidth = 0
	keyLength = 0

	keyList = []

	def __init__(self, numKeys=None):
		self.numKeys = numKeys or 12
		KBoard.keyList = [KbKey(name=keyNames[i%len(keyNames)]) for i in range(self.numKeys)]


class KbKey(KBoard):
	"""
	Defines a single key on a keyboard (KBoard) object
	"""
	def __init__(self, name=None, button=None):
		self.name = name or "C" 
		self.button = button
		self.xBounds = [0,0]
		self.yBounds = [0,0]
		self.isPressed = False
		self.sound = SineWave(pitch = keyNames.index(name))

	def drawKey(self, stdscr):
		"""
		Draws keys as lines with empty space if unpressed
		and lines containing a repeated symbol if pressed
		"""
		if self.isPressed:
			for y in range(self.yBounds[0], self.yBounds[1]):
				for x in range(self.xBounds[0], self.xBounds[1]):
					try:
						if x == self.xBounds[0] or x == self.xBounds[1]:
							stdscr.addstr(y, x, "|")
						else:
							stdscr.addstr(y, x, ";")
					except:
						pass
		else:
			for y in range(self.yBounds[0], self.yBounds[1]):
				for x in self.xBounds:
					try:
						stdscr.addstr(y, x, "|")
					except:
						pass