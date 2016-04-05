#########
######### Given a user beer listing page on RateBeer.com
######### Return a list of all beer review urls on that page
######### (Currently using selenium which forces Firefox browser pop-up)
#########
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib
import re
import sys
import pdb


def constructBeerListURL(userID):
    """
    Given user ID get list of 50 beers
    return :: url string
    """
    return  "http://www.ratebeer.com/user/" + str(userID) + "/beer-ratings/"

def constructTargetBeerURL(partialURL):
    """
    Given a partial URL return full url pointing at beer page 
    (with target user review first)
    return :: url string
    """
    return "http://www.ratebeer.com/" + partialURL
    
def convertURLs(urls, fn):
    """
    Convert a list of URLs given editing function `fn`
    return :: list of edited url strings
    """
    return [fn(url) for url in urls]

def getUserBeerURLs(beerListURL, userID):
    """
    Given user beer list url and id return
    target urls on this page
    return :: list of beer url strings
    """
    userID = str(userID)
   
    ## need selenium here because js script
    ## populates user beer list
    browser = webdriver.Firefox()
    browser.get(beerListURL)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    allURLs = soup.find_all("a", href = True)
    pattern = "(beer/.+" + userID + "/)"
    targetURLs = getTargetURLs(allURLs,  pattern)
    browser.close()

    return targetURLs
    
def getTargetURLs(urls, pattern):
    """
    Given list of urls, add regex pattern get target urls
    return : list of target url strings
    """
    goodURLs = []
    for url in urls:
        match = re.search(pattern, url['href'])
        if match:
            goodURLs.append(match.group(0))
    return goodURLs


def main():
    userID = sys.argv[1] if len(sys.argv) > 1 else "1786"
    beerListPage = constructBeerListURL(userID)
    print beerListPage
    beerURLs = getUserBeerURLs(beerListPage, userID)
    convertedURLs = convertURLs(beerURLs, constructTargetBeerURL)
    print convertedURLs

if __name__ == "__main__":
    main()
