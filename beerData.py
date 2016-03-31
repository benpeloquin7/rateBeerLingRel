#########
######### Given a beer review page with a target user
######### extract (title, scores, review_text)
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
    return :: title, scores, and review text
    """
    return [getTitle(soup), getScores(soup), getReviewText(soup)]

def main():
    ## example URLs for rater id 1786
    html1 = "http://www.ratebeer.com/beer/de-molen--hair-of-the-dog-fred/369740/1786/"
    html2 = "http://www.ratebeer.com/beer/ridge-ay-caramba-jalapeno-ipa/405866/1786/"
    html3 = "http://www.ratebeer.com/beer/skookum-murder-of-crows/176960/1786/"
    urls = sys.argv[1:] if len(sys.argv) > 1 else [html1]

    for url in urls:
        print "---------------------"
        print "====================="
        print "Currently scraping title, scores and review text for: \n" + url + "\n"
        r = urllib.urlopen(url).read()
        soup = BeautifulSoup(r, "html.parser")
        print getBeerInfo(soup)

if __name__ == "__main__":
    main()
