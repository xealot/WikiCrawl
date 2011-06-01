#!/usr/bin/env python
# encoding: utf-8

import cgi
import sys
import os
import wikitest
import urllib

def main():
	paths = wikitest.crawl('http://en.wikipedia.org/wiki/' + urllib.quote(sys.argv[1]))
	print paths


if __name__ == '__main__':
	main()
