#!/usr/bin/python

import sys
import urllib2
import re

linkRegex = re.compile('<a\shref=[\'|\"](.*?)[\'|\"].*?/>')
wordRegex = re.compile('>.*?\s([a-zA-Z]*)\s.*?<')
words = set([])

try:
	toCrawlList = open('toCrawl.txt', 'r')
	toCrawl = set(toCrawlList.readlines())
	toCrawlList.close()
except IOError:
	toCrawl = set(['http://crosswordcorner.blogspot.com/'])

for i in toCrawl:
	print 'To Crawl: ' + i

try:
	crawledList = open('crawled.txt', 'r')
	crawled = set(crawledList.readlines())
	crawledList.close()
except IOError:
	crawled = set([])

for i in crawled:
	print 'Crawled: ' + i


print 'start'

for y in range(10000):
	for x in range(1):
		try:
			crawl = toCrawl.pop()
			crawled.add(crawl)
		except KeyError:
			raise StopIteration
	
		try:
			page = urllib2.urlopen(crawl)
		except:
			continue
	
		page = page.read()
		link = re.findall(linkRegex, page)
		
		for i in link:
			toCrawl.add(i)
			
		word = re.findall(wordRegex, page)
		
		for i in word:
			if len(i) > 2:
				words.add(i.lower())
	
	wordsFile = open('words' + str(y) + '.txt', 'w')
	for i in words:
		wordsFile.write(i + '\n')
	wordsFile.close()

	toCrawlList = open('toCrawl.txt', 'w')
	for i in toCrawl:
		toCrawlList.write(i + '\n')
	toCrawlList.close()

	crawledList = open('crawled.txt', 'w')
	for i in crawled:
		crawledList.write(i +'\n')
	crawledList.close()
	
	print y
	
	
print 'completed'
