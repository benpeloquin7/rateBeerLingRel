## for processing html (looking at Beautiful Soup documentation)
from bs4 import BeautifulSoup
import urllib
import re

html1 = "http://www.ratebeer.com/beer/de-molen--hair-of-the-dog-fred/369740/1786/"

r = urllib.urlopen(html1).read()
soup = BeautifulSoup(r)
letters = soup.find_all("div", class_ = "curvy")
#print letters[0]
#print soup.prettify()
print soup.get_text()

