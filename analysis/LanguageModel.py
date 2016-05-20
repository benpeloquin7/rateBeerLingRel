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
		self.full_vocab = full_vocab               ## Do we want to store all possible words?
		self.training_vocab = set()
		self.training_total_tokens = 1             ## Save UNK
		self.training_vocab_size = 1               ## Save UNK
		self.ngrams_dict = defaultdict(lambda:0)   ## Holds all unigrams, bigrams and trigrams
		                                           ## default return 0 if no key

		self.ngram_range = ngram_range
		self.raw_data = []
		self.vocab_size = 0
		self.total_tokens = 0
		self.UNK = "UNK"
		self.START_SYMBOL = "__START__"
		self.END_SYMBOL = "__END__"
		self.VECTORIZER_TOKEN_PATTERN = u"(?u)\\b\\w+\\b"

		self.verbose = verbose
		
		## Scikit-learn text feature extraction helpers -- parameters
		self.ngram_vectorizer = CountVectorizer(ngram_range=ngram_range,\
								min_df = 1,\
								max_df = 1.0,\
								lowercase = True,\
								analyzer = "word",\
								token_pattern=self.VECTORIZER_TOKEN_PATTERN)

	def add_start_end_tokens(self, data):
		processed_data = self.START_SYMBOL + ' ' + data + ' ' + self.END_SYMBOL
		return processed_data


	def train(self, data):
		
		self.raw_data = [self.add_start_end_tokens(d) for d in data]

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

	def get_current_unigram(self, gram):
		return gram.split()[-1]

	def get_current_bigram(self, gram):
		return (' ').join(gram.split()[-2:])

	def get_words_and_counts(self):
		return([(word, count) for word, count in self.ngrams_dict.items()])

	def score(self, curr_example):
		return 0

	def print_internals(self, print_vocab = False):
		print "printing internals..."
		print "----------------------"
		print 'vocab_size:\t', self.training_vocab_size
		print 'total_tokens:\t', self.training_total_tokens
		if print_vocab: print 'vocab:\t', self.ngram_vectorizer.get_feature_names()


class UnigramLM_Laplace(LanguageModel):

	def score(self, curr_example):	
		processed_example = self.add_start_end_tokens(curr_example)
		example_length = len(processed_example.split())
	
		unigram_vectorizer = CountVectorizer(ngram_range=(1,1),\
												min_df=1,\
												max_df=1.0,\
												lowercase=True,
												analyzer="word",
												token_pattern=self.VECTORIZER_TOKEN_PATTERN)
		unigram_vectorizer.fit_transform([processed_example])
		unigram_count_matrix = unigram_vectorizer.transform([processed_example])
		
		score = 0
		for gram, count in zip(unigram_vectorizer.get_feature_names(), np.asarray(unigram_count_matrix.sum(axis=0)).ravel()):
			score += count * math.log(self.ngrams_dict[gram] + 1)
			score -= count * math.log(self.training_total_tokens + self.training_vocab_size)

		## Calculate perplexity for scoring
		exponent = -float(1) / example_length
		pp_score = math.pow(math.exp(score), exponent) if math.exp(score) > 0.0 else float('+inf')

		return pp_score

class BigramLM_Laplace(LanguageModel):

	def score(self, curr_example):
		# pdb.set_trace()	
		processed_example = self.add_start_end_tokens(curr_example)
		example_length = len(processed_example.split())
	
		bigram_vectorizer = CountVectorizer(ngram_range=(2,2),\
												min_df=1,\
												max_df=1.0,\
												lowercase=True,
												analyzer="word",
												token_pattern=self.VECTORIZER_TOKEN_PATTERN)
		bigram_vectorizer.fit_transform([processed_example])
		bigram_count_matrix = bigram_vectorizer.transform([processed_example])

		score = 0
		for gram, count in zip(bigram_vectorizer.get_feature_names(), np.asarray(bigram_count_matrix.sum(axis=0)).ravel()):
			score += count * math.log(self.ngrams_dict[gram] + 1)
			leading_unigram = self.get_leading_unigram(gram)
			score -= count * math.log(self.ngrams_dict[leading_unigram] + self.training_vocab_size)
			# n_size += count

		## Calculate perplexity for scoring
		exponent = -float(1) / example_length
		pp_score = math.pow(math.exp(score), exponent) if math.exp(score) > 0.0 else float('+inf')

		return pp_score

class TrigramLM_Laplace(LanguageModel):

	def score(self, curr_example):	
		# pdb.set_trace()	
		processed_example = self.add_start_end_tokens(curr_example)
		example_length = len(processed_example.split())

		trigram_vectorizer = CountVectorizer(ngram_range=(3,3),\
												min_df=1,\
												max_df=1.0,\
												lowercase=True,
												analyzer="word",
												token_pattern=self.VECTORIZER_TOKEN_PATTERN)
		trigram_vectorizer.fit_transform([processed_example])
		trigram_count_matrix = trigram_vectorizer.transform([processed_example])

		score = 0
		for gram, count in zip(trigram_vectorizer.get_feature_names(), np.asarray(trigram_count_matrix.sum(axis=0)).ravel()):
			score += count * math.log(self.ngrams_dict[gram] + 1)
			leading_bigram = self.get_leading_bigram(gram)
			score -= count * math.log(self.ngrams_dict[leading_bigram] + self.training_vocab_size)

		## Calculate perplexity for scoring
		exponent = -float(1) / example_length
		pp_score = math.pow(math.exp(score), exponent) if math.exp(score) > 0.0 else float('+inf')

		return pp_score


class Trigram_SB_LM(LanguageModel):

	def score(self, curr_example):	

		# print 'curr_example', curr_example
		processed_example = self.add_start_end_tokens(curr_example)
		# print 'processed_example', processed_example 
		example_length = len(processed_example.split())
		# print 'processed_example', processed_example

		## Populate Trigrams
		trigram_vectorizer = CountVectorizer(ngram_range=(3,3),\
												min_df=1,\
												max_df=1.0,\
												lowercase=True,
												analyzer="word",
												token_pattern=self.VECTORIZER_TOKEN_PATTERN)
		trigram_vectorizer.fit_transform([processed_example])
		trigram_count_matrix = trigram_vectorizer.transform([processed_example])

		## Trigram stupid backoff score calculation
		score = 0
		for gram, count in zip(trigram_vectorizer.get_feature_names(), np.asarray(trigram_count_matrix.sum(axis=0)).ravel()):
			leading_bigram = self.get_leading_bigram(gram)
			curr_bigram = self.get_current_bigram(gram)
			curr_unigram = self.get_current_unigram(gram)

			## trigrams
			if self.ngrams_dict[gram] != 0:
				score += count * math.log(self.ngrams_dict[gram])
				score -= count * math.log(self.ngrams_dict[leading_bigram])
			## back-off to bigrams
			elif self.ngrams_dict[curr_bigram] != 0:
				score += 0.4 * count * math.log(self.ngrams_dict[curr_bigram])
				score -= count * math.log(self.ngrams_dict[curr_unigram])
			## back-off to smoothed unigrams
			else:
				score += 0.4**2 * count * math.log(self.ngrams_dict[curr_unigram] + 1)
				score -= count * math.log(self.training_total_tokens + self.training_vocab_size)
		
		## Calculate perplexity for scoring
		exponent = -float(1) / example_length
		pp_score = math.pow(math.exp(score), exponent) if math.exp(score) > 0.0 else float('+inf')

		return pp_score

if __name__ == '__main__':
	# data_path = '../data/clean_data_full.csv'
	# df = pd.read_csv(data_path)
	# reviews = df['review_blob'].values
	# num_reviews = df['user_num_ratings'].values
	# reviews_shortened = reviews[1:10000]

	# print "Training models"
	# unigram_lm = UnigramLM_Laplace()
	# unigram_lm.train(reviews_shortened)
	# bigram_lm = BigramLM_Laplace()
	# bigram_lm.train(reviews_shortened)
	# trigram_lm = TrigramLM_Laplace()
	# trigram_lm.train(reviews_shortened)

	# for ide in [100, 1000, 1100, 1200, 3]:
	#     print("Review\n--------------")
	#     print(reviews_shortened[ide])
	#     print('unigram', unigram_lm.score(reviews_shortened[ide]))
	#     print('bigram', bigram_lm.score(reviews_shortened[ide]))
	#     print('trigram', trigram_lm.score(reviews_shortened[ide]))


	corpus = ['I am sam', 'sam I am', 'I really like eating ham']

	test1 = "hello sam friend"
	test2 = "i am sam"
	test3 = "i like eating sam"
	
	unigram_lm = UnigramLM_Laplace()
	bigram_lm = BigramLM_Laplace()

	bigram_lm.train(corpus)
	unigram_lm.train(corpus)
	
	print 'internals:\t'
	bigram_lm.print_internals(print_vocab = True)
	print unigram_lm.score(test1)
	print bigram_lm.score(test1)