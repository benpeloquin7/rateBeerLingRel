#############
#############
############# General language model class
#############
#############
import time
import pdb
import math
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer


class LanguageModel:
	def __init__(self, verbose=False, full_vocab=None, ngram_range=(1, 3)):
		self.full_vocab = full_vocab            ## Do we want to store all possible words?
		
		self.ngram_dict = defaultdict(lambda:0) ## Holds all unigrams, bigrams and trigrams


		self.ngram_range = ngram_range
		self.unigram_dict = defaultdict(lambda:0)
		self.bigram_dict = defaultdict(lambda:0)
		self.trigram_dict = defaultdict(lambda:0)
		self.score_fn = None
		self.raw_data = []
		self.vocab_size = 0
		self.total_tokens = 0
		self.UNK = "UNK"

		self.verbose = verbose
		
		## Scikit-learn text feature extraction helpers -- parameters
		self.ngram_vectorizer = CountVectorizer(ngram_range=ngram_range)

	def train(self, data):
		
		self.raw_data = data

		if self.verbose: print("Currently fitting ngrams in range:\t", self.ngram_range)
		self.ngram_vectorizer.fit_transform(self.raw_data)                               ## Vocab
		self.ngram_count_matrix = self.ngram_vectorizer.transform(self.raw_data)         ## Counts
		for word, count in zip(self.ngram_vectorizer.get_feature_names(), np.asarray(self.ngram_count_matrix.sum(axis=0)).ravel()):
			self.ngram_dict[word] = count

		# if self.verbose: print("unigram model")
		# self.unigram_vectorizer.fit_transform(self.raw_data)                           ## Vocab
		# self.unigram_count_matrix = self.unigram_vectorizer.transform(self.raw_data)   ## Counts
		# for word, count in zip(self.unigram_vectorizer.get_feature_names(), np.asarray(self.unigram_count_matrix.sum(axis=0)).ravel()):
		# 	self.events_dict[word] = count


		# if self.verbose: print("bigram model")
		# self.bigram_vectorizer.fit_transform(self.raw_data)                            ## Vocab
		# self.bigram_count_matrix = self.bigram_vectorizer.transform(self.raw_data)     ## Counts
		# for word, count in zip(self.bigram_vectorizer.get_feature_names(), np.asarray(self.bigram_count_matrix.sum(axis=0)).ravel()):
		# 	self.events_dict[word] = count


		# if self.verbose: print("trigram model")
		# self.trigram_vectorizer.fit_transform(self.raw_data)                           ## Vocab
		# self.trigram_count_matrix = self.trigram_vectorizer.transform(self.raw_data)   ## Counts
		# for word, count in zip(self.unigram_vectorizer.get_feature_names(), np.asarray(self.trigram_count_matrix.sum(axis=0)).ravel()):
		# 	self.events_dict[word] = count

		


	def get_leading_unigram(self, gram):
		return gram.split()[0]

	def get_leading_bigram(self, gram):
		return (' ').join(gram.split()[:1])


	def get_words_and_counts(self):
		return([(word, count) for word, count in self.ngram_dict.items()])

	def score(self, curr_example):
		pass
	
	# 	score = 0

	# 	## Process example
	# 	unigram_vectorizer = CountVectorizer(ngram_range=(1,1))
	# 	unigram_vectorizer.fit_transform([curr_example])
	# 	unigram_count_matrix = unigram_vectorizer.transform(curr_example)
	# 	bigram_vectorizer = CountVectorizer(ngram_range=(2,2))
	# 	bigram_vectorizer.fit_transform([curr_example])
	# 	bigram_count_matrix = bigram_vectorizer.transform(curr_example)
	# 	trigram_vectorizer = CountVectorizer(ngram_range=(3,3))
	# 	trigram_vectorizer.fit_transform([curr_example])
	# 	trigram_count_matrix = trigram_vectorizer.transform(curr_example)
		
	# 	## Bigram score
	# 	for gram, count in zip(bigram_vectorizer.get_feature_names, np.asarray(bigram_count_matrix.sum(axis=0)).ravel()):
	# 		score += count * math.log(min(self.events_dict[gram], 1))
	# 		leading_unigram = self.get_leading_unigram(gram)
	# 		score -= count * math.log(min(self.events_dict[leading_unigram]), 1)

	# 	return score

	# def get_vocab(self):
	# 	return self.unigram_dict.keys() + self.bigram_dict.keys()  + self.trigram_dict.keys()



if __name__ == '__main__':
	pdb.set_trace()
	trial_data = ['hello world', 'hello world oh, hello world again', 'i am sam']

	lm = LanguageModel()
	lm.train(trial_data)
	print lm.get_words_and_counts()