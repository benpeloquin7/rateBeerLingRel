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
		self.training_total_tokens = 0
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
			
			## Save all unigrams to vocab and get total token counts
			if len(word.split()) == 1:
				self.training_vocab.add(word)
				self.training_total_tokens += count
			## Populate to ngrams dict
			self.ngrams_dict[word] = count

		self.training_vocab_size = len(self.training_vocab) + 1 ## Add one for UNK

	def get_leading_unigram(self, gram):
		return gram.split()[0]

	def get_leading_bigram(self, gram):
		return (' ').join(gram.split()[:2])

	def get_words_and_counts(self):
		return([(word, count) for word, count in self.ngrams_dict.items()])

	def score(self, curr_example):
		return 0


class UnigramLM_Laplace(LanguageModel):

	def score(self, curr_example):		
		example_length = len(curr_example.split())

		score = 0

		unigram_vectorizer = CountVectorizer(ngram_range=(1,1))
		unigram_vectorizer.fit_transform([curr_example])
		unigram_count_matrix = unigram_vectorizer.transform([curr_example])

		for gram, count in zip(unigram_vectorizer.get_feature_names(), np.asarray(unigram_count_matrix.sum(axis=0)).ravel()):
			score += math.log(count) + math.log(self.ngrams_dict[gram] + 1)
			score -= math.log(count) + math.log(self.training_total_tokens + self.training_vocab_size)

		exponent = -float(1) / example_length
		pp_score = math.pow(math.exp(score), exponent)

		return pp_score

class BigramLM_Laplace(LanguageModel):

	def score(self, curr_example):		
		example_length = len(curr_example.split())

		## In the case of the bigram model avoid one word case
		if example_length < 2:
			return float('inf')

		score = 0

		bigram_vectorizer = CountVectorizer(ngram_range=(2,2))
		bigram_vectorizer.fit_transform([curr_example])
		bigram_count_matrix = bigram_vectorizer.transform([curr_example])

		for gram, count in zip(bigram_vectorizer.get_feature_names(), np.asarray(bigram_count_matrix.sum(axis=0)).ravel()):
			score += math.log(count) + math.log(self.ngrams_dict[gram] + 1)
			leading_unigram = self.get_leading_unigram(gram)
			score -= math.log(count) + math.log(self.ngrams_dict[leading_unigram] + self.training_vocab_size)

		exponent = -float(1) / example_length
		pp_score = math.pow(math.exp(score), exponent)

		return pp_score

class TrigramLM_Laplace(LanguageModel):

	def score(self, curr_example):		
		example_length = len(curr_example.split())

		## In the case of the trigram model avoid one word case
		if example_length < 3:
			return float('inf')

		score = 0

		trigram_vectorizer = CountVectorizer(ngram_range=(3,3))
		trigram_vectorizer.fit_transform([curr_example])
		trigram_count_matrix = trigram_vectorizer.transform([curr_example])

		for gram, count in zip(trigram_vectorizer.get_feature_names(), np.asarray(trigram_count_matrix.sum(axis=0)).ravel()):
			score += math.log(count) + math.log(self.ngrams_dict[gram] + 1)
			leading_bigram = self.get_leading_bigram(gram)
			score -= math.log(count) + math.log(self.ngrams_dict[leading_bigram] + self.training_vocab_size)

		exponent = -float(1) / example_length
		pp_score = math.pow(math.exp(score), exponent)

		return pp_score


class Trigram_Interpolated_LM(LanguageModel):

	def score(self, curr_example):		
		example_length = len(curr_example.split())

		## In the case of the trigram model avoid one word case
		if example_length < 3:
			return float('inf')

		score = 0

		trigram_vectorizer = CountVectorizer(ngram_range=(3,3))
		trigram_vectorizer.fit_transform([curr_example])
		trigram_count_matrix = trigram_vectorizer.transform([curr_example])

		## bigram score calculation
		for gram, count in zip(trigram_vectorizer.get_feature_names(), np.asarray(trigram_count_matrix.sum(axis=0)).ravel()):
			## Laplace smoothing with +1 / UNK implicitly
			score += math.log(count) + math.log(self.ngrams_dict[gram] + 1)
			leading_bigram = self.get_leading_bigram(gram)
			## Laplace smoothing with +1 / UNK with max(x, 1)
			score -= math.log(count) + math.log(self.ngrams_dict[leading_bigram] + self.training_vocab_size)

		exponent = -float(1) / example_length
		pp_score = math.pow(math.exp(score), exponent)

		return pp_score

if __name__ == '__main__':
	trial_data = ['hello world', 'hello world oh, hello jim again', 'i am sam']

	# lm = LanguageModel()
	# lm.train(trial_data)
	# print "score 1:\t", lm.score('hello world')
	# print "score 2:\t", lm.score('over the rainbow')
	# print "score 3:\t", lm.score('were waiting along time for many things to come')
	# print "score 4:\t", lm.score('world oh, jim')
	# print lm.get_words_and_counts()