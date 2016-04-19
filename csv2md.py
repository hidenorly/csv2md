#!/usr/bin/env python
# coding: utf-8

from optparse import OptionParser, OptionValueError
import sys
import codecs
import csv

cset = 'utf-8'

reload(sys)
sys.setdefaultencoding(cset)
sys.stdin = codecs.getreader(cset)(sys.stdin)
sys.stdout = codecs.getwriter(cset)(sys.stdout)


def csvReader(filename):
	if filename == sys.stdin:
		file = codecs.getreader(cset)(filename)
	else:
		file = open(filename,"r")

	reader = csv.reader(file)

	lines = []
	for line in reader:
		lines.append(line)

	file.close()

	return lines

def fileLineWriter(filename, lines):
	if filename == sys.stdout:
		writer = codecs.getwriter(cset)(filename)
	else:
		writer = open(filename,"w")

	for line in lines:
		writer.write("{}\n".format(line))

	writer.close()

def replaceResult(lines, replacers):
	if len(replacers) and replacers[0]!="":
		for i in range(len(lines)):
			result = lines[i]
			for aReplacer in replacers:
				posE = aReplacer.find("=")
				if posE!=-1:
					key = aReplacer[0:posE]
					keyLen = len(key)
					value = aReplacer[posE+1:len(aReplacer)]
					pos = 0
					while pos!=-1:
						pos = result.find(key, pos)
						if pos!=-1:
							result = "{} {} {}".format(result[0:pos], value, result[pos+keyLen:len(result)])
							pos = pos + keyLen
			lines[i] = result

	return lines


def conertCsv2Md(csv, align):
	result = []
	theNumOfRow = len( csv )
	theNumOfColumn = len( csv[0] )

	# header
	startRow = 0
	if csv[0][0][0:1] == "#":
		# found header
		line = "|"
		startRow = 1
		for header in csv[0]:
			if header[0:1] == "#":
				header = header[1:len(header)]
			line = "{} {} |".format(line, header)
		result.append(line)

	# add text align
	line = "|"
	marker = ":---"
	if align=="center":
		marker = ":---:"
	elif align == "right":
		marker = "---:"

	for i in range(theNumOfColumn):
		line = "{}{}|".format(line, marker)
	result.append(line)

	# output data
	for y in range(startRow, theNumOfRow):
		line = "|"
		for x in range(theNumOfColumn):
			line = "{} {} |".format(line, csv[y][x])
		result.append(line)

	return result


if __name__ == '__main__':
	parser = OptionParser()

	parser.add_option("-c", "--charset", action="store", type="string", dest="charset", default=cset, help="Specify charset")
	parser.add_option("-o", "--output", action="store", type="string", dest="outFilename", default=sys.stdout, help="Specify output filename")
	parser.add_option("-r", "--replace", action="store", type="string", dest="replacers", default="", help="Specify replace key=value,...")
	parser.add_option("-a", "--align", action="store", type="string", dest="align", default="left", help="Specify --align=left or center or right")

	(options, args) = parser.parse_args()

	inFilename = sys.stdin
	if args:
		inFilename = args[0]

	# set charset
	cset = options.charset

	# get key-value for replacement
	replacers = []
	if options.replacers.find(",")!=-1:
		replacers = options.replacers.split(",")
	else:
		replacers = [ options.replacers ]

	# read markdown
	lines = csvReader(inFilename)

	result = conertCsv2Md(lines, options.align)

	# replace with specified replacer
	result = replaceResult(result, replacers)

	# output the processed html
	fileLineWriter( options.outFilename, result )