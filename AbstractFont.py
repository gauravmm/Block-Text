#!/usr/bin/python3
# From: https:#github.com/gauravmm/HT1632-for-Arduino/blob/master/Arduino/HT1632/font_5x4.h

# Characters are defined as boolean arrays, as columns of bools (i.e. left-to-right,
#  each element is a list of booleans GLYPH_HEIGHT long, top-to-bottom.


class AbstractFont(object):
	def getCharWidth(self, ch):
		raise Exception("Abstract")

	def getCharHeight(self, ch):
		raise Exception("Abstract")

	def getMaxCharHeight(self):
		raise Exception("Abstract")

	def getChar(self, ch):
		raise Exception("Abstract")

	def getCharSpace(self):
		raise Exception("Abstract")


class FontWrapper(object):  # Currently not used
	def __init__(self, absFont):
		self.font = absFont

	def getStringWidth(self, instr):
		return sum(self.font.getCharWidth(ch) for ch in instr)

	def getStringHeight(self, instr):
		return max(self.font.getCharHeight(ch) for ch in instr)

	def getString(self, instr):
		return [col for ch in instr for col in self.font.getChar(ch)]


class AbstractGlyphMapper(object):
	def __init__(self):
		return

	def transform(self, inp):
		raise Exception("Abstract")

	def mapAcross(self, glyph):
		return [[self.transform(rel) for rel in col] for col in glyph]


class BasicValueMapper(AbstractGlyphMapper):
	def __init__(self, valIfTrue, valIfFalse):
		self.tv = valIfTrue
		self.fv = valIfFalse

	def transform(self, inp):
		return self.tv if inp else self.fv
