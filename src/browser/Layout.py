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

		self.line = []
		self.font_cache = {}

		for token in tokens: 
			self.token(token)
		self.flush()

	def token(self, token):
		if isinstance(token, Text):
			words = token.text.split() if len(token.text.split()) > 0 else token.text
			for word in words:
				self.word(word)
		elif token.tag == "i":
			self.style = "italic"
		elif token.tag == "/i":
			self.style = "roman"
		elif token.tag == "b":
			self.weight = "bold"
		elif token.tag == "/b":
			self.weight = "normal"
		elif token.tag == "small":
			self.size -= 2
		elif token.tag == "/small":
			self.size += 2
		elif token.tag == "big":
			self.size += 4
		elif token.tag == "/big":
			self.size -= 4
		elif token.tag == "br":
			self.flush()
		elif token.tag == "/p":
			self.flush()
			self.cursor_y += VSTEP
		elif "h1" in token.tag:
			self.center()
			#self.size += 8
		elif token.tag == "/h1":
			self.flush()
		elif token.tag == "/div":
			self.flush()

	def word(self, word):
		font = self.get_font(self.size, self.weight, self.style)
		self.cursor_x += HSTEP
		w = font.measure(word)

		if self.cursor_x + w > self.width - HSTEP:
			self.flush()

		if word == "\n":
			self.cursor_x = HSTEP
			self.cursor_y += NEW_LINE

		self.line.append((self.cursor_x, word, font))
		self.cursor_x += w + font.measure(" ")

	def get_font(self, size, weight, slant):
		key = (size, weight, slant)
		if key not in self.font_cache:
			font = tkinter.font.Font(
				size=size,
				weight=weight,
				slant=slant,
			)
			label = tkinter.Label(font=font)
			self.font_cache[key] = (font, label)

		return self.font_cache[key][0]

	def flush(self):
		if not self.line: return
		max_ascent = max([font.metrics("ascent") for x, word, font in self.line])
		max_descent = max([font.metrics("descent") for x, word, font in self.line])
		baseline = self.cursor_y + 1.25*max_ascent

		for x, word, font in self.line:
			y = baseline - font.metrics("ascent")
			self.display_list.append((x, y, word, font))

		self.cursor_y = baseline + 1.25*max_descent
		self.cursor_x = HSTEP
		self.line = []

	def center(self):
		if not self.line: return
		line_length = sum([font.measure(word) for x, word, font in self.line])
		center = self.width / 2
		line_start = center - (line_length / 2) - 2*HSTEP

		for x, word, font in self.line:
			print(x, word)
			self.display_list.append((x + line_start, self.cursor_y, word, font))

		self.cursor_x = HSTEP
		self.line = []