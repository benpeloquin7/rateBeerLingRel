class ReviewData():
	def __init__(self, userID, beerName, ratings, review):
		self.userID = userID
		self.beerName = beerName
		self.ratingsBlob = ratings
		self.reviewBlob = review
		self.overallScore = None
		self.totalScore = None
		self.aromaScore = None
		self.appearanceScore = None
		self.tasteScore = None
		self.palateScore = None
	
	######
	###### Data
	###### 

	## Overall
	def setOverallScore(self):
		pass
	def getOverallScore(self):
		return self.overallScore
	## Total
	def setTotalScore(self):
		pass
	def getTotalScore(self):
		return self.totalScore
	## Aroma
	def setAromaScore(self):
		pass
	def getAromaScore(self):
		return self.aromaScore
	## Appearance
	def setAppearanceScore(self):
		pass
	def getAppearanceScore(self):
		return self.appearanceScore
	## Taste
	def setTasteScore(self):
		pass
	def getTasteScore(self):
		return self.tasteScore
	## Palate
	def setPalateScore(self):
		pass
	def getPalateScore(self):
		return self.palateScore

	
	######
	###### Processing functionality
	######  
	