#!/usr/bin/python3
from AbstractFont import *
from Renderers import *
from HTMLRenderer import *
from font_5x4 import FONT5x4
import random, math

blockDist = lambda fracMin, fracMax, count: random.randint(math.floor(fracMin * count), math.ceil(fracMax * count))

fw = LayoutWrapper(FONT5x4())
#fw.appendString("+")
fw.appendString("Lorem ipsum dolor sit amet")
fw.setLineWidth(100)
fw.setBreakOnWord(True)

scatR = ScatterRenderer(4)
scatR.setDistrib(lambda val, count: blockDist(0.8, 1.0, count) if val else blockDist(0.0, 0.2, count))
#scatR.setDistrib(lambda val, count: 0 if val else count)

sR = SplitRenderer(2)
sR.setDistrib(lambda val, count: 1 if val else 0)

#shellR = ShellRenderer()
#shellR.render(scatR.render(fw))

r = HTMLRenderer()

#fw = scatR.render(fw)
#print(r.wrapTables(r.render(lW) for lW in ([fw] + sR.render(fw))))

renders = [fw] + sR.render(fw)
print(r.wrapTables(r.render(scatR.render(lW)) for lW in renders))