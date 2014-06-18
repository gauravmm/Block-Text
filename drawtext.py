#!/usr/bin/python3
from AbstractFont import *
from Renderers import *
from font_5x4 import FONT5x4

fw = LayoutWrapper(FONT5x4())
fw.appendString("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc commodo, nibh eu lobortis lobortis, augue nibh mattis sem, quis varius eros lorem eu velit. In diam quam, convallis sed dapibus pellentesque, pretium nec enim.")
#print(fw.get())

fw.setLineWidth(100)
fw.setBreakOnWord(False)

r = ShellRenderer()
r.render(fw)
