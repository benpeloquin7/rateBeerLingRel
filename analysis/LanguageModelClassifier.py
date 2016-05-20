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
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import f1_score
from LanguageModel import Trigram_SB_LM


class LanguageModelClassifier(BaseEstimator, ClassifierMixin):
	# def __init__(self, lm_type = Trigram_SB_LM, verbose = False):
	# 	self.lm_type = lm_type
	# 	self.verbose = verbose

	def __init__(self, lm_type = Trigram_SB_LM):
		self.lm_type = lm_type
		self.model1 = self.lm_type()
		self.model2 = self.lm_type()
		self.model3 = self.lm_type()
		self.model4 = self.lm_type()
		self.q1_reviews = []
		self.q2_reviews = []
		self.q3_reviews = []
		self.q4_reviews = []

	def fit(self, X, y, verbose = False):

		## Get training data for quantiles
		self.q1_reviews = X[np.where(y == "Q1")[0]]
		self.q2_reviews = X[np.where(y == "Q2")[0]]
		self.q3_reviews = X[np.where(y == "Q3")[0]]
		self.q4_reviews = X[np.where(y == "Q4")[0]]

		if verbose:
			print 'training models'
			print self.model1.print_internals()
			print self.model2.print_internals()
			print self.model3.print_internals()
			print self.model4.print_internals()

		## train models
		self.model1.train(self.q1_reviews)
		self.model2.train(self.q2_reviews)
		self.model3.train(self.q3_reviews)
		self.model4.train(self.q4_reviews)

	def get_params(self, deep = False):
		return {'lm_type':self.lm_type }

	def predict(self, X):
		## Get all predictions
		def predict_one_example(x):
			preds = [(self.model1.score(x), "Q1"),\
					(self.model2.score(x), "Q2"),\
					(self.model3.score(x), "Q3"),\
					(self.model4.score(x), "Q4")]
			model_pred = min(preds)[1]
			return model_pred

		return([predict_one_example(x) for x in X])

	def score(self, X, y):
		return(f1_score(self.predict(X), y))


class BaselineLanguageModel(LanguageModelClassifier):

	def __init__(self, lm_type = Trigram_SB_LM):
		self.lm_type = lm_type
		self.return_class = None
		self.q1_len = 0
		self.q2_len = 0
		self.q3_len = 0
		self.q4_len = 0
		self.prediction_class = ''
		self.lm_type = ''

	def fit(self, X, y):

		## Get training data for quantiles
		self.q1_len = len(X[np.where(y == "Q1")[0]])
		self.q2_len = len(X[np.where(y == "Q2")[0]])
		self.q3_len = len(X[np.where(y == "Q3")[0]])
		self.q4_len = len(X[np.where(y == "Q4")[0]])
		self.prediction_class = max([(self.q1_len, "Q1"),\
										(self.q2_len, "Q2"),\
										(self.q1_len, "Q3"),
										(self.q1_len, "Q4")])[1]

	def predict(self, X):
		num_preds = len(X)
		return [self.prediction_class for _ in range(num_preds)]

	def score(self, X, y):
		return(f1_score(self.predict(X), y))