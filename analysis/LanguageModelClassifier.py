#############
#############
############# Language model classifier
#############
#############
import time
import pdb
import math
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer


class LanguageModelClassifier():
	def __init__(self, lm_type, verbose = False):
		self.model1 = lm_type()
		self.model2 = lm_type()
		self.model3 = lm_type()
		self.model4 = lm_type()
		self.verbose = verbose

	def fit(self, X, y):

		## Get training data for quantiles
		q1_reviews = X[np.where(y == "Q1")[0]]
		q2_reviews = X[np.where(y == "Q2")[0]]
		q3_reviews = X[np.where(y == "Q3")[0]]
		q4_reviews = X[np.where(y == "Q4")[0]]

		## Train language models
		if self.verbose: print "Currently training language models..."
		self.model1.train(q1_reviews)
		self.model2.train(q2_reviews)
		self.model3.train(q3_reviews)
		self.model4.train(q4_reviews)

	def predict(self, X):
		## Get all predictions
		preds = [(self.model1.score(X), "Q1"),\
					(self.model2.score(X), "Q2"),\
					(self.model3.score(X), "Q3"),\
					(self.model4.score(X), "Q4")]
		model_preds = min(preds)[1]
		
		return model_preds