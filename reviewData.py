import re
import pdb

class ReviewData():
	def __init__(self, userID, beerName, ratings, review):
		## User info
		self.userID = userID
		self.userName = None
		self.userNumRated = None
		## Current review info
		self.beerName = beerName
		self.ratingsBlob = ratings
		self.reviewBlob = review
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
		self.brewerName = None
		self.beerGlobalScore = None
		self.beerGlobalStyleScore = None
		self.beerWeightedAvgScore = None
		self.beerCountryOfOrigin = None
		self.beerNumRatings = None
		self.beerNumColories = None
		self.beerABV = None

	######
	###### Data
	###### 

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
		pattern = "OVERALL\s(1?[0-9])/20"
		score = re.search(pattern, self.ratingsBlob)
		self.overallScore = score.group(1) if score != None else score
	def getOverallScore(self):
		return self.overallScore
	
	## Avg
	def setAvgScore(self):
		pattern = "^([0-5]\.[0-9])\sAROMA"
		score = re.search(pattern, self.ratingsBlob)
		self.avgScore = score.group(1) if score != None else score
	def getAvgScore(self):
		return self.totalScore
	
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

	## Beer Global Info
	def setBeerGlobalInfo(self, data):
		self.beerGlobalScore = data[1]
		self.beerGlobalStyleScore = data[2]
		self.brewerName = data[3]
		self.beerWeightedAvgScore = data[3]
		self.beerCountryOfOrigin = None
		self.beerNumRatings = None
		self.beerNumColories = None
		self.beerABV = None

	## Set above fields
	def setData(self):
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
	
	######
	###### Processing functionality
	######  
	def parseReview(self):
		"""
		Extract linguistic content from review
		"""
		pass

	def prettyPrint(self):
		"""
		Pretty printing of internal data
		"""
		print "------------------"
		print "=================="
		print "\t------USER------"
		print "userID:\t", self.userID
		print "userName:\t", self.userName
		print "userNumRated:\t", self.userNumRated
		print "\t------BEER------"
		print "beerName:\t", self.beerName
		print "overallScore:\t", self.overallScore
		print "avgScore:\t", self.avgScore
		print "aromaScore:\t", self.aromaScore
		print "appearanceScore:\t", self.appearanceScore
		print "tasteScore:\t", self.tasteScore
		print "palateScore:\t", self.palateScore
		print "reviewBlob:\t", self.reviewBlob
		print "ratingsBlob:\t", self.ratingsBlob

	def outputToDict(self):
		"""
		Output internals to dictionary (for easy converstion to csv)
		"""
		dict = {
			userID : self.userID,
			userName : self.userName,
			userNumRated : self.userNumRated,
			beerName : self.beerName,
			overallScore : self.overallScore,
			avgScore : self.avgScore,
			aromaScore : self.aromaScore,
			appearanceScore : self.appearanceScore,
			tasteScore : self.tasteScore,
			palateScore : self.palateScore,
			reviewBlob : self.reviewBlob,
			ratingsBlob : self.ratingsBlob
		}
		return dict