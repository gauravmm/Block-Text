#!/usr/bin/python3
from AbstractFont import *
from Renderers import *
from HTMLRenderer import *
from font_5x4 import FONT5x4

#fw = LayoutWrapper(FONT5x4())
#fw.appendString("Lorem ipsum dolor sit amet")

#fw.setLineWidth(100)
#fw.setBreakOnWord(True)

#sR = SplitRenderer(3)
#sR.setDistrib(lambda val, count: 1 if val else 0)

#r = HTMLRenderer()

#print(r.wrapTables(r.render(lW) for lW in ([fw] + sR.render(fw))))


fw = LayoutWrapper(FONT5x4())
fw.appendString("+")

scatR = ScatterRenderer(5)
shellR = ShellRenderer()
#print(scatR.render(fw).get())
shellR.render(scatR.render(fw))