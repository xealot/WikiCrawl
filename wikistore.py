#!/usr/bin/env python
# encoding: utf-8

import cgi
import sys
import os
import pickle
import wikitest
import urllib
from pprint import pprint

def main():
    try:
        wiki_terms = pickle.load(open('wiki.terms', 'r'))
    except:
        wiki_terms = {}
    #pprint(wiki_terms)
    #return
    
    #paths = wikitest.crawl('http://en.wikipedia.org/wiki/' + urllib.quote(sys.argv[1]), terms=wiki_terms)
    paths = wikitest.crawl(sys.argv[1], terms=wiki_terms)
    print paths
    for i in xrange(len(paths) - 1):
        wiki_terms[paths[i].url] = {'title': paths[i].title, 'next': paths[i+1]._asdict()}
    if len(paths) > 0:
        if paths[-1].url not in wiki_terms:
            wiki_terms[paths[-1].url] = {'title': paths[-1].title, 'next': None}
    pickle.dump(wiki_terms, open('wiki.terms', 'w'))

if __name__ == '__main__':
	main()
