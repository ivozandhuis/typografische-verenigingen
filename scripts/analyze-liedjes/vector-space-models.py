#! /usr/bin/env python3
# Analyzing data/liedjes
# With thanks to Karsdorp, Kestemont and Riddell 2021

import os
import nltk
import nltk.tokenize
import re
import unidecode
import collections
import numpy as np
import csv

nltk.download('punkt', quiet=True)

def read_data(csvfile):
	# Result: list (= row) of lists, without header.
	data = []
	headers = True
	with open(csvfile) as stream:
		reader = csv.reader(stream, delimiter=',')
		for row in reader:
			if not headers:
				data.append(row)

			headers=False

	return data


def texts2list(rootdir):
	# Result: A list where every item is the TXT of a file in directory and subdirectories of _rootdir_ ...
	# ... lexicographically ordered on path-name.
	files_all = []
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			if not file.endswith('.txt'):
				continue
			fn = os.path.join(subdir, file)
			files_all.append(fn)

	files_all = sorted(files_all)

	texts = []
	for file in files_all:
		with open(file) as stream:
			text = stream.read()
		texts.append(text)

	return texts

def is_punctuation(string):
	# Result: A boolean for being a punctuation mark or not
	return re.compile(r'[^\w\s]+$').match(string) is not None

def remove_diacritics(string):
	# Result: A string without diacritics (accents)
	return unidecode.unidecode(string)

def preprocess_text(string):
	# Result: list of tokens in a string (= "tokenized corpus")
	string = string.lower()
	tokens = nltk.tokenize.word_tokenize(string, language="dutch")
	tokens = [token for token in tokens if not is_punctuation(token)]
	tokens = [remove_diacritics(token) for token in tokens]

	return tokens

def extract_vocabulary(tokenized_corpus, min_count=1, max_count=float('inf')):
	# Result: list of unique words derived from a list of lists of strings
	vocabulary = collections.Counter()
	for document in tokenized_corpus:
		vocabulary.update(document)
	vocabulary = { 
		word for word, count in vocabulary.items()
		if count >= min_count and count <= max_count
	}

	return sorted(vocabulary)

def corpus2dtm(tokenized_corpus, vocabulary):
	# Result: Document Term Matrix: 
	# rows being documents in tokenized_corpus, columns being the words in vocabulary, 
	# values being the count of the word in the document
	document_term_matrix = []
	for document in tokenized_corpus:
		document_counts = collections.Counter(document)
		row = [document_counts[word] for word in vocabulary]
		document_term_matrix.append(row)

	return document_term_matrix

##########

liedjes_data = np.array(read_data('../../data/liedjes/liedjes.csv')) # create np.array to be able to order lexicographically
liedjes_data = liedjes_data[liedjes_data[:, 1].argsort()] # order lexicographically on identifier just like the textlist

liedjes_textlist = texts2list('../../data/liedjes')
tokenized_liedjes = [preprocess_text(liedje) for liedje in liedjes_textlist]
vocabulary_liedjes = extract_vocabulary(tokenized_liedjes, min_count=2)
dtm_liedjes = np.array(corpus2dtm(tokenized_liedjes, vocabulary_liedjes))

n=100
print(f"Created document-term matrix with {dtm_liedjes.shape[0]} liedjes and {dtm_liedjes.shape[1]} words.")
print(f"E.g.: liedje {n}:")
print(liedjes_data[n])
print(liedjes_textlist[n])
print(tokenized_liedjes[n])
print(dtm_liedjes[n])


