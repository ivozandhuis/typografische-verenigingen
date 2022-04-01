#! /usr/bin/env python3
# Analyzing data/liedjes

import os
import spacy
import gensim
import random
import pprint

def texts2list(rootdir):
    # input: directory with (subdirectory with) TXT-files to be handled
	# output: list of strings lexicographically ordered on path-name

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

def lemmatize(texts, allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]):   
    # input: list of texts
    # input: allowed_postags is list of wordtypes to be kept in the lemmatization process
    # output: list of lemmatized texts. Lemmatization by spaCy.

    nlp = spacy.load("nl_core_news_sm") # create spaCy processor named 'nlp' based on small model for Dutch
    # nlp.Defaults.stop_words |= {"", "", ""} # optionally: add stopwords to processor

    result = []                                                         
    for text in texts:                                                     

        nlp.max_length = len(text)  
        doc = nlp(text) # tokenize and annotate 'text' with processor named 'nlp'

        new_text = []
        for token in doc: 
            if token.is_alpha: # keep tokens with alphanumerical characters (so no numbers or punctuation)
                if not token.is_stop: # remove stopwords
                    if token.pos_ in allowed_postags: # keep wordtypes in the allowed_postags list
                        new_text.append(token.lemma_) # get the word in the lemma and add it to the list of words

        final = " ".join(new_text) # transform list of words into a string concatenating all listitems
        result.append(final) # add string to the list of lemmatized texts

    return result

def preprocess(texts):
    # input: list of lemmatized texts
    # output: list of lists of preprocessed words, bigrams or trigrams. Preprocessing by gensim.

    # what kind of preprocessing does gensim do?
    result = []
    for text in texts:
        new = gensim.utils.simple_preprocess(text, deacc=True)
        result.append(new)

    # find bigrams and trigrams. Don't understand yet how precisely ... 
    bigram_phrases  = gensim.models.Phrases(result, min_count=5, threshold=100)
    trigram_phrases = gensim.models.Phrases(bigram_phrases[result], threshold=100)
    bigram  = gensim.models.phrases.Phraser(bigram_phrases)
    trigram = gensim.models.phrases.Phraser(trigram_phrases)
    bigrams  = [bigram[doc] for doc in result]
    trigrams = [trigram[bigram[doc]] for doc in result]

    return trigrams

######
n = 50 # Choose a number for a song to inspect.

liedjes   = texts2list('../../data/liedjes')
print(liedjes[n])

lemmatized_liedjes = lemmatize(liedjes)
print(lemmatized_liedjes[n])

preprocessed_liedjes = preprocess(lemmatized_liedjes)
print(preprocessed_liedjes[n])

# create gensim Dictionary-thing for input in gensim-code: list of unique words in alphabetical order
# (similar to 'vocabulary' in the VSM script)
liedjes_gensimDict = gensim.corpora.Dictionary(preprocessed_liedjes) 
liedjes_gensimDict.filter_extremes(no_below = 5, no_above = 0.5, keep_n = 100000) 

# create 'bag-of-words'
# A bag of words is a list of 2-tuples (term_id, frequency), where term_id is id for a term in the liedjes_gensimDict.
liedjes_bow = []
for text in preprocessed_liedjes:
    new = liedjes_gensimDict.doc2bow(text)
    liedjes_bow.append(new)

print(liedjes_bow[n])

# train model !!
lda_model = gensim.models.ldamodel.LdaModel(
    corpus  = liedjes_bow,         # corpus met documenten gerepresenteerd als bag-of-words
    id2word = liedjes_gensimDict,  # dictionary: lijst met identificatie nummers van alle woorden
    num_topics = 10,               # het aantal topics dat het algoritme zal identificeren 
    random_state = 100,            # seed voor het later kunnen reproduceren van de resultaten
    update_every = 1,              # 0 voor batch learning, > 1 voor online learning
    iterations = 100,              # aantal herhalingen
    chunksize = len(liedjes_bow),  # aantal gebruikte documenten per training 
    passes = 100,                  # aantal herhalingen gedurende een training 
    alpha = "auto",                # LDA hyperparameter, zie haalbaarheidsstudie
    eta = "symmetric")             # LDA hyperparameter, zie haalbaarheidsstudie

# get list of all topic-distributions per liedje
# a topic distribution is a list topics of a liedje. Every topic is a 2-tuples (topic_id, probability).
liedjes_topics_dist = lda_model.get_document_topics(liedjes_bow)
print(liedjes_topics_dist[n])

# print all topics (= combination of terms) of liedje 'n'
i = 0
while i < len(liedjes_topics_dist[n]):
    print(lda_model.show_topics(num_words = 10, formatted = True)[liedjes_topics_dist[n][i][0]])
    i = i + 1 
