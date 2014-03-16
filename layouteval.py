#!/usr/bin/env python

import sys,os,re,string,random,math,numpy, json
from deap import algorithms, base, creator, tools

from beige import fullset as excludes
from proposals import hof

import ergofirmware as ef

from simpletest import match_set_layout, cmpLayoutSet, loadLayouts, loadSubLayouts, printStats

if __name__ == '__main__' :
	if len(sys.argv) <= 1 :
		print "Please provide a file name"
		sys.exit(-1)

	full = True

	if full :
		layouts = loadLayouts(sys.argv[1:])
		laysubopt = {}
		for n in layouts.keys() :
			laysubopt[n] = []
		excludes = tuple(filter(lambda k: k[1] == '1x1.5' or k[1] == '1.5x1' or k[1] == '2x1' or k[1] == '1x2', excludes))
		hof = map(lambda keyset: tuple(keyset) + excludes, hof)
	else :
		layouts, laysubopt, allsubopt = loadSubLayouts(sys.argv[1:])

	print 'Loaded %d layouts'%len(layouts)
	print 'Names: ' + ', '.join(sorted(layouts.keys())) + '\n'

	printStats(hof, layouts, laysubopt)
