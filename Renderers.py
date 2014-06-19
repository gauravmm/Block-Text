#!/usr/bin/python3

import random
from AbstractFont import ReadOnlyLayoutWrapper
random.seed()


class AbstractRenderer(object):
	def render(self, layoutWrapper):
		raise Exception("Abstract")


class ShellRenderer(AbstractRenderer):
	def __init__(self):
		self.glyphTransform = lambda g: "#" if g else " "

	def render(self, layoutWrapper):
		lines = layoutWrapper.get()
		for ln in lines:
			for r in range(0, layoutWrapper.getLineHeight()):
				print("".join(self.glyphTransform(col[r]) for col in ln))
			print()
			print("".join(self.glyphTransform(c) for c in
				  [True, False] * (layoutWrapper.getLineWidth() // 2)))
			print()

	def setGlyphTransformation(self, transform):
		self.glyphTransform = transform



class DistributionGeneratorRenderer(AbstractRenderer):
	def __init__(self, bufCount):
		super(SplitRenderer).__init__()
		if bufCount <= 0:
			raise Exception("Must have at least one dimension in the distribution!")
		self.bufCount = bufCount
		self.distrib = lambda v, c: c if v else 0

	def render(self, layoutWrapper):
		lines = layoutWrapper.get()
		# Transpose outBufs is now [lines][columns][cells][buffer_number]
		return ReadOnlyLayoutWrapper(layoutWrapper,
				[[[self.generateDist(r)
					 for r in col] for col in ln] for ln in lines])

	def setDistrib(self, func):
		self.distrib = func

	def generateDist(self, val):
		numTrue = self.distrib(val, self.bufCount)
		rv = [True] * numTrue + [False] * (self.bufCount - numTrue)
		random.shuffle(rv)
		return rv


class SplitRenderer(AbstractRenderer):
	def __init__(self, bufCount):
		super(SplitRenderer).__init__()
		self.distGen = DistributionGeneratorRenderer(bufCount)
		self.bufCount = bufCount
		
	def render(self, layoutWrapper):
		dist = self.distGen.render(layoutWrapper)
		outBufs = dist.get()
		# Transpose outBufs from [lines][columns][cells][buffer_number]
		#  to [buffer_number][lines][columns][cells]:
		return [ReadOnlyLayoutWrapper(layoutWrapper,
				[[[r[bidx] for r in col]
				  for col in ln]
				 for ln in outBufs])
				for bidx in range(self.bufCount)]

	def setDistrib(self, func):
		self.distGen.setDistrib(func)

class ScatterRenderer(AbstractRenderer):
	def __init__(self, scatterSize):
		super(ScatterRenderer).__init__()
		self.distGen = DistributionGeneratorRenderer(scatterSize ** 2)
		self.scatterSize = scatterSize
		
	def render(self, layoutWrapper):
		dist = self.distGen.render(layoutWrapper)
		outBufs = dist.get()
		# outBufs is [lines][columns][cells][buffer_number]
		sS = self.scatterSize
		#  Transpose outBufs to [lines][columns][scattered_cells][scattered_cols]
		outBufs = [[[r[bidx * sS : (bidx + 1) * sS]
						for r in col for bidx in range(sS)]
							for col in ln]
								for ln in outBufs]

		# Transpose outBufs to [lines][scattered_cols][scattered_cells]
		outBufs = [[[r[bidx] for r in col]
						 for col in ln for bidx in range(sS)]
								for ln in outBufs]

		return ReadOnlyLayoutWrapper(layoutWrapper, outBufs, sS)

	def setDistrib(self, func):
		self.distGen.setDistrib(func)