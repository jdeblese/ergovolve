#!/usr/bin/env python

import sys,os,re

names = 'keyboard.h'
shortnames = 'keyboard--short-names.h'

comments = re.compile('[ \t]*//.*$')

sizes = ('unused',
        # Left Fingers
         '1.5x1', '1x1',  '1x1',  '1x1',  '1x1',  '1x1',  '1x1',
         '1.5x1', '1x1',  '1x1',  '1x1',  '1x1',  '1x1',  '1x1.5',
         '1.5x1', '1x1',  '1x1',  '1x1',  '1x1',  '1x1',
         '1.5x1', '1x1',  '1x1',  '1x1',  '1x1',  '1x1',  '1x1.5',
         '1x1',  '1x1',  '1x1',  '1x1',  '1x1',
         # Left Thumb
         '1x1', '1x1',
         'unused', 'unused', '1x1',
         '1x2', '1x2', '1x1',
         # Right Hand
         '1x1', '1x1',  '1x1',  '1x1',  '1x1',  '1x1',  '1.5x1',
       '1x1.5', '1x1',  '1x1',  '1x1',  '1x1',  '1x1',  '1.5x1',
                '1x1',  '1x1',  '1x1',  '1x1',  '1x1',  '1.5x1',
       '1x1.5', '1x1',  '1x1',  '1x1',  '1x1',  '1x1',  '1.5x1',
                        '1x1',  '1x1',  '1x1',  '1x1',  '1x1',
         # Right Thumb
         '1x1', '1x1',
         '1x1', 'unused', 'unused',
         '1x1', '1x2', '1x2' )


# Some keys can be used interchangeably
aliases = (
	(("KEY_ReturnEnter", "1x2"), ("KEYPAD_ENTER", "1x2")), )

# Given two sets, return their relative complements
def match_set_layout(keyset1,keyset2,rotated=False) :
	modset1 = list(keyset1)
	modset2 = list(keyset2)
	compl2 = []
	# Find the keys in each set that are not in the other. Include
	# rotated versions of keys, if so desired.
	for key in modset2 :
		if key in modset1 :
			modset1.remove(key)
		else :
			rotkey = (key[0], 'x'.join(key[1].split('x')[::-1]))
			if rotated and rotkey in modset1 :
				print "Key " + str(key) + " found in a rotated version, excluding..."
				modset1.remove(rotkey)
			else :
				compl2.append(key)
	# Now check if any aliased keys are in both
	for pair in aliases :
		if pair[0] in modset1 and pair[1] in compl2 :
			modset1.remove(pair[0])
			compl2.remove(pair[1])
			print "Treating " + pair[0][0] + " and " + pair[1][0] + " as identical"
		elif pair[1] in modset1 and pair[0] in compl2 :
			modset1.remove(pair[1])
			compl2.remove(pair[0])
			print "Treating " + pair[0][0] + " and " + pair[1][0] + " as identical"
	# Return the Relative Complements of the two sets
	return tuple(modset1), tuple(compl2)

# Build a dictionary mapping based on C #defines
def buildmap(fn, typefn, regex) :
	mapdict = {}
	with open(fn,'r') as fh :
		line = fh.readline()
		while line != '' :
			m = regex.match(line)
			if m is not None and m.group(2) != '' :
				mapdict[m.group(1)] = typefn(m.group(2))
			line = fh.readline()
	return mapdict

def parse(filename) :
	# Construct various maps based on available header files
	shortmap = buildmap(shortnames, str, re.compile('^[ \t]*#define[ \t]*([a-z_0-9]*)[ \t]*(KEY[a-z_0-9]*)', re.IGNORECASE))
	namemap = buildmap(names, lambda s: int(s,16), re.compile('^[ \t]*#define[ \t]*(KEY[a-z_0-9]*)[ \t]*(0x[a-z_0-9]*)', re.IGNORECASE))
	# Build the inverse scancode->name map
	codemap = {v:k for k,v in namemap.iteritems()}

	# Read in the layout defined in 'filename'
	with open(filename, 'r') as fh :
		layout = None
		while layout is None :
			line = fh.readline()
			# Find the definition of the first layer
			if line.find('_kb_layout') != -1 :
				while line.find('),') == -1 :
					line += fh.readline()
				# Extract the list of keys
				start = line.find('KB_MATRIX_LAYER') + 16
				end = line.find('),', start)
				lines = line[start:end].split('\n')
				# Delete comments
				# Filter out empty lines
				# Combine, then split on commas, removing whitespace
				# Map the short names to long names. Assume any unknown keys are layer keys
				prefix = 'SPECIAL_Layer_'
				keys = map(lambda k: (shortmap[k] if k in shortmap.keys() else (prefix + str(k))),
					map(lambda k: k.strip(), ''
						.join(
						filter(lambda l: l != '',
							map(lambda l: comments.sub('', l),
								lines)))
						.split(',')))
				# Ignore keys marked as unused, or keys mapped to '0'
				layout = filter(lambda p: p[1] != 'unused' and p[0] != prefix + '0', zip(keys,sizes))
	return layout

if __name__ == '__main__' :
	print parse('jw.c')
