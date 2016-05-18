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
		self.training_vocab = set()
		self.ngrams_dict = defaultdict(lambda:0) ## Holds all unigrams, bigrams and trigrams


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
			## Save all unigrams to vocavular
			if len(word.split()) == 1: self.training_vocab.add(word)
			self.ngrams_dict[word] = count

		self.training_vocab_size = len(self.training_vocab) + 1 ## Add one for UNK

	def get_leading_unigram(self, gram):
		return gram.split()[0]

	def get_leading_bigram(self, gram):
		return (' ').join(gram.split()[:1])


	def get_words_and_counts(self):
		return([(word, count) for word, count in self.ngrams_dict.items()])

	def score(self, curr_example):
		return 0
		
		# example_length = len(curr_example.split())

		# ## In the case of the bigram model avoid one word case
		# if example_length < 2:
		# 	return 0

		# score = 0

		# ## unigrams
		# # unigram_vectorizer = CountVectorizer(ngram_range=(1,1))
		# # unigram_vectorizer.fit_transform([curr_example])
		# # unigram_count_matrix = unigram_vectorizer.transform(curr_example)
		# ## bigrams
		# bigram_vectorizer = CountVectorizer(ngram_range=(2,2)) ## Keep the 1 so that we can handle one word reviews
		# bigram_vectorizer.fit_transform([curr_example])
		# bigram_count_matrix = bigram_vectorizer.transform([curr_example])


		# ## bigram score calculation
		# for gram, count in zip(bigram_vectorizer.get_feature_names(), np.asarray(bigram_count_matrix.sum(axis=0)).ravel()):
		# 	score += count * math.log(self.ngrams_dict[gram] + 1)            ## Laplace smoothing with +1 / UNK implicitly
		# 	leading_unigram = self.get_leading_unigram(gram)
		# 	score -= count * math.log(self.ngrams_dict[leading_unigram] + self.training_vocab_size) ## Laplace smoothing with +1 / UNK with max(x, 1)

		# exponent = -float(1) / example_length
		# pp_score = math.pow(math.exp(score), exponent)

		# return pp_score


class BigramLM_Laplace(LanguageModel):

	def score(self, curr_example):		
		example_length = len(curr_example.split())

		## In the case of the bigram model avoid one word case
		if example_length < 2:
			return 0

		score = 0

		bigram_vectorizer = CountVectorizer(ngram_range=(2,2)) ## Keep the 1 so that we can handle one word reviews
		bigram_vectorizer.fit_transform([curr_example])
		bigram_count_matrix = bigram_vectorizer.transform([curr_example])

		## bigram score calculation
		for gram, count in zip(bigram_vectorizer.get_feature_names(), np.asarray(bigram_count_matrix.sum(axis=0)).ravel()):
			score += count * math.log(self.ngrams_dict[gram] + 1)            ## Laplace smoothing with +1 / UNK implicitly
			leading_unigram = self.get_leading_unigram(gram)
			score -= count * math.log(self.ngrams_dict[leading_unigram] + self.training_vocab_size) ## Laplace smoothing with +1 / UNK with max(x, 1)

		exponent = -float(1) / example_length
		pp_score = math.pow(math.exp(score), exponent)

		return pp_score


if __name__ == '__main__':
	trial_data = ['hello world', 'hello world oh, hello jim again', 'i am sam']

	lm = LanguageModel()
	lm.train(trial_data)
	print "score 1:\t", lm.score('hello world')
	print "score 2:\t", lm.score('over the rainbow')
	print "score 3:\t", lm.score('were waiting along time for many things to come')
	print "score 4:\t", lm.score('world oh, jim')
	print lm.get_words_and_counts()