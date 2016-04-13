#########
######### soupParser.py
######### RateBeer.com BS4 soup parsing functionatliy
#########
from bs4 import BeautifulSoup
import urllib
import re
import sys
import pdb

## -------------------------------
## Cleaning / helpers
## ===============================
def removeNonAscii(s):
    if not isinstance(s, basestring): return s
    return ''.join([i if ord(i) < 128 else ''\
                for i in s])

## -------------------------------
## Primary data extractionq
## ===============================
def getTitle(soup):
    """
    Extract beer title
    return :: string beer name
    """
    return soup.find("h1").get_text()

def getScores(soup):
    """
    Get individual attribute scores
    (RateBeer.com places target user reviews in class = 'curvy')
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
    """
    return :: boolean check if we have target div
    """
    currAttr = div.attrs
    return currAttr and\
        attr in currAttr.keys() and\
        re.search(pattern, currAttr[attr]) != None


def getReviewText(soup):
    """
    Extract review text
    return :: string review text for target user review
    """
    paddingPattern = "padding: 20px 10px 0px 0px; line-height: 1.5;" # from manual inspection
    allDivs = soup.find_all("div")
    for div in allDivs:
        if targetDiv(div, paddingPattern, "style"):
            return div.get_text()

    return ""

def getBeerInfo(soup):
    """
    Primary soup parsing functionality, collects all data we'd like
    return :: title, scores, and review text
    """
    return [getTitle(soup), getScores(soup), getReviewText(soup)]

def getAllLinks(soup):
	allURLs = soup.find_all("a", href = True)
	return allURLs


## -------------------------------
## Beer page global information
## ===============================

def getBeerGlobalScore(soup):
    """
    Given a beer page soup (likely from a urlToSoup call)
    return :: beers global score
    """
    # pdb.set_trace()
    scorePattern1 = "font-size: 48px; font-weight: bold; color: #fff; padding: 7px 10px;"
    currDiv = soup.find_all('div', style = scorePattern1)
    if currDiv == []: return None ## If score is empty return None

    divAttrs = currDiv[0].attrs
    scorePattern2 = "^([1-9]+\.[0-9]*): This figure represents"
    if "title" in divAttrs.keys():
        currSearch = re.search(scorePattern2, divAttrs["title"])
    return currSearch.group(1) if currSearch != None else None

def getBeerGlobalStyleScore(soup):
    """
    Given a beer page soup (likely from a urlToSoup call)
    return :: beers global score
    """
    scorePattern1 = "background-color: #66A212; position: relative; left: 0px; top: -20px; width: 67px; height: 67px; border-radius: 67px; z-index: -1;text-align: center;"
    currDiv = soup.find_all('div', style = scorePattern1)
    if currDiv == []: return None ## If score is empty return None

    divAttrs = currDiv[0].attrs
    scorePattern2 = "^([1-9]+\.[0-9]*): This figure represents"
    if "title" in divAttrs.keys():
        currSearch = re.search(scorePattern2, divAttrs["title"])
    return currSearch.group(1) if currSearch != None else None

def getBeerBrewer(soup):
    """
    Given a beer page soup (likely from a urlToSoup call)
    return :: beer's brewer (brand)
    """
    target = soup.find_all('a', id = '_brand4')[0]
    return target.get_text()

def getBeerStyle(soup):
    """
    Given a beer page soup (likely from a urlToSoup call)
    return :: beer's style
    """
    target = soup.find_all('a', href = re.compile("/beerstyles/.+"))[0]
    return target.get_text()
    
def getBeerCountry(soup):
    """
    Given a beer page soup (likely from a urlToSoup call)
    return :: beer's country
    """
    target = soup.find_all('div', style = "padding-bottom: 7px; line-height: 1.5;")[0]
    pattern = ".+,\s([A-Z]\w+)\s"
    for t in target:
        currSearch = re.search(pattern, t.get_text())
        if currSearch != None:
            return currSearch.group(1)
    return None

def getBeerNumRatings(soup):
    """
    Given a beer page soup (likely from a urlToSoup call)
    return :: number of ratings for this beer
    """
    target = soup.find_all('span', id = "_ratingCount8")[0].get_text()
    return target

def getBeerWeightedAvg(soup):
    """
    Given a beer page soup (likely from a urlToSoup call)
    return :: number of ratings for this beer
    """
    target = soup.find_all('a', title = re.compile("The weighted average,.+"))[0]
    pattern = "The weighted average,\s([0-9]+\.[0-9]*).+"
    avg = re.search(pattern, target['title']).group(1)
    return avg
    
def getBeerCalories(soup):
    """
    Given a beer page soup (likely from a urlToSoup call)
    return :: number of colories
    """
    target = soup.find_all('big', style = "color: #777;")
    pattern = "^([1-9][0-9]{1,3}[^%])$"
    for t in target:
        currSearch = re.search(pattern, t.get_text())
        if currSearch != None:
            return currSearch.group(1)
    # return target

def getBeerABV(soup):
    """
    Given a beer page soup (likely from a urlToSoup call)
    return :: abv for this beer
    """
    target = soup.find_all('big', style = "color: #777;")
    pattern = "^([0-9][0-9]?(?:\.[0-9])?%)$"
    for t in target:
        currSearch = re.search(pattern, t.get_text())
        if currSearch != None:
            return currSearch.group(1)

def getBeerGlobalInfo(soup):
    """
    Given a beer page soup (likely from a urlToSoup call)
    return :: list of global info
    """
    return [getBeerGlobalScore(soup), getBeerGlobalStyleScore(soup),\
            getBeerBrewer(soup), getBeerStyle(soup), getBeerCountry(soup),\
            getBeerNumRatings(soup), getBeerWeightedAvg(soup), getBeerCalories(soup),\
            getBeerABV(soup)]