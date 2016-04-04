#########
######### Gather data
#########


import beerData
import userBeerList
import csv


def removeNonAscii(s):
    return ''.join([i if ord(i) < 128 else ''\
                        for i in s])

user = 1786

beerList = userBeerList.constructBeerListURL(user)
urls = [userBeerList.constructTargetBeerURL(url)\
    for url in userBeerList.getUserBeerURLs(beerList, user)]

dataHold = []

for url in urls:
    soup = beerData.urlToSoup(url)
    data = beerData.getBeerInfo(soup)
    #print "--------"
    #print data
    dataDict = {"user":user,\
                    "beerName":removeNonAscii(data[0]),\
                    "ratings":removeNonAscii(data[1]),\
                    "review":removeNonAscii(data[2])}
    dataHold.append(dataDict)

    
keys = dataHold[0].keys()
with open('rateBeerData.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(dataHold)

