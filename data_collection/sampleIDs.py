import time
import scraper
import userPage
import os
from RateBeerHelpers import LOWEST_USER_ID, HIGHEST_USER_ID
import time
import random
import csv
from collections import defaultdict

########
#### NOTE: got rate limited at pause time 30 ,rate_limit_value 20
####


## Seed from 

## Run data
# set seed 7 at 4/19/2016 start time 9:52pm
####

random.seed(8)
NUM_IDS = 50000
RATE_LIMIT_VALUE = 20
RATE_LIMIT_PAUSE_TIME = 40
goodIDs = []
badIDs = []
path = 'data/'

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

# Convert IDs to strings
userIDs = [str(id) for id in random.sample(range(LOWEST_USER_ID, HIGHEST_USER_ID), NUM_IDS)]
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
	
	## only take reviewers with 1 or more
	if len(beerURLs) > 0: goodIDs.append((userID, len(beerURLs)))
	else: badIDs.append(userID)

	if i % RATE_LIMIT_VALUE == 0:
		## Interim data logging
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
		goodIDs = []
		badIDs = []
		time.sleep(RATE_LIMIT_PAUSE_TIME)

# Data logging
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