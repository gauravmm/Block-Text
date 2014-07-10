#!/usr/bin/python3
from AbstractFont import *
from Layout import *
from Renderers import *
from HTMLRenderer import *
from font_5x4 import FONT5x4
import sys, argparse


def main():

	LEGAL_TYPES = ["TXT", "HTML", "PNG"]

	parser = argparse.ArgumentParser(description='Render split messages.')
	parser.add_argument("file", metavar="FILE", type=str, nargs="?",
						help="an ASCII/UTF-7 encoded text file to render. If not specified, defaults to STDIN.")
	parser.add_argument("-s", "--split", metavar="S", type=int, default=2,
						help='set the number of images to split the image into (default: 2)')
	parser.add_argument("-z", "--scale", metavar="S", type=int, default=5,
						help='set the size of each block in the block font (default: 5)')
	parser.add_argument("-n", "--noise", metavar="N", type=float, default=0.2,
						help='set the amount of noise in the white part of the image (default: 0.2)')
	#parser.add_argument("-d", "--density", metavar="D", type=float, default=1,
	#					help='set the shaded proportion of the black part of the image (default: 1)')
	parser.add_argument("--break-on-char", action="store_true",
						help='break lines on character boundaries (default: words are not broken across lines)')
	parser.add_argument("-f", "--first-line", action="store_true",
						help='do not split the first line')
	parser.add_argument("-w", "--width", metavar="W", type=int, default=-1,
						help='set the width of the output in blocks (default: set by output type)')
	parser.add_argument("-t", "--type", metavar="T", type=str, default=LEGAL_TYPES[0],
						help='output as ' + ", ".join(LEGAL_TYPES) + ' (default: ' + LEGAL_TYPES[0] + '). PNG requires PyCairo.')
	parser.add_argument("-o", "--output", metavar="FILE", type=str, default="",
						help='direct the output to this file (default: to stdout)')
	parser.add_argument("-v", "--verbose", action="store_true",
						help='output additional images')
	
	
	args = parser.parse_args()
	print(args)

	# Bounds checking:
	boundsCheck(args.scale, "scale", 1)
	boundsCheck(args.split, "split", 1)
	#boundsCheck(args.density, "density", 0, 1)
	boundsCheck(args.noise, "noise", 0, 1)
	if args.type.strip().upper() not in LEGAL_TYPES:
		print("Unrecognized type parameter: {}. Pick one of: {}".format(args.type.strip().upper(), ", ".join(LEGAL_TYPES)))
		exit()

	# Load string:
	content = ""
	if args.file is None:
		content = "\n".join(sys.stdin.readlines())
	else:
		try:
			with open(args.file, 'r') as content_file:
				content = "\n".join(content_file.readlines())
		except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
			print("Cannot read file " + args.file)
			exit()

	if content == "":
		print("There's nothing to render!")
		exit()

	# type='TXT'
	# output=''
	
	lineWidth = 200
	if args.width > 0:
		lineWidth = args.width
	elif args.output == "" and args.type == "TXT":
		lineWidth = 80

	scaleFactor = args.scale
	
	# Render the string in the font:
	fwGen = LayoutGenerator(FONT5x4())
	fwGen.appendString(content)
	fwGen.setLineWidth(lineWidth)
	fwGen.setBreakOnWord(True)
	fw = fwGen.get()  # Convert to BlockImage
	
	# Expand each cell in the image to a scaleFactor * scaleFactor square of cells.
	scatR = MapScaleRenderer(scaleFactor)
	scatR.setDistrib(lambda val, count, line, col, row: count if val else 0)
	fw = scatR.render(fw)

	# Generate an image that contains 20% noise in the white areas:
	noiseR = NoiseRenderer(lambda v: 0 if v else args.noise)
	fwNoise = noiseR.render(fw)

	# Split such that each output image gets exactly 1/2 of the total.
	sR = SplitRenderer(args.split)
	if args.first_line:
		sR.setDistrib(lambda val, count, line, col, row: (count if line == 0 else 1) if val else 0)

	compositeR = CompositeRenderer()

	#shellR = ShellRenderer()
	#shellR.render(scatR.render(fw))

	#r = HTMLRenderer()
	#fw = scatR.render(fw)
	#print(r.wrapTables(r.render(lW) for lW in ([fw] + sR.render(fw))))

	toComposite = sR.render(fw)
	if args.verbose:
		toComposite.append(fw)

	renders = [compositeR.render(partW, fwNoise, lambda a, b: a or b) for partW in toComposite]
	del toComposite

	if args.verbose:
		renders.extend([fwNoise, fw])

	i = 0
	img = ImageRenderer(lineWidth * scaleFactor * 5, 0)
	for r in renders:
		img.render(r, "test_{}.png".format(i))
		i += 1

def boundsCheck(val, _name, _min, _max=None):
	if val < _min:
		print("{} is too low, min: {}".format(_name, str(_min)))
	elif _max is not None and val > _max:
		print("{} is too high, max: {}".format(_name, str(_max)))
	else:
		return
	exit()

if __name__ == "__main__":
	main()
