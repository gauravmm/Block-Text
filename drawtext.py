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
fw.appendString("Lorem ipsum dolor sit amet; This is a test. Let's try this.")
fw.setLineWidth(100)
fw.setBreakOnWord(True)
fw = fw.get()  # Convert to LayoutWrapper

scatR = ScatterRenderer(4)
scatR.setDistrib(lambda val, count: blockDist(0.8, 1.0, count) if val else blockDist(0.0, 0.2, count))
#scatR.setDistrib(lambda val, count: 0 if val else count)

sR = SplitRenderer(2)
sR.setDistrib(lambda val, count: 1 if val else 0)

#shellR = ShellRenderer()
#shellR.render(scatR.render(fw))

#r = HTMLRenderer()
#fw = scatR.render(fw)
#print(r.wrapTables(r.render(lW) for lW in ([fw] + sR.render(fw))))

fw = scatR.render(fw)
renders = [fw] + sR.render(fw)
i = 0
img = ImageRenderer(1600, 2)
for r in renders:
	img.render(r, "test_{}.png".format(i))
	i += 1