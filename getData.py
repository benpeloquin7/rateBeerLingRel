#########
######### Gather data
#########
import scraper
import soupParser
import RateBeerHelpers as RBhelpers
import reviewData
import userPage
import csv
import numpy as np


np.random.seed(1786)
np.random.randint(1000)



#############
#############
#############
############# Scrape review and global for a single url
#############
#############
#############
id = "83882"
uPage = userPage.UserPage(id)
uPage.setAllFields()
beerURLs = uPage.getBeerList()

reviews_store = []
for url in beerURLs:
	print url
	soup = scraper.urlToSoup(url)
	r_data = reviewData.ReviewData()
	r_data.setAllReviewData(id, url, soup)
	d = r_data.outputToDict()
	d.update(uPage.outputToDict())
	reviews_store.append(d)	

keys = reviews_store[0].keys()
with open(id + '.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(reviews_store)





#############
#############
#############
############# Scrape User page info
#############
#############
#############
# id = "304719"
# url = "http://www.ratebeer.com/user/304719/"

# uPage = userPage.UserPage(id)
# uPage.setAllFields()
# print uPage.prettyPrint()


#############
#############
#############
############# Scrape review and global for a single url
#############
#############
#############
# user = "83882"
# beerListURL = scraper.constructBeerListURL(user)
# beerURLs = scraper.getUserBeerURLs(beerListURL, user)
# reviews_store = []
# for url in beerURLs:
# 	print url
# 	soup = scraper.urlToSoup(url)
# 	r_data = reviewData.ReviewData()
# 	r_data.setAllReviewData(user, url, soup)
# 	reviews_store.append(r_data.outputToDict())	

# keys = reviews_store[0].keys()
# with open(user + '.csv', 'wb') as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(reviews_store)



# badUserId = "12000"
# print scraper.getUserBeerURLs(scraper.constructBeerListURL(badUserId), badUserId)

## userPage scrape

## http://www.ratebeer.com/user/304719/




## 1) compile random list of user id's


## 2) for each user id - get beer list

	## if beer list < 5 skip
	## else get beer list

## 3) for each beer in beer list scrape beers, store in user.csv



#############
#############
#############
############# Scrape review and global for a single url
#############
#############
#############
# url = "http://www.ratebeer.com/beer/allagash-little-brett/385843/83882/"
# user = "83882"
# soup = scraper.urlToSoup(url)
# r_data = reviewData.ReviewData()
# r_data.setAllReviewData(user, url, soup)
# r_data.prettyPrint()

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

#############
#############
#############
############# Scrape review and global for a single url
#############
#############
#############
# user = "1786"
# url = "http://www.ratebeer.com/beer/parallel-49--cannery-gimme-shelter/409009/1786/"
# soup = scraper.urlToSoup(url)
# data =  soupParser.getBeerInfo(soup)
# id = user
# beerName = soupParser.removeNonAscii(data[0])
# ratingsBlob = soupParser.removeNonAscii(data[1])
# reviewBlob = soupParser.removeNonAscii(data[2])
# data =\
#     reviewData.ReviewData(userID = id,
#     beerName = beerName,
#     ratings = ratingsBlob,
#     review = reviewBlob)
# data.setReviewData()
# data.setBeerGlobalInfo(soupParser.getBeerGlobalInfo(soup))
# data.prettyPrint()




#############
#############
#############
############# Scrape multiple users
#############
#############
#############
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
