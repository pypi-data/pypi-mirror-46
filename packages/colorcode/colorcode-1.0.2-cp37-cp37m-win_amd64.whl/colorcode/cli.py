
"""
Command line interface

This module contains the whole command line interface
including argument parsing and main procedure
"""

import argparse
import sys

from .loader import BUILDERS
from .imgen.interleave import INTERLEAVING_MODES, BEST_PARSE_MODE
from .imgen.draw import ImGenerator

_parseBool = lambda i: i.lower()[0] in '1tyo' and i.lower()[1] != 'f'

def _apInit():
	parser = argparse.ArgumentParser(
		description = "Generate multi-colored 2D codes"
	)

	parser.add_argument(
		'-t',
		'--type',
		action = 'store',
		choices = BUILDERS.keys(),
		default = 'aztec',
		dest = 'type',
		help = 'Type of code to generate',
	)

	parser.add_argument(
		'-i',
		'--interleaving',
		action = 'store',
		choices = INTERLEAVING_MODES.keys(),
		default = None,
		dest = 'int',
		help = 'Interleaving method to use',
	)
	parser.add_argument(
		'-m',
		'--module-size',
		action = 'store',
		type = int,
		default = 32,
		dest = 'msize',
		help = 'Number of pixels on one side of a module',
	)
	parser.add_argument(
		'-q',
		'--quiet-zone',
		action = 'store',
		type = int,
		default = 4,
		dest = 'qzone',
		help = 'Number of modules between the edge of the image and the code',
	)
	parser.add_argument(
		'--aztec-layers',
		action = 'store',
		type = int,
		default = None,
		dest = 'aztec_layers',
		help = 'For Aztec codes: force the number of layers',
	)
	parser.add_argument(
		'--aztec-compact',
		action = 'store',
		type = _parseBool,
		default = None,
		dest = 'aztec_compact',
		help = 'For Aztec codes: force the use of compact mode (truthy) or full mode (falsey)',
	)
	
	parser.add_argument(
		'-f',
		'--from-files',
		action = 'store_true',
		dest = 'usefiles',
		help = 'If specified, the DATA arguments will be interpeted as file names from which the data will be read',
	)
	parser.add_argument(
		'-o',
		'--out',
		action = 'store',
		default = 'code.png',
		dest = 'out',
		help = 'The output file. If the value is "-", PNG image will be output to stdout.',
	)
	parser.add_argument(
		'data',
		action = 'store',
		nargs = '+',
		metavar = 'DATA',
		help = 'The data of each code',
	)

	return parser

def parseCLI(*a):
	"""
	Parse command line arguments

	This function parse the command line arguments
	with which the program has been started
	and prepares them for use with the main program

	Returns
	-------
	data : :py:class:`list`
		The list of data elements to encode
	codeType : :py:class:`str`
		The id of the code generation module
	outfile : :py:class:`str`
		The name of the file to which the image will be saved
	cgenKwargs : :py:class:`dict`
		The dictionnary to be passed by keyword argument expansion
		to the code builder constructor
	imgenKwargs : :py:class:`dict`
		The dictionnary to be passed by keyword argument expansion
		to the image builder constructor
	"""

	args = _apInit().parse_args(*a)
	codeType = args.type

	if args.usefiles:
		data = [open(f, 'rb').read() for f in args.data]
	else:
		data = [d.encode('utf8') for d in args.data]
	
	if args.int is not None:
		interleave = INTERLEAVING_MODES[args.int]
	else:
		interleave = INTERLEAVING_MODES[BEST_PARSE_MODE[len(data) - 1]]
	if args.int is not None and len(data) > interleave['maxcodes']:
		raise ArgumentError("Too many codes specified for this interleaving mode")

	imgenKwargs = {
		'interleaving' : interleave['int'],
		'imageMode' : interleave['mode'],
		'modSize' : args.msize,
		'quietZone' : args.qzone,
	}

	cgenKwargs = {}

	if codeType == 'aztec':
		cgenKwargs['forceLayers'] = args.aztec_layers
		cgenKwargs['forceCompact'] = args.aztec_compact
	
	return data, codeType, args.out, cgenKwargs, imgenKwargs

def main():
	"""
	Main procedure of the CLI version of the program

	This function is the main of the program for use in command line mode.
	"""
	data, codeType, outfile, cgenKwargs, imgenKwargs = parseCLI()
	cgenClass = BUILDERS[codeType]['builder']
	cgenInstances = [cgenClass(d, **cgenKwargs) for d in data]
	size = max((g.size for g in cgenInstances), key = BUILDERS[codeType]['params']['sizeSortKey'])
	for g in cgenInstances:
		g.size = size
	codes = [g.encode() for g in cgenInstances]
	imgenerator = ImGenerator(codes, **imgenKwargs)
	imgenerator.drawCode()
	if outfile == "-":
		imgenerator.saveImage(sys.stdout.buffer, format="png")
	else:
		imgenerator.saveImage(outfile)
