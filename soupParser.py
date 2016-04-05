#########
######### soupParser.py
######### RateBeer.com BS4 soup parsing functionatliy
#########
from bs4 import BeautifulSoup
import urllib
import re
import sys

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
