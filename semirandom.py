#!/usr/bin/python

from crossword import *
import numpy
import sys
import random
import copy

debug = open("debug.txt", "w")
globalitr = 0
globalitrmax = 4000

def recurseRandom(pt, plt, u, v, iterr, d, wlf):
	p = copy.copy(pt)
	pl = copy.copy(plt)
	global debug
	global globalitr
	if globalitr > globalitrmax:
		return 0
	print "entering recurse for", u, v, iterr
	printPuzzle(p, pl)
	if p[u][v] == -1:
		ur, vr, dirr = getRandomSpace(pt, wlf)
		print "Block; moving to", ur, vr, dirr
		return recurseRandom(pt, plt, ur, vr, iterr, dirr, wlf)
	else:
		flag = 0
		print "looking at", u, v, d, iterr, globalitr
		pos = findPossible(p, pl, u, v, wlf, d)
		if len(pos) == 0:
			#print "Branch dead."
			return 0
		while flag == 0 and globalitr < globalitrmax:
			globalitr += 1
			p_pop = pickBest(p, pl, pos, u, v, d, iterr+1, wlf)
			if p_pop != 0:
				ptemp, pltemp = addWord(p, pl, p_pop, u, v, d)
				ur, vr, dirr = getRandomSpace(ptemp, wlf)
				print "moving to", ur, vr, dirr
				flag = recurseRandom(ptemp, pltemp, ur, vr, iterr+1, dirr, wlf)
			else:
				print "Branch dead."
				return 0
		return flag

def getRandomSpace(p, wlf):
	lh = []
	lv = []
	flag = 1
	for i in range(1, len(p)-1):
		for j in range(1, len(p)-1):
			lh.append([i,j])
			lv.append([i,j])
	while (len(lv) > 0 or len(lh) > 0) and flag == 1:
		dirflag = int(random.random()*2)
		if dirflag % 2:
			temp = lv.pop(int(random.random()*len(lv)))
		else:
			temp = lh.pop(int(random.random()*len(lh)))
		flag = len(findPossible(p, [], temp[0], temp[1], wlf, dirflag))
	if len(lv) == 0 and len(lh) == 0:
		print "Puzzle found."
		printPuzzle(p, [])
		sys.exit(0)
	return temp[0], temp[1], dirflag

def pickBest(pt, plt, pos, u, v, hor_vert, max_consider, wlf):
	p = copy.copy(pt)
	pl = copy.copy(plt)
	if max_consider > len(pos):
		max_consider = len(pos)
	poss = []
	i_eval = 0
	eval_max = 0
	for i in range(0, max_consider):
		lens = []
		poss.append(pos.pop(int(random.random()*len(pos))))
		ptemp, pltemp = addWord(p, pl, poss[i], u, v, hor_vert)
		wordrange = findRange(p, pl, u, v, wlf, hor_vert)
		for j in range(wordrange[0]+1, wordrange[1]-1):
			t = findPossible2(ptemp, pltemp, u, v, j, wlf, hor_vert+1)
			lens.append(len(t))
		eltemp = evalLens(lens)
		if eltemp > eval_max:
			i_eval = i
			eval_max = eltemp
	if eval_max == 0:
		return 0
	else:
		print "adding '", poss[i_eval], "' with an evaluation of", eval_max, "out of", max_consider
		return poss[i_eval]

def evalLens(l):
	if len(l) == 0:
		return 0
	else:
		return ( max(l) + min(l) + float(sum(l)/len(l)) )*min(l)	

def scatterLetter(pt, letter, prob):
	p = copy.copy(pt)
	for i in range(0, len(p)):
		for j in range(0, len(p)):
			if random.random() < prob and p[i][j] != -1:
				p[i][j] = encodeLetter(letter)
	return p

def fillBlocks(pt, pl, blocklist):
	p = copy.copy(pt)
	l = len(p) - 1
	for i in range(0, len(blocklist)):
		u = blocklist[i][0]
		v = blocklist[i][1]
		p[u][v] = -1
		p[l-u][l-v] = -1
	printPuzzle(p, pl)
	return p, pl

def scatterBlocks(pt, pl, prob, maxn, wlf):
	p = copy.copy(pt)
	l = len(p)-1 
	count = 0
	for i in range(1, l-1):
		for j in range(i, l-1):
			if random.random() < prob and count < maxn:
				count += 2
				p[i][j] = -1
				p[l-i][l-j] = -1

	printPuzzle(p, pl)

	for i in range(1, len(p)-1):
		for j in range(1, len(p)-1):
			if p[i][j] == -1:
				f1 = 1
				f2 = 1
				f3 = 1
				f4 = 1
				#print i, j
				if j != 1:
					f1 = len(findPossible(p, [], i, j-1, wlf, 1))
				if j != len(p) - 1:
					f2 = len(findPossible(p, [], i, j+1, wlf, 1))
				if i != 1:
					f3 = len(findPossible(p, [], i-1, j, wlf, 0))
				if i != len(p) -1:
					f4 = len(findPossible(p, [], i+1, j, wlf, 0))
				#print f1, f2, f3, f4
				if not f1 or not f2 or not f3 or not f4:
					p[i][j] = 0

	printPuzzle(p, pl)
	return p, pl

def randomWord(pt, plt, wlf):
	p = copy.copy(pt)
	pl = copy.copy(plt)
	flag = 0
	while flag == 0:
		u = 1 + int(random.random()*(len(p)-2))
		v = 1 + int(random.random()*(len(p)-2))
		s = int(random.random()*2)
		pos = findPossible(p, pl, u, v, wlf, s)
		flag = len(pos)
	pn, pln = addWord(p, pl, pos[int(random.random()*len(pos))], u, v, s)
	return pn, pln

def checkFeasible(pt, plt, wlf):
	print "Checking feasibility."
	p = copy.copy(pt)
	pl = copy.copy(plt)
	flagl = []
	for i in range(1, len(p)-1):
		for j in range(1, len(p)-1):
			flagl.append(len(findPossibleS(p, j, i, wlf, 0)))
			flagl.append(len(findPossibleS(p, j, i, wlf, 1)))
	printPuzzle(p, pl)
	print "Puzzle has feasability", min(flagl)
	return min(flagl)

def startSearch(p, pl, wlf):
	global globalitr
	globalitr = 0

	if not recurseRandom(p, pl, int(random.random()*len(p)), int(random.random()*len(p)), 0, int(random.random()), wlf):
		print "Puzzle not feasible."
		return 0

	return 1

if __name__ == "__main__":
	if len(sys.argv) == 2:
		wlf = sys.argv[1]
		if os.path.isfile(wlf):
			print "Starting puzzle."
			p, pl = makeNewPuzzle(9)
			printPuzzle(p, pl)
			p, pl = fillBlocks(p, pl, [ [1,1], [1,5], [1,6], [2,6], [4,7], [4,8], [4,9], [5,5], [8,9], [9,9] ])

			while not startSearch(p, pl, wlf):
				pass
		else:
			print "Dictionary not a real file."
	else:
		print "No dictionary provided."
m()*len(p)), 0, int(random.random()), wlf):
		print "Puzzle not feasible."
		return 0

	return 1

if __name__ == "__main__":
	if len(sys.argv) == 2:
		wlf = sys.argv[1]
		if os.path.isfile(wlf):
			print "Starting puzzle."
			p, pl = makeNewPuzzle(9)
			printPuzzle(p, pl)
			p, pl = fillBlocks(p, pl, [ [1,1], [1,5], [1,6], [2,6], [4,7], [4,8], [4,9], [5,5], [8,9], [9,9] ])

			while not startSearch(p, pl, wlf):
				pass
		else:
			print "Dictionary not a re