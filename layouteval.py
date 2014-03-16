#!/usr/bin/env python

import sys,os,re,string,random,math,numpy
from deap import algorithms, base, creator, tools

from beige import fullset as excludes

import ergofirmware as ef

from simpletest import match_set_layout, cmpLayoutSet

if __name__ == '__main__' :
	from proposals import hof

	import sys,json
	if len(sys.argv) <= 1 :
		print "Please provide a file name"
		sys.exit(-1)

	filenames = tuple(sys.argv[1:])
	layouts = []
	layoutnames = []
	laysubopt = []
	allsubopt = []
	for fn in filenames :
		if fn[-1] == 'c' :
			this = ef.parse(fn)
			subset,rotated = match_set_layout(excludes, this, rotated=True)[1:]
			layouts.append(filter(lambda k: k[1] != '1x1', subset))
			laysubopt.append(filter(lambda k: k[1] != '1x1', rotated))
			allsubopt += rotated
			layoutnames.append(fn[:-2])
		elif fn[-4:] == 'json' :
			with open(fn,'r') as fh :
				jdata = json.load(fh)
			print '\nImporting %d layouts from JSON'%len(jdata)
			print 'Names: ' + ', '.join(map(lambda u: u['name'], jdata)) + '\n'
			for user in jdata :
				layoutnames.append(user['name'])
				this = []
				for key in user['horizontal_keys'] :
					this.append((key, '1.5x1'))
				for key in user['vertical_keys'] :
					this.append((key, '1x1.5'))
				for key in user['double_keys'] :
					this.append((key, '1x2'))
				subset,rotated = match_set_layout(excludes, this, rotated=True)[1:]
				layouts.append(filter(lambda k: k[1] != '1x1', subset))
				laysubopt.append(filter(lambda k: k[1] != '1x1', rotated))
				allsubopt += rotated

	if len(allsubopt) > 0 :
		print '''The following keys are available in the base
set in an incorrect orientation. They will
nonetheless be left out of the optimalization.'''
		print "  " + '\n  '.join(sorted(map(str,allsubopt)))

	for indi in hof :
		# Lower bounds on acceptable % coverage
		coverage,extra = [],[]
		for layout in layouts :
			c,e = cmpLayoutSet(layout, indi)
			c /= float(len(layout))
			coverage.append(c)
			extra.append(e)
		coverage = numpy.array(coverage)
		extra = numpy.array(extra)

		print "---\n"
		# Print the average % coverage
		print "%d keys, with:"%len(indi)
		print "  mean coverage %.1f%%"%(coverage.mean()*100)
		print "    std. deviation %.1f%%"%((coverage - coverage.mean()).std()*100)
		print "  median coverage %.1f%%"%(numpy.median(coverage)*100)
		print "  minimum coverage %.1f%%"%(coverage.min()*100)
		print "  maximum coverage %.1f%%"%(coverage.max()*100)
		# Print the keys in this set
		print '\n'.join(map(lambda k: str(k[::-1]),indi)) + '\n'
		# Generate statistics for how well this set covers each layout
		for layout,name,c,e,prerot in zip(layouts,layoutnames,coverage,extra,laysubopt) :
			print "Coverage of layout '%s' is %.0f%% with %d extra keys"%(name,100*c,e)
			if c != 1.0 :
				missing,rotated = match_set_layout(indi,layout,True)[1:]
				if len(prerot) > 0 :
					print "  Rotated keys from base set:\n    " + '\n    '.join(sorted(map(str,prerot)))
				if len(rotated) > 0 :
					print "  Suboptimal keys:\n    " + '\n    '.join(sorted(map(str,rotated)))
				if len(missing) > 0 :
					print "  Missing keys:\n    " + '\n    '.join(sorted(map(str,missing)))
			print ""
