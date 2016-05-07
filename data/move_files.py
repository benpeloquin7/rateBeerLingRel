import os
import csv

## Currently in dir data/
path = '../missingOverallScores.csv'

users = []
with open(path, 'r') as input:
	reader = csv.reader(input, delimiter = ',')
	for row in reader:
		users.append(row[1])

users = users[2:]
for user in users:
	old_path = 'reviews_store/' + user + '.csv'
	new_path = 'temp_store/' + user + '.csv'
	os.rename(old_path, new_path)
