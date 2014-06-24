#!/usr/bin/python3

import random, math
import cairo as C
from Layout import ReadOnlyLayoutWrapper
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

class ImageRenderer(AbstractRenderer):
	def __init__(self, width, gutter):
		self.width = width
		self.gutter = gutter

	def render(self, layoutWrapper, filename="out.png"):
		lines = layoutWrapper.get()
		blockSz = self.width / layoutWrapper.getLineWidth()
		height = ((layoutWrapper.getLineCount() - 1)*self.gutter
					+ layoutWrapper.getLineCount()*layoutWrapper.getLineHeight()) * blockSz

		surf = C.ImageSurface(C.FORMAT_ARGB32, self.width, math.floor(height))
		ctx = C.Context(surf)
		#ctx.set_source_rgb(1, 1, 1)
		#ctx.rectangle(0, 0, self.width, height)
		#ctx.fill()
		ctx.set_source_rgb(0, 0, 0)

		_y = 0
		for ln in lines:
			for r in range(0, layoutWrapper.getLineHeight()):
				_x = 0
				for col in ln:
					if col[r]:
						ctx.rectangle(round(_x), round(_y), round(blockSz), round(blockSz))
						ctx.fill()
					_x += blockSz
				_y += blockSz  # Advance one row down.
			_y += blockSz * self.gutter  # The gutter

		surf.write_to_png(filename)


class DistributionGeneratorRenderer(AbstractRenderer):
	def __init__(self, bufCount):
		super(SplitRenderer).__init__()
		if bufCount <= 0:
			raise Exception("Must have at least one dimension in the distribution!")
		self.bufCount = bufCount
		self.distrib = lambda v, c: c if v else 0

	def render(self, layoutWrapper):
		lines = layoutWrapper.get()
		#outBufs is now [lines][columns][cells][buffer_number]
		return ReadOnlyLayoutWrapper(layoutWrapper,
				[[[self.generateDist(lines[ln][col][r], ln, col, r)
					 for r in range(len(lines[ln][col]))] for col in range(len(lines[ln]))] for ln in range(len(lines))])

	def setDistrib(self, func):
		self.distrib = func

	def generateDist(self, val, ln, col, r):
		numTrue = self.distrib(val, self.bufCount, ln, col, r)
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

	def setDistribExtended(self, func):
		self.distGen.setDistrib(func)



class NoiseRenderer(AbstractRenderer):
	def __init__(self, noiseProbability=lambda v: 0 if v else 0.1):
		self.nP = noiseProbability

	def render(self, layoutWrapper):
		lines = layoutWrapper.get()
		return ReadOnlyLayoutWrapper(layoutWrapper,
				[[[ (random.random() < self.nP(r))
					 for r in col] for col in ln] for ln in lines])

class CompositeRenderer(AbstractRenderer):
	def render(self, layoutWrapperA, layoutWrapperB, compositeFunc):
		linesA = layoutWrapperA.get()
		linesB = layoutWrapperB.get()
		return ReadOnlyLayoutWrapper(layoutWrapperA,
				[[[ compositeFunc(linesA[lnI][colI][rI], linesB[lnI][colI][rI])
					 for rI in range(len(linesA[lnI][colI]))]
					 	for colI in range(len(linesA[lnI]))]
					 		for lnI in range(len(linesA))])
