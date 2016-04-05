#########
######### scraper.py
######### RateBeer.com scraping functionatliy
#########
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib
import re
import sys
import pdb

def urlToSoup(url, selenium = False):
	"""
	Given a url return soup object
	"""
	if selenium:
		browser = webdriver.Firefox()
		browser.get(url)
		soup = BeautifulSoup(browser.page_source, "html.parser")
		browser.close()
	else:
		htmlData = urllib.urlopen(url).read()
		soup = BeautifulSoup(htmlData, "html.parser")
	return soup

def convertURLs(urls, fn):
    """
    Convert a list of URLs given editing function `fn`
    return :: list of edited url strings
    """
    return [fn(url) for url in urls]

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

def getUserBeerURLs(beerListURL, userID):
    """
    Given user beer list url and id return
    target urls on this page
    return :: list of beer url strings
    extra  :: RateBeer specific fn
    """
    userID = str(userID)
    soup = urlToSoup(beerListURL, selenium = True) ## require selenium
    allURLs = soup.find_all("a", href = True)
    pattern = "(beer/.+" + userID + "/)"
    partialURLs = parse_bs4URLs(allURLs, key = 'href', pattern = pattern)
    fullURLs = convertURLs(partialURLs, constructTargetBeerURL)
    return fullURLs

def parse_bs4URLs(urls, key = 'href', pattern = "."):
    """
    Given list of BeautifulSoup urls and `key` attribute
    return : list of target url strings (possibly partial URL patterns)
    """
    goodURLs = []
    for url in urls:
        match = re.search(pattern, url[key])
        if match:
            goodURLs.append(match.group(0))
    return goodURLs



