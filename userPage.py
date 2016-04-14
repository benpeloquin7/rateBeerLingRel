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
		self.bio = None ## location ???
		self.numRatings = None
		self.numPlaces = None
		self.numBreweries = None
		self.numCountries = None
		self.numStyles = None
		self.numFollowing = None
		self.numFriends = None
		self.memberSince = None
		self.profileBio = None

	def setAllFields(self):
		self.setUrl()
		self.setBeerList()
		self.setSoup()
		self.setUserName

	def setUrl(self):
		self.url = scraper.constructBeerListURL(self.userID)
	def setBeerList(self):
		self.beerList = scraper.getUserBeerURLs(self.url, self.userID)
	def setSoup(self):
		self.soup = scraper.urlToSoup(self.url)
	def setUserName(self):
		if self.soup == None: return
		userName = self.soup.find_all("span", class_ = "username")
		if len(userName) > 0:
			self.userName = userName[0].get_text()
	def setNumRatings(self):
		pass
	def setNumPlaces(self):
		pass
	def setNumBreweries(self):
		pass
	def setNumCountries(self):
		pass
	def setNumStyles(self):
		pass
	def setNumFollowing(self):
		pass
	def setNumFriends(self):
		pass	
	def setMemberSince(self):
		pass	
	def setBio(self):
		pass	