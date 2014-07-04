#!/usr/bin/python3
from AbstractFont import *
from Layout import *
from Renderers import *
from HTMLRenderer import *
from font_5x4 import FONT5x4
import random, math

lineWidth = 200
scatterFactor = 5

blockDist = lambda fracMin, fracMax, count: random.randint(math.floor(fracMin * count), math.ceil(fracMax * count))

fw = LayoutGenerator(FONT5x4())
with open('message.txt', 'r') as content_file:
	content = "\n".join(content_file.readlines())
	fw.appendString(content)
fw.setLineWidth(lineWidth)
fw.setBreakOnWord(True)
fw = fw.get()  # Convert to LayoutWrapper

scatR = ScatterRenderer(scatterFactor)
scatR.setDistrib(lambda val, count, line, col, row: count if val else 0)
fw = scatR.render(fw)

# Generate 10% noise in the white areas:
noiseR = NoiseRenderer(lambda v: 0 if v else 0.2)
fwNoise = noiseR.render(fw)

# Split such that each output image gets exactly 1/2 of the total.
sR = SplitRenderer(2)
sR.setDistrib(lambda val, count, line, col, row: (count if line == 0 else 1) if val else 0)

compositeR = CompositeRenderer()

#shellR = ShellRenderer()
#shellR.render(scatR.render(fw))

#r = HTMLRenderer()
#fw = scatR.render(fw)
#print(r.wrapTables(r.render(lW) for lW in ([fw] + sR.render(fw))))

renders = [fwNoise, fw] + [compositeR.render(partW, fwNoise, lambda a, b: a or b) for partW in [fw] + sR.render(fw)]
i = 0
img = ImageRenderer(lineWidth * scatterFactor * 5, 0)
for r in renders:
	img.render(r, "test_{}.png".format(i))
	i += 1