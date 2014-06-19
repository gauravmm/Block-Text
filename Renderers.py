#!/usr/bin/python3

import random
from AbstractFont import ReadOnlyLayoutWrapper
random.seed()


class AbstractRenderer(object):
    def __init__(self):
        self.glyphTransform = lambda g: "M" if g else " "

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
            print("".join(self.glyphTransform(c) for c in
                  [True, False] * (layoutWrapper.getLineWidth() // 2)))
            print()


class SplitRenderer(AbstractRenderer):
    def __init__(self, bufCount, density):
        super().__init__()
        if bufCount <= 0:
            raise Exception("Must have at least one output buffer!")
        self.bufCount = bufCount
        if density <= 0 or density > 1:
            raise Exception("Density must be in range (0..1]")
        self.median = density * (bufCount - 1) + 1
        self.numTrueInDist = lambda b, m, v: \
            round(random.triangular(1, b, m)) if v else 0

    def setGlyphTransformation(self, transform):
        raise Exception("Cannot set transformation on a non-terminal renderer!")

    def render(self, layoutWrapper):
        lines = layoutWrapper.get()
        outBufs = [[[self.generateDist(self.bufCount, self.median, r)
                     for r in col] for col in ln] for ln in lines]
        # Transpose outBufs from [lines][columns][cells][buffer_number]
        #  to [buffer_number][lines][columns][cells]:
        return [ReadOnlyLayoutWrapper(layoutWrapper,
                [[[r[bidx] for r in col]
                  for col in ln]
                 for ln in outBufs])
                for bidx in range(self.bufCount)]

    def setNumTrueInDist(self, func):
        self.numTrueInDist = func

    def generateDist(self, bC, median, val):
        if not val:
            return [False] * bC

        numTrue = self.numTrueInDist(bC, median, val)
        rv = [True] * numTrue + [False] * (bC - numTrue)
        random.shuffle(rv)
        return rv
