
class LayoutGenerator(object):
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

	def get(self):
		currLineBuffer = []
		currWordBuffer = []
		outputLines = []

		for ch in self.buffer:
			if ch not in [" ", "\n"]:
				chrBuffer = self.font.getChar(ch)
				currWordBuffer.extend(chrBuffer)
				currWordBuffer.extend(self.font.getCharSpace() * self.charSpacing)

			if ch == "\n":
				# Append this word to the lineBuffer and then move to the next line
				currLineBuffer.extend(currWordBuffer)
				outputLines.append(self.padRight(currLineBuffer))
				currLineBuffer = []
				currWordBuffer = []
				#currLineBuffer.extend(self.font.getChar("\\"))
				#currLineBuffer.extend(self.font.getChar("n"))

			if ch == " " or not self.breakOnWord:
				# Check to see if the word buffer + the line is larger than the max line size:
				if len(currLineBuffer) + len(currWordBuffer) > self.lineWidth:
					# Break to new line before this word:
					outputLines.append(self.padRight(currLineBuffer))
					currLineBuffer = currWordBuffer
					currWordBuffer = []
				else:
					# Append this word to this line:
					currLineBuffer.extend(currWordBuffer)
					currWordBuffer = []

				# If there is space on this line, then add a traiing space:
				if ch == " ":
					if len(currLineBuffer) + self.font.getCharWidth(" ") \
						+ (len(self.font.getCharSpace()) * self.charSpacing) < self.lineWidth:
						currLineBuffer.extend(self.font.getChar(" "))
						currLineBuffer.extend(self.font.getCharSpace() * self.charSpacing)

		# Flush whatever buffer is remaining:
		if len(currWordBuffer) > 0:
			currLineBuffer.extend(currWordBuffer)
		if len(currLineBuffer) > 0:
			outputLines.append(self.padRight(currLineBuffer))

		return BlockImage(self.font, self.lineWidth, outputLines)

	def padRight(self, lineBuffer):
			return lineBuffer + ([[False] * self.font.getMaxCharHeight()] * (self.lineWidth - len(lineBuffer)))



class AbstractBlockImage(object):
	def getLineHeight(self):
		raise Exception("Abstract")

	def getLineWidth(self):
		raise Exception("Abstract")

	def getLineCount(self):
		raise Exception("Abstract")

	def getFont(self):
		raise Exception("Abstract")

	def get(self):
		raise Exception("Abstract")


class BlockImage(AbstractBlockImage):
	def __init__(self, font, lineWidth, buffer):
		self.lineHeight = font.getMaxCharHeight()
		self.lineWidth = lineWidth
		self.buffer = buffer

	def getLineHeight(self):
		return self.lineHeight

	def getLineWidth(self):
		return len(self.buffer[0])

	def getLineCount(self):
		return len(self.buffer)

	def get(self):
		return self.buffer


class ReadOnlyBlockImage(AbstractBlockImage):
	def __init__(self, layoutWrapper, _outputBuffer, _scaleFactor=1):
		self.parent = layoutWrapper
		self.scaleFactor = _scaleFactor
		if _outputBuffer is None:
			raise Exception("OutputBuffer cannot be None!")
		else:
			self.outputBuffer = _outputBuffer

	def getLineHeight(self):
		return self.parent.getLineHeight() * self.scaleFactor

	def getLineWidth(self):
		return self.parent.getLineWidth() * self.scaleFactor

	def getLineCount(self):
		return len(self.outputBuffer)

	def get(self):
		return self.outputBuffer
