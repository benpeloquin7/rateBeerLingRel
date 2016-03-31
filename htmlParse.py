from bs4 import BeautifulSoup
import urllib
import re
import sys
import pdb

## example urls
html1 = "http://www.ratebeer.com/beer/de-molen--hair-of-the-dog-fred/369740/1786/"
html2 = "http://www.ratebeer.com/beer/ridge-ay-caramba-jalapeno-ipa/405866/1786/"
html3 = "http://www.ratebeer.com/beer/skookum-murder-of-crows/176960/1786/"

## set-up
def getTitle(soup):
    """
    return :: beer name
    """
    return soup.find("h1").get_text()

def getScores(soup):
    """
    RateBeer.com places target user reviews in class = 'curvy'
    returns :: string of individual scores or empty string
    """
    userPattern = "background: #ffffdd;" # identify our user
    curvy = soup.find_all("div", class_ = "curvy")
    for r in curvy:
        if "style" in r.attrs and\
                re.search(userPattern, r.attrs["style"]):
            return r.get_text()
    return ""

def targetDiv(div, pattern, attr):
    currAttr = div.attrs
    return currAttr and\
        attr in currAttr.keys() and\
        re.search(pattern, currAttr[attr]) != None

def getReviewText(soup):
    """
    return :: string review text for target user review
    """
    paddingPattern = "padding: 20px 10px 0px 0px; line-height: 1.5;" # from manual inspection
    allDivs = soup.find_all("div")
    for div in allDivs:
        if targetDiv(div, paddingPattern, "style"):
            return div.get_text()

    return ""


#    paddingPattern = "padding: 20px 10px 0px 0px; line-height: 1.5;" # from manual inspection
#    allDivs = soup.find_all("div")
#                
#    reviewText = ""
#    for div in allDivs:
#        currAttr = div.attrs
#        if "style" in currAttr.keys() and\
#                re.search(paddingPattern, currAttr['style']) != None:
#            reviewText = div.get_text()


r = urllib.urlopen(html1).read()
soup = BeautifulSoup(r, "html.parser")
print getTitle(soup)
print getScores(soup)
print getReviewText(soup)



####
#### 1) extract name of review
####
#h1Text = soup.find("h1").get_text()


####
#### 2) extract individual scores
####
#userPattern = "background: #ffffdd;" # identify our user
#scores = ''
#for r in curvy:
#    if "style" in r.attrs and\
#            re.search(userPattern, r.attrs["style"]):
#        scores = r.get_text()

####
#### 3) extract review text
####

## current data
#data = (h1Text, scores, reviewText) 
#print data


