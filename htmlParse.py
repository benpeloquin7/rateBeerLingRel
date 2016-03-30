from bs4 import BeautifulSoup
import urllib
import re

## example urls
html1 = "http://www.ratebeer.com/beer/de-molen--hair-of-the-dog-fred/369740/1786/"
html2 = "http://www.ratebeer.com/beer/ridge-ay-caramba-jalapeno-ipa/405866/1786/"
html3 = "http://www.ratebeer.com/beer/skookum-murder-of-crows/176960/1786/"


## set-up
r = urllib.urlopen(html1).read()
soup = BeautifulSoup(r, "html.parser")

## children of curvy div
curvy = soup.find_all("div", class_ = "curvy")

####
#### 1) extract name of review
####
h1Text = soup.find("h1").get_text()


####
#### 2) extract individual scores
####
userPattern = "background: #ffffdd;" # identify our user
scores = ''
for r in curvy:
    if "style" in r.attrs and\
            re.search(userPattern, r.attrs["style"]):
        scores = r.get_text()

####
#### 3) extract review text
####
paddingPattern = "padding: 20px 10px 0px 0px; line-height: 1.5;" # from manual inspection
allDivs = soup.find_all("div")
reviewText = ""
for div in allDivs:
    currAttr = div.attrs
    if "style" in currAttr.keys() and\
            re.search(paddingPattern, currAttr['style']) != None:
        reviewText = div.get_text()


## current data
print h1Text
print scores
print reviewText
