#########
######### Gather data
#########
import scraper
import soupParser
import RateBeerHelpers as RBhelpers
import reviewData
import csv
import numpy as np


np.random.seed(1786)
np.random.randint(1000)


## Get beer global information
# url = "http://www.ratebeer.com/beer/beerbliotek-imperial-mocha-latte-stout/296801/5011/"
# url2 = "http://www.ratebeer.com/beer/mikkeller-ramen-to-biiru/381088/345852/"

# soup = scraper.urlToSoup(url)
# print soupParser.getBeerGlobalScore(soup)
# print soupParser.getBeerGlobalStyleScore(soup)
# print soupParser.getBeerBrewer(soup)
# print soupParser.getBeerStyle(soup)
# print soupParser.getBeerCountry(soup)
# print soupParser.getBeerNumRatings(soup)
# print soupParser.getBeerWeightedAvg(soup)
# print soupParser.getBeerCalories(soup)
# print soupParser.getBeerABV(soup)
# print soupParser.getBeerGlobalInfo(soup)


user = "1786"
url = "http://www.ratebeer.com/beer/parallel-49--cannery-gimme-shelter/409009/1786/"
soup = scraper.urlToSoup(url)
data =  soupParser.getBeerInfo(soup)
id = user
beerName = soupParser.removeNonAscii(data[0])
ratingsBlob = soupParser.removeNonAscii(data[1])
reviewBlob = soupParser.removeNonAscii(data[2])
data =\
    reviewData.ReviewData(userID = id,
    beerName = beerName,
    ratings = ratingsBlob,
    review = reviewBlob)
data.setReviewData()
data.setBeerGlobalInfo(soupParser.getBeerGlobalInfo(soup))
data.prettyPrint()
# data.setData()
# data.prettyPrint()

# users = scraper.getUserIds(RBhelpers.TOP_RATERS_URL)

# dataHold = []

# for user in users[0:2]:
#     beerListURL = scraper.constructBeerListURL(user)
#     beerURLs = scraper.getUserBeerURLs(beerListURL, user)
#     for url in beerURLs:
#         soup = scraper.urlToSoup(url)
#         data =  soupParser.getBeerInfo(soup)
#         id = user
#         beerName = soupParser.removeNonAscii(data[0])
#         ratingsBlob = soupParser.removeNonAscii(data[1])
#         reviewBlob = soupParser.removeNonAscii(data[2])
#         data =\
#             reviewData.ReviewData(userID = id,
#             beerName = beerName,
#             ratings = ratingsBlob,
#             review = reviewBlob)
#         # dataDict = {"user":user,\
#         #         "beerName":removeNonAscii(data[0]),\
#         #         "ratings":removeNonAscii(data[1]),\
#         #         "review":removeNonAscii(data[2])}
#         dataHold.append(data)
        
# for i in range(len(dataHold)):
#     print dataHold[i].prettyPrint()

# for i in range(len(dataHold)):
#     print type(i)
## practice with a single user
# user = str(1786)
# beerListURL = scraper.constructBeerListURL(user)
# beerURLs = scraper.getUserBeerURLs(beerListURL, user)

# dataHold = []
# for url in beerURLs:
#     soup = scraper.urlToSoup(url)
#     data = soupParser.getBeerInfo(soup)
#     dataDict = {"user":user,\
#                 "beerName":removeNonAscii(data[0]),\
#                 "ratings":removeNonAscii(data[1]),\
#                 "review":removeNonAscii(data[2])}
#     dataHold.append(dataDict)
# for i in [1, 2, 3]:
#     print dataHold[i]
