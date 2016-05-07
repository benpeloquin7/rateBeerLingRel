#############
#############
#############
############# Practice scrape of 100 users
#############
#############
#############
import reviewData
import userPage
import scraper
from RateBeerHelpers import LOWEST_USER_ID, HIGHEST_USER_ID
import random
import csv

random.seed(500)
n = 500
userIDs = random.sample(range(LOWEST_USER_ID, HIGHEST_USER_ID), n)

badIDsList = []
for userID in userIDs:
	uPage = userPage.UserPage(userID)
	uPage.setAllFields()
	beerURLs = beerURLs = uPage.getBeerList()

	## only take reviewers with over 5 beers
	if len(beerURLs) < 3:
		badIDsList.append(userID)
		continue
	
	reviews_store = []
	for url in beerURLs:
		print url
		soup = scraper.urlToSoup(url)
		r_data = reviewData.ReviewData()
		r_data.setAllReviewData(userID, url, soup)
		d = r_data.outputToDict()
		d.update(uPage.outputToDict())
		reviews_store.append(d)	

	scraper.createUserCSV(userID, reviews_store, "data/")

with open('data/badUserIds2.txt', 'wb') as output_file:
	for id in badIDsList:
		output_file.write(str(id) + ',')

