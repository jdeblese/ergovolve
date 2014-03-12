#!/usr/bin/env python

import sys,os,re,string,random,math,numpy
from deap import algorithms, base, creator, tools

from beige import fullset as excludes

import ergofirmware as ef

# What about 'Left' and 'Right' keys? Keep the distinction?

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
		ind1,ind2 = creator.Individual(ind1[:idx1] + ind2[idx2:]), creator.Individual(ind2[:idx2] + ind1[idx1:])
#	print sizes,"->",(len(ind1),len(ind2))
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

	IND_INIT_SIZE = len(items)

	# Define functions here that form a closure using 'items'
	def evalLayout(individual) :
		mincoverage, maxextra = 1, 0
		for layout in layouts :
			txt = map(lambda idx: items[idx], individual)
			coverage,extra = cmpLayoutSet(layout, txt)
			coverage /= 1.0 * len(layout)
			mincoverage = min(coverage,mincoverage)
			maxextra = max(extra,maxextra)
		return maxextra,mincoverage

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

	creator.create('Fitness', base.Fitness, weights=(-0.2,1.0))
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
	NGEN = 100
	MU = 50
	LAMBDA = 100
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
	layout = ef.parse('layout.c')

	subset = ef.match_set_layout(excludes, layout, rotated=True)[1]
	ergoset = tuple(subset)
	ergoset2 = tuple(ergoset[:-2]) + (("KEY_RightGui", "1x1"), ("KEY_RightControl", "1x1"), ("KEY_RightControl", "1x1"))
	ergoset2 = ((ergoset2[0][0], 'x'.join(ergoset2[0][1].split('x')[::-1])), ) + ergoset2[1:]
	layouts = (ergoset,ergoset2)

	# Set up DEAP toolbox
	toolbox = deapsetup(layouts)
	# Optimize
	pop,stats,hof = main(toolbox)
	# Print out results from the hall of fame
	for indi in hof :
		print "---\n"
		for layout,name in zip(layouts,('test1','test2')) :
			c,e = cmpLayoutSet(layout, indi)
			print "Coverage of layout '" + name + "' is " + str(int(c*100/len(layout))) + "% with " + str(e) + " extra keys"
			if int(c) != len(layout) :
				missing = ef.match_set_layout(indi, layout)[1]
				print "  Missing keys:\n    " + '\n    '.join(sorted(map(str,missing)))
		print ""
		print '\n'.join(sorted(map(str,indi)))
		print ""
