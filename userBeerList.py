from bs4 import BeautifulSoup
import urllib
import re
import sys


def userBeerList(id):
    userBeerListPage = "http://www.ratebeer.com/user/" + userId + "/"
    r = urllib.urlopen(userBeerListPage).read()
    return BeautifulSoup(r, "html.parser")

def getBeerUrls(soup):
    table = soup.find("table", {"class" : "table"})


def main():
    userId = sys.argv[1]

if __name__ == "__main__":
    main()
