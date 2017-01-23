#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#收集一个website下的所有链接
__author__ = "caster"

from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
class LinkParser(HTMLParser):

    # This is a function that HTMLParser normally has
    # but we are adding some functionality to it
    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    # We are grabbing the new URL. We are also adding the
                    # base URL to it. For example:
                    # www.netinstructions.com is the base and
                    # somepage.html is the new URL (a relative URL)
                    #
                    # We combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # www.netinstructions.com/somepage.html
                    newUrl = parse.urljoin(self.baseUrl, value)
                    # And add it to our colection of links:
                    if newUrl not in self.links:
                        self.links = self.links + [newUrl]

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url):
        self.links = []
        # Remember the base URL which will be important when creating
        # absolute URLs
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        if response.getheader('Content-Type').find('text/html') > -1:
            htmlBytes = response.read()
            # Note that feed() handles Strings well, but not bytes
            # (A change from Python 2.x to Python 3.x)
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return self.links
        else:
            return []

def collectingallURLS(url):
	parse = LinkParser()
	URLScrawled  = []
	URLstocrawl = [url]
	numberVisited = 0

	while URLstocrawl != [] and numberVisited < 10000:
		try:
			numberVisited += 1
			print("Visiting: ",numberVisited," ",URLstocrawl[0])
			for link in parse.getLinks(URLstocrawl[0]):
				if link not in URLstocrawl and link not in URLScrawled:
					URLstocrawl += [link] 
		except:
			print("Failed!")
		URLScrawled += [URLstocrawl[0]]
		URLstocrawl = URLstocrawl[1:]

	with open('all_URLs','wt') as textfile: 
		for line in URLScrawled: 
			print(line,file=textfile)		

if __name__ == '__main__':
	collectingallURLS("http://www.baojiayin.com/")
