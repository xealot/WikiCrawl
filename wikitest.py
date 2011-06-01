"""
Not italicized, not in parens.
"""

import urllib2, re, sys
from collections import namedtuple
from itertools import chain
from BeautifulSoup import BeautifulSoup

Article = namedtuple('WikiArticle', 'url title')

max_hops = 50
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.71 Safari/534.24'
#starting_url = 'http://en.wikipedia.org/wiki/Special:Random'
stop_url = 'http://en.wikipedia.org/wiki/Philosophy'


def crawl(current, terms=None):
    count = 0
    hits = []
    
    while True:
        if count >= max_hops:
            print 'Maximum Hops Reached'
            break
        if terms is not None and current in terms:
            print 'FOUND KNOWN TERM', current
            hits.append(Article(current, terms[current]['title']))
            break
        if current == stop_url:
            print current
            print 'FOUND PHILOSOPHY'
            print len(hits)
            hits.append(Article(current, 'Philosophy'))
            print len(hits)
            break
        
        print 'Trying: %s' % current
    
        try:
            request = urllib2.Request(current, headers={'User-Agent': user_agent})
            response = urllib2.urlopen(request, timeout=10)
        except urllib2.HTTPError as e:
            print str(e)
            break
        html = response.read()
    
        soup = BeautifulSoup(html)
        title = soup.find('h1', id='firstHeading')
        hits.append(Article(current, title and title.text or None))
        
        #Remove Shit
        for shit in chain(soup.findAll('i'), soup.findAll('table')):
            shit.extract()

        anchor = None
        for paragraph in chain(soup.findAll('p'), soup.findAll('li')):
            #Kill params
            non_paren = ''
            paren_count = 0
            skip = False
            for i in ''.join(str(paragraph)):
                if i == '<':
                    skip = True
                if i == '>':
                    skip = False
                if skip is False:
                    if i == '(':
                        paren_count += 1
                    if i == ')':
                        paren_count -= 1
                        continue
                if paren_count == 0:
                    non_paren += i
            soup2 = BeautifulSoup(non_paren)
            anchor = soup2.find('a', href=re.compile('^/wiki/[^\:]+$'))
            if anchor:
                current = 'http://en.wikipedia.org' + dict(anchor.attrs)['href']
                break
        if anchor is None:
            print 'Could not find trail from %s' % current
        count += 1
    return hits

if __name__ == '__main__':
    hits = crawl(sys.argv[1] if len(sys.argv) > 1 else 'http://en.wikipedia.org/wiki/Special:Random')
    print hits
    