#############
#############
#############
############# Practice scrape of 100 users
#############
#############
#############
import reviewData
import scraper
from RateBeerHelpers import LOWEST_USER_ID, HIGHEST_USER_ID
import random
import csv

random.seed(100)
n = 100
userIDs = random.sample(range(LOWEST_USER_ID, HIGHEST_USER_ID), n)

badIDsList = []

for userID in userIDs:
	userID = str(userID)
	beerListURL = scraper.constructBeerListURL(userID)
	beerURLs = scraper.getUserBeerURLs(beerListURL, userID)

	## only take reviewers with over 5 beers
	if len(beerURLs) < 5:
		badIDsList.append(userID)
		continue
	
	reviews_store = []
	for url in beerURLs:
		print url
		soup = scraper.urlToSoup(url)
		r_data = reviewData.ReviewData()
		r_data.setAllReviewData(userID, url, soup)
		reviews_store.append(r_data.outputToDict())	

	scraper.createUserCSV(userID, reviews_store, "data/")

with open('data/badUserIds.txt', 'wb') as output_file:
	for id in badIDsList:
		output_file.write(str(id) + ',')

