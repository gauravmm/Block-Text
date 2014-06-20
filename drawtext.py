#!/usr/bin/python3
from AbstractFont import *
from Layout import *
from Renderers import *
from HTMLRenderer import *
from font_5x4 import FONT5x4
import random, math

blockDist = lambda fracMin, fracMax, count: random.randint(math.floor(fracMin * count), math.ceil(fracMax * count))

fw = LayoutGenerator(FONT5x4())
#fw.appendString("+")
fw.appendString("Lorem ipsum dolor\nsit amet; This is a test. Let's try this.")
fw.setLineWidth(100)
fw.setBreakOnWord(True)
fw = fw.get()  # Convert to LayoutWrapper

scatR = ScatterRenderer(5)
scatR.setDistrib(lambda val, count: count if val else 0)
#scatR.setDistrib(lambda val, count: blockDist(0.8, 1.0, count) if val else blockDist(0.0, 0.2, count))
fw = scatR.render(fw)

# Generate 10% noise in the white areas:
noiseR = NoiseRenderer(lambda v: 0 if v else 0.2)
fwNoise = noiseR.render(fw)

# Split such that each output image gets exactly 1/2 of the total.
sR = SplitRenderer(2)
sR.setDistrib(lambda val, count: 1 if val else 0)

compositeR = CompositeRenderer()


#shellR = ShellRenderer()
#shellR.render(scatR.render(fw))

#r = HTMLRenderer()
#fw = scatR.render(fw)
#print(r.wrapTables(r.render(lW) for lW in ([fw] + sR.render(fw))))

renders = [fwNoise, fw] + [compositeR.render(partW, fwNoise, lambda a, b: a or b) for partW in [fw] + sR.render(fw)]
i = 0
img = ImageRenderer(2000, 0)
for r in renders:
	img.render(r, "test_{}.png".format(i))
	i += 1