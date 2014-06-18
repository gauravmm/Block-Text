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

# Currently not used:
class FontWrapper(object):
	def __init__(self, absFont):
		self.font = absFont

	def getStringWidth(self, instr):
		return sum(self.font.getCharWidth(ch) for ch in instr)

	def getStringHeight(self, instr):
		return max(self.font.getCharHeight(ch) for ch in instr)

	def getString(self, instr):
		return [col for ch in instr for col in self.font.getChar(ch)]

class LayoutWrapper(object):
	def __init__(self, absFW):
		self.font = absFW
		self.lineWidth = 80
		self.charSpacing = 1
		self.buffer = ""
		self.breakOnWord = True

	def setLineWidth(self, lW):
		self.lineWidth = lW

	def setCharSpacing(self, cS):
		self.charSpacing = cS

	def setBreakOnWord(self, bOW):
		self.breakOnWord = bOW

	def appendString(self, instr):
		self.buffer += instr;

	def appendLine(self, instr = ""):
		self.appendString(instr)
		self.appendLine()

	def clear(self):
		self.buffer = ""

	def getLineHeight(self):
		return self.font.getMaxCharHeight()

	def get(self):
		tmpBuffer = []
		outputLines = []
		currLineWidth = 0
		if not self.breakOnWord
		for ch in self.buffer:
			chrBuffer = self.font.getChar(ch)
			
			# If we are eligible to break lines here see if we need to break them:
			if ch == " " or not self.breakOnWord:
				if currLineWidth + len(chrBuffer) > self.lineWidth:
					# Break before this character:
					outputLines.append(tmpBuffer)
					tmpBuffer = []
					currLineWidth = 0

			# Append this character to the end of the line
			currLineWidth += len(chrBuffer)
			tmpBuffer.extend(chrBuffer)
			tmpBuffer.extend(self.font.getCharSpace() * self.charSpacing)

		# Flush whatever buffer is remaining:
		if len(tmpBuffer) > 0:
			outputLines.append(tmpBuffer)

		return outputLines

