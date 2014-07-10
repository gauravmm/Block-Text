#!/usr/bin/python3
from AbstractFont import *
from Layout import *
from Renderers import *
from HTMLRenderer import *
from font_5x4 import FONT5x4
import argparse


def main():
	parser = argparse.ArgumentParser(description='Render split messages.')
	parser.add_argument("file", metavar="FILE", type=str, nargs="?",
						help="an ASCII/UTF-7 encoded text file to render. If not specified, defaults to STDIN.")
	parser.add_argument("-s", "--split", metavar="S", type=int, default=2,
						help='set the number of images to split the image into (default: 2)')
	parser.add_argument("-z", "--scale", metavar="S", type=int, default=1,
						help='set the size of each block in the block font (default: 1)')
	parser.add_argument("-n", "--noise", metavar="N", type=float, default=0.2,
						help='set the amount of noise in the white part of the image (default: 0.2)')
	parser.add_argument("-d", "--density", metavar="D", type=float, default=1,
						help='set the shaded proportion of the black part of the image (default: 1)')
	parser.add_argument("-f", "--firstline", default=False, const=True, action="store_const",
						help='do not split the first line')
	parser.add_argument("-w", "--width", metavar="W", type=int, default=-1,
						help='set the width of the output in blocks (default: 1)')
	parser.add_argument("-o", "--output", metavar="FILE", type=str, default="",
						help='direct the output to this file (default: to stdout)')
	

	args = parser.parse_args()
	print(args.accumulate(args.integers))


	lineWidth = 200
	scatterFactor = 5

	fw = LayoutGenerator(FONT5x4())
	with open('message.txt', 'r') as content_file:
		content = "\n".join(content_file.readlines())
		fw.appendString(content)
	fw.setLineWidth(lineWidth)
	fw.setBreakOnWord(True)
	fw = fw.get()  # Convert to LayoutWrapper

	scatR = MapScaleRenderer(scatterFactor)
	scatR.setDistrib(lambda val, count, line, col, row: count if val else 0)
	fw = scatR.render(fw)

	# Generate 20% noise in the white areas:
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

if __name__ == "__main__":
	main()