from kboard import KBoard, KbKey
from pynput import keyboard
from settings import *
import curses
import os


class KeyLog(object):
	"""
	Records button presses for buttons in question
	"""
	blackKeyDict = {1 : 's'
				, 3 : 'd'
				, 6 : 'g'
				, 8 : 'h'
				, 10 : 'j'}
	whiteKeyDict = {0 : 'z'
				, 2 : 'x'
				, 4 : 'c'
				, 5 : 'v'
				, 7 : 'b'
				, 9 : 'n'
				, 11 : 'm'}

	blackKeyDict_Rev = dict((v, k) for k, v in blackKeyDict.items())
	whiteKeyDict_Rev = dict((v, k) for k, v in whiteKeyDict.items())

	keyboardKeysDict_Rev = blackKeyDict_Rev
	keyboardKeysDict_Rev.update(whiteKeyDict_Rev)

	keyboardKeys = list(blackKeyDict.values()) + list(whiteKeyDict.values())

	activeKeys = {key : False for key in keyboardKeys}

	def on_press(self, key):
		try:
			if key.char in KeyLog.keyboardKeys:
				KeyLog.activeKeys[key.char] = True
				KBoard.keyList[KeyLog.keyboardKeysDict_Rev[key.char]].sound.play()
		except:
			pass
		finally:
			if key == keyboard.Key.esc:
				curses.flushinp()
				curses.endwin()
				os._exit(0)

	def on_release(self, key):
		try:
			if key.char in KeyLog.keyboardKeys:
				KeyLog.activeKeys[key.char] = False
				KBoard.keyList[KeyLog.keyboardKeysDict_Rev[key.char]].sound.stop()
		except:
			pass