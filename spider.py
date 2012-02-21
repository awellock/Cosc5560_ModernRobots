import urllib2
import sys
from BeautifulSoup import *
from urlparse import urljoin

# Create a list of words to ignore
# Not exactly needed for what we're doing.
#ignorewords = set(['Penis', 'Banana'])

def crawl(self, pages, depth=2):
  for i in range(depth):
    newpages=set()
    for page in pages:
      try:
        c = urllib2.urlopen(page)
      except:
        print("Could not open %s" % page)
        continue
      soup = BeautifulSoup(c.read())
      self.addtoindex(page,soup)

      links = soup('a')
      for link in links:
        if('href' in dict(link.attrs)):
          url = urljoin(page,link['href'])
          if url.find("'")!=-1: continue
          url = url.split('#')[0]    # remove the location portion
          if url[0:4] == 'http' and not self.isindexed(url):
            newpages.add(url)
          linkText = self.gettextonly(link)
          self.addlinkref(page,url,linkText)

      self.dbcommit()

    pages = newpages

if __name__ == '__main__':
  site = 'http://localhost'
    if len(sys.argv) > 1:  
      site = sys.arvc[1]
  crawl() 
