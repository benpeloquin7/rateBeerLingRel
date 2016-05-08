import reviewData
import scraper
import soupParser
import userPage
from RateBeerHelpers import LOWEST_USER_ID, HIGHEST_USER_ID
import os
import pdb
import re
import time
import random
import csv
from collections import defaultdict


RATE_LIMIT_VALUE = 20
RATE_LIMIT_PAUSE_TIME = 40


#################################################
####### Helpers
#######
def increment_counter(i, stop_value, stop_rate):
	time.sleep(3)
	if i % stop_value == 0:
		print "i: ", i
		print "sleeping for ", stop_rate, " seconds..."
		time.sleep(stop_rate)
	return i + 1

def review_list_to_csv(path, data):
	keys = data[0].keys()
	with open(path + '.csv', 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(data)

#################################################
####### Set-up
#######

## Get all the users we've already scraped
reviews_store_path = '../data/reviews_store/'
pattern = "([0-9]+).csv"
already_scraped_users = set([re.findall(pattern, user)[0] for user in os.listdir(reviews_store_path)])
## Get all 'good' users (with 1 or more reviews)
good_users_path = '../data/good.csv'
users = []
with open(good_users_path, 'r') as input:
	reader = csv.reader(input, delimiter = ',')
	for row in reader:
		users.append(row[0])


#################################################
####### Get data
#######

i = 0 # Avoid rate-limits

## Iterate over users
for id in users:
	if id in already_scraped_users:
		i += 1
		print "already seen user ", id, "!!!!"
		continue
	print "=============="
	print "user id: ", id
	uPage = userPage.UserPage(id)
	uPage.setAllFields()
	user_data = uPage.outputToDict()
	user_reviews = []

	## Iterate over (up to 50) user beers
	for beer_url in uPage.getBeerList():
		print '\t' + beer_url
		data_store = dict()
		data_store = user_data.copy()
		r_data = reviewData.ReviewData()
		r_data.setAllReviewData(id, beer_url)
		i = increment_counter(i, RATE_LIMIT_VALUE, RATE_LIMIT_PAUSE_TIME)
		data_store.update(r_data.outputToDict())
		user_reviews.append(data_store)

	## Write to csv
	print "writing to csv..."
	print '=================='
	path = reviews_store_path + id
	review_list_to_csv(path, user_reviews)
	


## Run data
# random.seed(1)
# numIDs = 1000
# RATE_LIMIT_VALUE = 30
# RATE_LIMIT_PAUSE_TIME = 30
# goodIDs = []
# badIDs = []

# userIDs = random.sample(range(LOWEST_USER_ID, HIGHEST_USER_ID), 30)
# userIDs.append("1786")
# for i, userID in enumerate(userIDs):
# 	print i
# 	uPage = userPage.UserPage(userID)
# 	uPage.setUrl()
# 	uPage.setBeerList()
# 	beerURLs = uPage.getBeerList()
# 	## only take reviewers with 3 or more
# 	if len(beerURLs) > 0:
# 		goodIDs.append((userID, len(beerURLs)))
# 	else: badIDs.append(userID)

# 	if i % RATE_LIMIT_VALUE == 0:
# 		time.sleep(RATE_LIMIT_PAUSE_TIME)

# # Data logging
# path = 'data/'
# if not os.path.exists(path):
# 	os.makedirs(path)

# ## Save good Ids and number
# with open(path + 'good.csv','a') as out:
#     csv_out = csv.writer(out)
#     for row in goodIDs:
#         csv_out.writerow(row)

# ## Save good Ids and number
# with open(path + 'bad.csv', 'a') as out:
# 	csv_out = csv.writer(out)
# 	for row in badIDs:
# 		csv_out.writerow(row)

