#!/usr/bin/env python

import sys,os,re,string,random,math,numpy, json
from deap import algorithms, base, creator, tools

from beige import fullset as excludes
from proposals import hof

import ergofirmware as ef

from simpletest import match_set_layout, cmpLayoutSet, loadSubLayouts, printStats

if __name__ == '__main__' :
	if len(sys.argv) <= 1 :
		print "Please provide a file name"
		sys.exit(-1)

	layouts, laysubopt, allsubopt = loadSubLayouts(sys.argv[1:])

	print 'Loaded %d layouts'%len(layouts)
	print 'Names: ' + ', '.join(sorted(layouts.keys())) + '\n'

	printStats(hof, layouts, laysubopt)
