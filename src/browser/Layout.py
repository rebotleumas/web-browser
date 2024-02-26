from Text import Text
from Tag import Tag

import tkinter
import tkinter.font

HSTEP, VSTEP = 13, 18
NEW_LINE = 20


class Layout:
	def __init__(self, tokens):
		self.width, self.height = 800, 600
		self.display_list = []
		self.cursor_x, self.cursor_y = HSTEP, VSTEP
		self.weight = "normal"
		self.style = "roman"
		self.size = 16

		for token in tokens: 
			self.token(token)

	def token(self, token):
		if isinstance(token, Text):
			words = token.text.split() if len(token.text.split()) > 0 else token.text
			for word in words:
				self.word(word)
		elif token.tag == "i":
			style = "italic"
		elif token.tag == "/i":
			style = "roman"
		elif token.tag == "b":
			weight = "bold"
		elif token.tag == "/b":
			weight = "normal"

	def word(self, word):
		font = tkinter.font.Font(
			size=self.size,
			weight=self.weight,
			slant=self.style,
		)

		self.cursor_x += HSTEP
		if word == "\n":
			self.cursor_x = HSTEP
			self.cursor_y += NEW_LINE

		w = font.measure(word)
		if self.cursor_x + w > self.width - HSTEP:
				self.cursor_y += font.metrics("linespace") * 1.25
				self.cursor_x = HSTEP
		self.display_list.append((self.cursor_x, self.cursor_y, word, font))
		self.cursor_x += w + font.measure(" ")