#!/usr/bin/env python

import sys,os,re,string,random,math,numpy
from deap import algorithms, base, creator, tools

from beige import fullset as excludes

import ergofirmware as ef

# What about 'Left' and 'Right' keys? Keep the distinction?

# Some keys can be used interchangeably
aliases = (
	(("KEY_ReturnEnter", "1x2"), ("KEYPAD_ENTER", "1x2")), )

# Given two sets, return their relative complements
def match_set_layout(keyset1,keyset2,rotated=False) :
	modset1 = list(keyset1)
	modset2 = list(keyset2)
	compl2 = []
	rot = []
	# Find the keys in each set that are not in the other. Include
	# rotated versions of keys, if so desired.
	for key in modset2 :
		if key in modset1 :
			modset1.remove(key)
		else :
			rotkey = (key[0], 'x'.join(key[1].split('x')[::-1]))
			if rotated and rotkey in modset1 :
				modset1.remove(rotkey)
				rot.append(rotkey)
			else :
				compl2.append(key)
	# Now check if any aliased keys are in both
	for pair in aliases :
		# TODO check rotated aliases
		if pair[0] in modset1 and pair[1] in compl2 :
			modset1.remove(pair[0])
			compl2.remove(pair[1])
			print "Treating " + pair[0][0] + " and " + pair[1][0] + " as identical"
		elif pair[1] in modset1 and pair[0] in compl2 :
			modset1.remove(pair[1])
			compl2.remove(pair[0])
			print "Treating " + pair[0][0] + " and " + pair[1][0] + " as identical"
	# Return the Relative Complements of the two sets
	if rotated :
		return tuple(modset1), tuple(compl2), tuple(rot)
	else :
		return tuple(modset1), tuple(compl2)

def cmpLayoutSet(layout, keyset) :
	modset = list(layout)
	moditems = list(keyset)
	coverage, extra = 0.0, 0
	for key in moditems :
		if key in modset :
			modset.remove(key)
			coverage += 1
			# Rotated keys?
		else :
			size = key[1].split('x')
			rotated = (key[0], size[1] + 'x' + size[0])
			if rotated in modset :
				modset.remove(rotated)
				coverage += 0.5
			else :
				extra += 1
	return coverage,extra

def cxSet(ind1, ind2):
	"""Apply a crossover operation on input sets. A random cut point is
	chosen in each individual, and the rear segments are then swapped.
	"""
	sizes = (len(ind1),len(ind2))
	if len(ind1) > 2 and len(ind2) > 2 :
		idx1 = random.randint(0,len(ind1)-2)
		idx2 = random.randint(0,len(ind2)-2)
		ind1,ind2 = ind1[:idx1] + ind2[idx2:], ind2[:idx2] + ind1[idx1:]
	s = lambda i: creator.Individual(sorted(tuple(i)))
	return s(ind1),s(ind2)

def deapsetup(layouts) :
	# Make a list of all desired keys, so that an individual can be an index to this list
	items = []
	for keyset in layouts :
		for key in keyset :
			if key not in items :
				items.append(key)
	items = tuple(items)

	IND_INIT_SIZE = 20

	# Define functions here that form a closure using 'items'
	def evalLayout(individual) :
		avgcoverage, maxextra = 0.0, 0.0
		for layout in layouts :
			txt = map(lambda idx: items[idx], individual)
			coverage,extra = cmpLayoutSet(layout, txt)
			coverage /= float(len(layout))
			assert coverage <= 1.0
			assert coverage >= 0.0
			avgcoverage += coverage
			maxextra += extra
		return maxextra/len(layouts),avgcoverage/len(layouts)

	def mutSet(individual):
		"""Mutation that pops or add an element."""
		if random.random() < 0.5:
			if len(individual) > 0:	 # We cannot pop from an empty set
				individual.remove(random.choice(sorted(tuple(individual))))
		else:
			individual.append(random.randrange(len(items)))
		return creator.Individual(sorted(tuple(individual))),

	def unmap(population) :
		"""Maps a population to a list of key specifications"""
		return map(lambda ind: map(lambda idx: items[idx], ind), population)

	creator.create('Fitness', base.Fitness, weights=(-0.1,1.0))
	# Individual must be a list, as a key can occur more than once
	creator.create('Individual', list, fitness=creator.Fitness)

	toolbox = base.Toolbox()
	# Attribute generator
	toolbox.register("attr_item", random.randrange, len(items))
	# Structure initializers
	toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, IND_INIT_SIZE)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", evalLayout)
	toolbox.register("mate", cxSet)
	toolbox.register("mutate", mutSet)
	toolbox.register("select", tools.selNSGA2)
	toolbox.register("unmap", unmap)

	return toolbox

def main(toolbox):
	NGEN = 250
	MU = 100
	LAMBDA = 200
	CXPB = 0.7
	MUTPB = 0.2

	pop = toolbox.population(n=MU)
	hof = tools.ParetoFront()

	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats_len = tools.Statistics(key=len)
	mstats = tools.MultiStatistics(xfitness=stats, length=stats_len)
	mstats.register("avg", numpy.mean, axis=0)
	mstats.register("std", numpy.std, axis=0)

	algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, mstats, halloffame=hof)

	return toolbox.unmap(pop), stats, toolbox.unmap(hof)


if __name__ == '__main__' :
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
			print 'Importing %d layouts from JSON'%len(jdata)
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

	# Set up DEAP toolbox
	toolbox = deapsetup(layouts)
	# Optimize
	pop,stats,hof = main(toolbox)
	# Print out results from the hall of fame
	for indi in hof :
		# Upper bounds on number of acceptable keys
		if len(indi) > 20 :
			continue

		# Lower bounds on acceptable % coverage
		coverage,extra = [],[]
		for layout in layouts :
			c,e = cmpLayoutSet(layout, indi)
			c /= float(len(layout))
			coverage.append(c)
			extra.append(e)
		coverage = numpy.array(coverage)
		extra = numpy.array(extra)
#		if coverage.min() < 0.6 :
#			print "Minimum coverage is too low (%.0f%%)"%(coverage.min()*100)
#			continue

		print "---\n"
		# Print the average % coverage
		print "%d keys with an average coverage of %.0f%%\n"%(len(indi), coverage.mean()*100)
		# Print the keys in this set
		print '\n'.join(sorted(map(lambda k: str(k[::-1]),indi))) + '\n'
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
		print ""
