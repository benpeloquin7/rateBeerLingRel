import time
import scraper
import userPage
import os
from RateBeerHelpers import LOWEST_USER_ID, HIGHEST_USER_ID
import time
import random
import csv
from collections import defaultdict

## Run data
random.seed(2)
numIDs = 100
RATE_LIMIT_VALUE = 30
RATE_LIMIT_PAUSE_TIME = 1
goodIDs = []
badIDs = []

## Store IDs that have been seen
seenIDs = set()
## Get seen good IDs
with open('data/good.csv') as infile:
	reader = csv.reader(infile)
	for rows in reader:
		seenIDs.add(rows[0])
## Get seen bad IDs
with open('data/bad.csv') as infile:
	reader = csv.reader(infile)
	for rows in reader:
		seenIDs.add(rows[0])
print len(seenIDs)
print seenIDs

# Convert IDs to strings
userIDs = [str(id) for id in random.sample(range(LOWEST_USER_ID, HIGHEST_USER_ID), numIDs)]
for i, userID in enumerate(userIDs):
	## Skip seen IDs
	print i
	if userID in seenIDs:
		print "SEEN THIS ID!!!: ", userID
		continue
	
	uPage = userPage.UserPage(userID)
	uPage.setUrl()
	uPage.setBeerList()
	beerURLs = uPage.getBeerList()
	
	## only take reviewers with 3 or more
	if len(beerURLs) > 0: goodIDs.append((userID, len(beerURLs)))
	else: badIDs.append(userID)

	if i % RATE_LIMIT_VALUE == 0:
		time.sleep(RATE_LIMIT_PAUSE_TIME)

# Data logging
path = 'data/'
if not os.path.exists(path):
	os.makedirs(path)

## Save good Ids and number
with open(path + 'good.csv','a') as out:
    csv_out = csv.writer(out)
    for row in goodIDs:
        csv_out.writerow(row)

## Save good Ids and number
with open(path + 'bad.csv', 'a') as out:
	csv_out = csv.writer(out)
	for row in badIDs:
		csv_out.writerow([row])