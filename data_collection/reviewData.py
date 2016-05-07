import re
import pprint
import pdb
import soupParser
import scraper
from bs4 import BeautifulSoup

class ReviewData():
	def __init__(self):
		# , userID, beerName, ratings, review
		## User info
		## ---------
		self.userID = None
		self.userName = None
		self.userNumRated = None
		self.url = None
		## Current review info
		## -------------------
		self.beerName = None
		self.ratingsBlob = None
		self.reviewBlob = None
		self.overallScore = None
		self.overallScoreTotal = 20
		self.avgScore = None
		self.avgScoreTotal = 5
		self.aromaScore = None
		self.aromaScoreTotal = 10
		self.appearanceScore = None
		self.appearanceScoreTotal = 5
		self.tasteScore = None
		self.tasteScoreTotal = 10
		self.palateScore = None
		self.palateScoreTotal = 5
		## Beer global info
		## -----------------
		self.beerGlobalScore = None
		self.beerGlobalStyleScore = None
		self.brewerName = None
		self.beerStyleName = None
		self.beerCountryOfOrigin = None
		self.beerNumRatings = None
		self.beerWeightedAvgScore = None
		self.beerNumCalories = None
		self.beerABV = None

	######
	###### Data
	###### 
	## Set all data wrapper
	def setAllReviewData(self, userID, url):
		# Prelim data
		soup = scraper.urlToSoup(url)
		data = soupParser.getBeerInfo(soup)
		self.userID = userID
		self.url = url
		self.beerName = soupParser.removeNonAscii(data[0])
		self.ratingsBlob = soupParser.removeNonAscii(data[1])
		self.reviewBlob = soupParser.removeNonAscii(data[2])
		# Set remaining data
		self.setReviewData()
		self.setBeerGlobalInfo(soupParser.getBeerGlobalInfo(soup))
		self.cleanAllData()

	## Set review fields
	def setReviewData(self):
		"""
		Set internal data
		"""
		self.setUserName()
		self.setUserNumRated()
		self.setOverallScore()
		self.setAvgScore()
		self.setAromaScore()
		self.setAppearanceScore()
		self.setTasteScore()
		self.setPalateScore()

	## set global beer fields
	def setBeerGlobalInfo(self, data):
		"""
		`data` should be returned from a call to soupParser.getBeerGlobalInfo()
		"""
		self.beerGlobalScore = data[0]
		self.beerGlobalStyleScore = data[1]
		self.brewerName = data[2]
		self.beerStyleName = data[3]
		self.beerCountryOfOrigin = data[4]
		self.beerNumRatings = data[5]
		self.beerWeightedAvgScore = data[6]
		self.beerNumCalories = data[7]
		self.beerABV = data[8]

	## Remove non_ascii from all data
	def cleanAllData(self):
		self.userID = soupParser.removeNonAscii(self.userID)
		self.userName = soupParser.removeNonAscii(self.userName)
		self.userNumRated = soupParser.removeNonAscii(self.userNumRated)
		## Current review info
		## -------------------
		self.beerName = soupParser.removeNonAscii(self.beerName)
		self.ratingsBlob = soupParser.removeNonAscii(self.ratingsBlob)
		self.reviewBlob = soupParser.removeNonAscii(self.reviewBlob)
		self.overallScore = soupParser.removeNonAscii(self.overallScore)
		self.overallScoreTotal = soupParser.removeNonAscii(self.overallScoreTotal)
		self.avgScore = soupParser.removeNonAscii(self.avgScore)
		self.aromaScore = soupParser.removeNonAscii(self.aromaScore)
		self.appearanceScore = soupParser.removeNonAscii(self.appearanceScore)
		self.tasteScore = soupParser.removeNonAscii(self.tasteScore)
		self.palateScore = soupParser.removeNonAscii(self.palateScore)
		## Beer global info
		## -----------------
		self.beerGlobalScore = soupParser.removeNonAscii(self.beerGlobalScore)
		self.beerGlobalStyleScore = soupParser.removeNonAscii(self.beerGlobalStyleScore)
		self.brewerName = soupParser.removeNonAscii(self.brewerName)
		self.beerStyleName = soupParser.removeNonAscii(self.beerStyleName)
		self.beerCountryOfOrigin = soupParser.removeNonAscii(self.beerCountryOfOrigin)
		self.beerNumRatings = soupParser.removeNonAscii(self.beerNumRatings)
		self.beerWeightedAvgScore = soupParser.removeNonAscii(self.beerWeightedAvgScore)
		self.beerNumCalories = soupParser.removeNonAscii(self.beerNumCalories)
		self.beerABV = soupParser.removeNonAscii(self.beerABV)


	## User name
	def setUserName(self):
		pattern = "OVERALL\s1?[0-9]/20(.+?)\([0-9]+\)$"
		score = re.search(pattern, self.ratingsBlob)
		self.userName = score.group(1) if score != None else score

	def setUserNumRated(self):
		pattern = ".+\(([0-9]+)\)$"
		score = re.search(pattern, self.ratingsBlob)
		self.userNumRated = score.group(1) if score != None else score

	## Overall
	def setOverallScore(self):
		pattern = "OVERALL\s((?:1|2)?[0-9])/20"
		score = re.search(pattern, self.ratingsBlob)
		self.overallScore = score.group(1) if score != None else score
	def getOverallScore(self):
		return self.overallScore
	
	## Avg score
	def setAvgScore(self):
		pattern = "^([0-5](?:\.[0-9])?)\sAROMA"
		score = re.search(pattern, self.ratingsBlob)
		self.avgScore = score.group(1) if score != None else score
	def getAvgScore(self):
		return self.avgScore
	
	## Aroma
	def setAromaScore(self):
		pattern = "AROMA\s([0-9]|10)/10\sAPPEARANCE"
		score = re.search(pattern, self.ratingsBlob)
		self.aromaScore = score.group(1) if score != None else score
	def getAromaScore(self):
		return self.aromaScore
	
	## Appearance
	def setAppearanceScore(self):
		pattern = "APPEARANCE\s([0-5])/5\sTASTE"
		score = re.search(pattern, self.ratingsBlob)
		self.appearanceScore = score.group(1) if score != None else score
	def getAppearanceScore(self):
		return self.appearanceScore
	
	## Taste
	def setTasteScore(self):
		pattern = "TASTE\s([0-9]|10)/10\sPALATE"
		score = re.search(pattern, self.ratingsBlob)
		self.tasteScore = score.group(1) if score != None else score
	def getTasteScore(self):
		return self.tasteScore
	
	## Palate
	def setPalateScore(self):
		pattern = "PALATE\s([0-5])/5\sOVERALL"
		score = re.search(pattern, self.ratingsBlob)
		self.palateScore = score.group(1) if score != None else score
	def getPalateScore(self):
		return self.palateScore

	
	######
	###### Processing functionality
	######  
	def parseReview(self):
		"""
		Extract linguistic content from review
		"""
		pass


	## NOTE: look at python pretty print functionality (pprint.py)
	def prettyPrint(self):
		"""
		Pretty printing of internal data
		"""
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(self.outputToDict())

		# print "------------------"
		# print "=================="
		# print "\t------USER------"
		# print "userID:\t", self.userID
		# print "userName:\t", self.userName
		# print "userNumRated:\t", self.userNumRated
		# print "\t------REVIEW------"
		# print "beerName:\t", self.beerName
		# print "overallScore:\t", self.overallScore
		# print "avgScore:\t", self.avgScore
		# print "aromaScore:\t", self.aromaScore
		# print "appearanceScore:\t", self.appearanceScore
		# print "tasteScore:\t", self.tasteScore
		# print "palateScore:\t", self.palateScore
		# print "reviewBlob:\t", self.reviewBlob
		# print "ratingsBlob:\t", self.ratingsBlob
		# print "\t------GLOBAL_BEER------"
		# print ""

	def outputToDict(self):
		"""
		Output internals to dictionary (for easy converstion to csv)
		"""
		dict = {
			## Review
			"review_overall_score" : self.overallScore,
			"review_avg_score" : self.avgScore,
			"review_aroma_score" : self.aromaScore,
			"review_appearance_score" : self.appearanceScore,
			"review_taste_score" : self.tasteScore,
			"review_palate_score" : self.palateScore,
			"review_blob" : self.reviewBlob,
			"review_ratings_blob" : self.ratingsBlob,
			## Beer global
			"beer_name" : self.beerName,
			"beer_url" : self.url,
			"beer_global_score" : self.beerGlobalScore,
			"beer_global_style_score" : self.beerGlobalStyleScore,
			"beer_brewer_name" : self.brewerName,
			"beer_style": self.beerStyleName,
			"beer_location" : self.beerCountryOfOrigin,
			"beer_num_ratings" : self.beerNumRatings,
			"beer_weighted_avg_score" : self.beerWeightedAvgScore,
			"beer_num_calories" : self.beerNumCalories,
			"beer_ABV" : self.beerABV
		}
		return dict