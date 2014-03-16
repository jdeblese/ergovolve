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
				prefix = 'SPECIAL_Fn'
				keys = map(lambda k: (shortmap[k] if k in shortmap.keys() else (k if k[0:3] == 'KEY' or k == '0' else prefix )),
					map(lambda k: k.strip(), ''
						.join(
						filter(lambda l: l != '',
							map(lambda l: comments.sub('', l),
								lines)))
						.split(',')))
				# Ignore keys marked as unused, or keys mapped to '0'
				layout = filter(lambda p: p[1] != 'unused' and p[0] != '0', zip(keys,sizes))
	return layout

if __name__ == '__main__' :
	import sys
	if len(sys.argv) > 1 :
		print parse(sys.argv[1])
