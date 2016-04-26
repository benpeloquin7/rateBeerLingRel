import re
import pprint
import pdb
import soupParser
import scraper
from bs4 import BeautifulSoup

class UserPage():
	def __init__(self, id):
		self.userID = id 
		self.url = None
		self.soup = None
		self.beerList = None
		self.userName = None
		self.numRatings = None
		self.numPlaces = None
		self.numBreweries = None
		self.numCountries = None
		self.numStyles = None
		self.numFollowing = None
		self.numFriends = None
		self.profileBio = None

	def setAllFields(self):
		self.setUrl()
		self.setSoup()
		self.setBeerList()
		self.setUserName()
		self.setNumRatings()
		self.setNumPlaces()
		self.setNumBreweries()
		self.setNumCountries()
		self.setNumStyles()
		self.setNumFollowing()
		self.setNumFriends()
		self.setProfileBio()
		## run cleaning
		self.cleanAllData()

	def setUrl(self):
		self.url = scraper.constructBeerListURL(self.userID)
	def getUrl(self):
		return self.url
	def setSoup(self):
		self.soup = scraper.urlToSoup(self.url)
	def getSoup(self):
		return self.soup
	def setBeerList(self):
		self.beerList = scraper.getUserBeerURLs(self.url, self.userID)
	def getBeerList(self):
		return self.beerList
	def setUserName(self):
		if self.soup == None: return
		userName = self.soup.find_all("span", class_ = "username")
		if len(userName) > 0:
			self.userName = str(userName[0].get_text())
	def setNumRatings(self):
		if self.soup == None: return
		numRatings = self.soup.find_all("div", id = "beer-ratings")
		if len(numRatings) > 0:
			self.numRatings = numRatings[0].get_text()
	def setNumPlaces(self):
		if self.soup == None: return
		numPlaces = self.soup.find_all("div", id = "place-ratings")
		if len(numPlaces) > 0:
			self.numPlaces = numPlaces[0].get_text()
	def setNumBreweries(self):
		if self.soup == None: return
		numBreweries = self.soup.find_all("div", id = "breweries")
		if len(numBreweries) > 0:
			self.numBreweries = numBreweries[0].get_text()
	def setNumCountries(self):
		if self.soup == None: return
		numCountries = self.soup.find_all("div", id = "countries-rated")
		if len(numCountries) > 0:
			self.numCountries = numCountries[0].get_text()
	def setNumStyles(self):
		if self.soup == None: return
		numStyles = self.soup.find_all("div", id = "style-ratings")
		if len(numStyles) > 0:
			self.numStyles = numStyles[0].get_text()
	def setNumFollowing(self):
		if self.soup == None: return
		numFollowing = self.soup.find_all("div", id = "following")
		if len(numFollowing) > 0:
			self.numFollowing = numFollowing[0].get_text()
	def setNumFriends(self):
		if self.soup == None: return
		numFriends = self.soup.find_all("div", id = "friends")
		if len(numFriends) > 0:
			self.numFriends = numFriends[0].get_text()
	def setProfileBio(self):
		if self.soup == None: return
		bioInfo = self.soup.find_all("div", class_ = "biography")
		if len(bioInfo) > 0:
			pattern = '[\n\r\t]'
			self.profileBio = re.sub(pattern, '', bioInfo[0].get_text())
	def prettyPrint(self):
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(self.outputToDict())

	def cleanAllData(self):
		self.userID = soupParser.removeNonAscii(self.userID)
		self.url = soupParser.removeNonAscii(self.url)
		self.userName = soupParser.removeNonAscii(self.userName)
		self.numRatings = soupParser.removeNonAscii(self.numRatings)
		self.numPlaces = soupParser.removeNonAscii(self.numPlaces)
		self.numBreweries = soupParser.removeNonAscii(self.numBreweries)
		self.numCountries = soupParser.removeNonAscii(self.numCountries)
		self.numFollowing = soupParser.removeNonAscii(self.numFollowing)
		self.numFriends = soupParser.removeNonAscii(self.numFriends)
		self.profileBio = soupParser.removeNonAscii(self.profileBio)

	def outputToDict(self):
		dict = {
			"user_id" : self.userID,
			"user_url": self.url,
			"user_name" : self.userName,
			"user_num_ratings" : self.numRatings,
			"user_num_places_rated" : self.numPlaces,
			"user_num_breweries_rated" : self.numBreweries,
			"user_num_countries_rated" : self.numCountries,
			"user_num_following" : self.numFollowing,
			"user_num_friends" : self.numFriends,
			"user_location" : self.profileBio
		}
		return dict
