#!/usr/bin/python3

class AbstractRenderer(object):
	def __init__(self):
		self.glyphTransform = lambda g: "X" if g else " "

	def setGlyphTransformation(self, transform):
		self.glyphTransform = transform
	
	def render(self, layoutWrapper):
		raise Exception("Abstract")

class ShellRenderer(AbstractRenderer):
	def render(self, layoutWrapper):
		lines = layoutWrapper.get()
		for ln in lines:
			for r in range(0, layoutWrapper.getLineHeight()):
				print("".join(self.glyphTransform(col[r]) for col in ln))
			print()
