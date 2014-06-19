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
		self.buffer += instr

	def appendLine(self, instr=""):
		self.appendString(instr)
		self.appendLine()

	def clear(self):
		self.buffer = ""

	def getLineHeight(self):
		return self.font.getMaxCharHeight()

	def getLineWidth(self):
		return self.lineWidth

	def getLineCount(self):
		raise Exception("We don't know that yet.")

	def getFont(self):
		return self.font

	def get(self):
		currLineBuffer = []
		currWordBuffer = []
		outputLines = []

		for ch in self.buffer:
			chrBuffer = self.font.getChar(ch)

			if ch != " ":
				currWordBuffer.extend(chrBuffer)
				currWordBuffer.extend(self.font.getCharSpace() * self.charSpacing)

			if ch == " " or not self.breakOnWord:
				# Check to see if the word buffer + the line is larger than the max line size:
				if len(currLineBuffer) + len(currWordBuffer) > self.lineWidth:
					# Break to new line before this word:
					outputLines.append(
						currLineBuffer
						# Add right-padding:
						+ ([[False] * self.getLineHeight()] * (self.getLineWidth() - len(currLineBuffer)))
					)
					currLineBuffer = currWordBuffer
					currWordBuffer = []
				else:
					# Append this word and a trailing space to this line:
					currLineBuffer.extend(currWordBuffer)
					currWordBuffer = []

				# If there is space on this line, then add a space:
				if ch == " ":
					if len(currLineBuffer) + self.font.getCharWidth(" ") \
						+ (len(self.font.getCharSpace()) * self.charSpacing) < self.lineWidth:
						currLineBuffer.extend(self.font.getChar(" "))
						currLineBuffer.extend(self.font.getCharSpace() * self.charSpacing)

		# Flush whatever buffer is remaining:
		if len(currWordBuffer) > 0:
			currLineBuffer.extend(currWordBuffer)
		if len(currLineBuffer) > 0:
			outputLines.append(currLineBuffer)

		return outputLines


class ReadOnlyLayoutWrapper(LayoutWrapper):
	def __init__(self, layoutWrapper, _outputBuffer=None, _scaleFactor=1):
		self.parent = layoutWrapper
		self.scaleFactor = _scaleFactor
		if _outputBuffer is None:
			self.outputBuffer = layoutWrapper.get()
		else:
			self.outputBuffer = _outputBuffer

	def setLineWidth(self, lW):
		raise Exception("Read-only")

	def setCharSpacing(self, cS):
		raise Exception("Read-only")

	def setBreakOnWord(self, bOW):
		raise Exception("Read-only")

	def appendString(self, instr):
		raise Exception("Read-only")

	def appendLine(self, instr=""):
		raise Exception("Read-only")

	def clear(self):
		raise Exception("Read-only")

	def getLineHeight(self):
		return self.parent.getLineHeight() * self.scaleFactor

	def getLineWidth(self):
		return self.parent.getLineWidth() * self.scaleFactor

	def getLineCount(self):
		return len(self.outputBuffer)

	def getFont(self):
		return self.parent.getFont()

	def get(self):
		return self.outputBuffer
