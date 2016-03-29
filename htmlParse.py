## for processing html (looking at Beautiful Soup documentation)
from bs4 import BeautifulSoup
import urllib
import re

html1 = "http://www.ratebeer.com/beer/de-molen--hair-of-the-dog-fred/369740/1786/"
html2 = "http://www.ratebeer.com/beer/ridge-ay-caramba-jalapeno-ipa/405866/1786/"
html3 = "http://www.ratebeer.com/beer/skookum-murder-of-crows/176960/1786/"
r = urllib.urlopen(html3).read()
soup = BeautifulSoup(r, "html.parser")
#letters = soup.find_all("div", class_ = "curvy")
#print letters[0]
#print soup.prettify()
#letters2 = soup.find("div", class_ = "curvy")

#print letters[0].get_text()


## children of curvy div
curvy = soup.find_all("div", class_ = "curvy")
#curvy = soup.find(string=re.compile("background: #ffffdd;"))
print type(curvy)

for r in curvy:
    print "==========="
    currAttributes = r.attrs['style']
    print re.search("background: #ffffdd;", currAttributes) != None

#print re.findall("#ffffdd;", r)
#children = curvy.findChildren()
#for child in children:
#    print "================="
#    print child
