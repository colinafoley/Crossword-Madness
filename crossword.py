#!/usr/bin/python

import numpy
import sys
import os
import copy

#alphabet key
a_key = ['.', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '#']

def decode(word):
	global a_key
	ret = "^"
	for i in range(1, len(word)-1):
		ret = ret + a_key[word[i]]
	return ret + "$"

def encode(word):
	global a_key
	ret = [0 for i in range(0, len(word))]
	for i in range(0, len(word)):
		for j in range(0, len(a_key)):
			if word[i] == a_key[j]:
				ret[i] = j
				break
	return ret

def encodeLetter(letter):
	global a_key
	for i in range(0, len(a_key)):
		if letter == a_key[i]:
			return i

def writeLine(word):
	global a_key
	ret = ""
	for i in range(0, len(word)):
		ret = ret + a_key[word[i]] + "  "
	return ret

def findWordRangeH(p, r, c):
	ret = [-1, -1]
	for i in range(c, len(p)):
		if p[r,i] == -1:
			ret[1] = 1 + i
			break
	for i in range(c, -1, -1):
		if p[r,i] == -1:
			ret[0] = i
			break
	return ret

def findWordRangeV(p, r, c):
	ret = [-1, -1]
	for i in range(r, len(p)):
		if p[i,c] == -1:
			ret[1] = 1 + i
			break
	for i in range(r, -1, -1):
		if p[i,c] == -1:
			ret[0] = i
			break
	return ret

#if flag is even, findPossibleV, else findPossibleH
def findPossible(p, plt, r, c, wlf, flag):
	#print "findpossible"
	if flag % 2:
		return findPossibleH(p, plt, r, c, wlf)
	else:
		return findPossibleV(p, plt, r, c, wlf)

def findRange(p, plt, r, c, wlf, flag):
	#print "findpossible"
	if flag % 2:
		return findWordRangeH(p, r, c)
	else:
		return findWordRangeV(p, r, c)

#if flag is even, findPossibleV, else findPossibleH taking the same format
def findPossibleS(p, plt, r, c, wlf, flag):
	#print "findpossibles"
	if flag % 2:
		return findPossibleH(p, plt, c, r, wlf)
	else:
		return findPossibleV(p, plt, r, c, wlf)

def findPossible2(p, plt, r, c, j, wlf, flag):
	#print "findpossibles"
	if flag % 2:
		return findPossibleH(p, plt, j, c, wlf)
	else:
		return findPossibleV(p, plt, r, j, wlf)

#if flag is even, addWordV, else addWordH
def addWord(pt, plt, w, r, c, flag):
	p = copy.copy(pt)
	pl = copy.copy(plt)
	if flag % 2:
		return addWordH(p, pl, w, r, c)
	else:
		return addWordV(p, pl, w, r, c)

#if flag is even, addWordV, else addWordH taking the same format
def addWordS(pt, plt, w, r, c, flag):
	p = copy.copy(pt)
	pl = copy.copy(plt)
	#print "adding word", w
	if flag % 2:
		return addWordH(p, pl, w, r, c)
	else:
		return addWordV(p, pl, w, c, r)

def printPuzzle(p, pl):
	stri = "    "
	for i in range(0, len(p[0])):
		if i < 10:
			stri += str(i) + "  "
		else:
			stri += str(i-10) + "  "
	print stri
	for i in range(0, len(p[0])):
		if i < 10:
			print str(i) + "   " + writeLine(p[i,:])
		else:
			print str(i-10) + "   " + writeLine(p[i,:])
	print pl

#add a word horizontally starting at (r,c) and add a -1 at the end
def addWordH(p, pl, w, r, c):
	temp = findWordRangeH(p, r, c)
	p[r,temp[0]+1:temp[1]-1] = encode(w)
	p[r,temp[1]-1] = -1
	pl.append(w)
	#p[r,c:(c+len(w))] = encode(w)
	#p[r,(c+len(w))] = -1
	return p, pl

#add a word vertically starting at (r,c) and add a -1 at the end
def addWordV(p, pl, w, r, c):
	temp = findWordRangeV(p, r, c)
	p[temp[0]+1:temp[1]-1,c] = encode(w)
	p[temp[1]-1,c] = -1
	pl.append(w)
	#p[r:(r+len(w)),c] = encode(w)
	#p[(r+len(w)),c] = -1
	return p, pl

def getList(s, wlf):
	ret = os.popen(("grep " + s + " " + wlf)).read().split("\n")
	ret = ret[0:len(ret)-1]
	return ret

def findPossibleH(p, pl, r, c, wlf):
	#print "finding H", r, c
	#printPuzzle(p, pl)
	#return getList(decode(p[r,c:findWordEnd(p[r,:],c)]), wlf)
	temp = findWordRangeH(p, r, c)
	gl = getList(decode(p[r,temp[0]:temp[1]]), wlf)
	count = 0
	for i in range(0, len(gl)):
		if gl[i-count] in pl:
			#print "removing", gl[i-count], r, c
			gl.pop(i-count)
			#print "removing", temp
			count += 1
	return gl

def findPossibleH2(p, pl, r, c, wlf):
	#print "finding H", r, c
	#printPuzzle(p, pl)
	#return getList(decode(p[r,c:findWordEnd(p[r,:],c)]), wlf)
	temp = findWordRangeH(p, r, c)
	gl = getList(decode(p[r,temp[0]:temp[1]]), wlf)
	count = 0
	for i in range(0, len(gl)):
		if gl[i-count] in pl:
			#print "removing", gl[i-count], r, c
			gl.pop(i-count)
			#print "removing", temp
			count += 1
	return gl

def findPossibleV(p, pl, r, c, wlf):
	#print "finding V", r, c
	#printPuzzle(p, pl)
	#return getList(decode(p[r:findWordEnd(p[:,c],r),c]), wlf)
	temp = findWordRangeV(p, r, c)
	gl = getList(decode(p[temp[0]:temp[1],c]), wlf)
	count = 0
	for i in range(0, len(gl)):
		if gl[i-count] in pl:
			#print "removing", gl[i-count], r, c
			temp = gl.pop(i-count)
			#print "removing", temp
			count += 1
	return gl

def makeNewPuzzle(n):
	p = numpy.zeros((n+2,n+2), dtype=int)
	p[0,:] = -1
	p[len(p)-1,:] = -1
	p[:,0] = -1
	p[:,len(p)-1] = -1
	pl = []
	return p, pl


if __name__ == "__main__":
	wordlist_f = sys.argv[1]

	#test = numpy.zeros((6,6), dtype=int)
	test = makeNewPuzzle(7)
	printPuzzle(test)
	print "possible h"
	print findPossibleH(test, 1, 1, wordlist_f)


	"""
	test = numpy.array(  [ [-1, 1, 2, 3, 4], [5, -1, 6, 7, 8], [10, 11, -1, 12, 13], [14, 15, 16, -1, 17], [18, 19, 20, 21, -1]  ] )
	test1 = numpy.array(  [ [-1, 1, 2, 3, 4], [5, -1, 6, 7, 8], [10, 11, -1, 12, 13], [14, 15, 16, -1, 17], [18, 19, 20, 21, -1]  ] )
	test2 = numpy.ones((7,7), dtype=int)*-1
	print test2[1,1:5]
	print test1[0,0:5]
	for i in range(1, 6):
		for j in range(1, 6):
			test2[i,j] = test1[i-1,j-1]
	printPuzzle(test2)
	#test = numpy.array( [ [2,3], [3,4] ] )
	#test = numpy.array( [ (3,4,2) , (5,3,2) ] )
	print test
	printPuzzle(test)
	print decode(test[0,:])
	print decode(test[:,0])
	print test[2,0:findWordEnd(test[2,:],0)]
	print findWordEnd(test[2,:],3)
	printPuzzle(test2)
	print test2[2,:]
	print test2[2,2]
	print findWordRange(test2[2,:], 2)
	print test2[2,:]
	print test2[2,0]
	print "flag"
	print findWordRangeH(test2, 2, 0)
	print test2[:,3]
	print test2[2,3]
	print findWordRangeV(test2, 2, 3)

	print decode(encode("test"))
	test = addWordH(test, "hi", 1, 2)
	test = addWordV(test, "hi", 0, 0)
	printPuzzle(test)
	print getList("^....$", wordlist_f)

	print decode([3,4,0,4,3,5,23])
	print encode("test")
	print decode(encode("test"))
	print findWordEnd([1,2,3,4,5,-1,4,5,6,7,8,9,-1,7,8,9,10], 0)
	print findWordEnd([1,2,3,4,5,-1,4,5,6,7,8,9,-1,7,8,9,10], 6)
	print findWordEnd([3,4,2,4,5],0)
	"""

	print findWordRangeH(test2, 2, 0)
	print test2[:,3]
	print test2[2,3]
	print findWordRangeV(test2, 2, 3)

	print decode(encode("test"))
	test = addWordH(test, "hi", 1, 2)
	test = addWordV(test, "hi", 0, 0)
	printPuzzle(test)
	print getList("^....$", wordlist_f)

	print decode([3,4,0,4,3,5,23])
	print encode("te