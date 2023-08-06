import sys, os, subprocess
import spacy
import gensim
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class Important_Words:
    #input string list of context sentences
    def __init__(self, string_list):
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except:
            subprocess.call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_lg'])
            sys.exit('Please restart the program to take effect.')
        string_list = self.__pre_processing_list(string_list)
        self.vectorizer = TfidfVectorizer()
        self.vectorizer.fit_transform(string_list)
        self.feature_array = np.array(self.vectorizer.get_feature_names())

    def find_important_words(self, string):
        string_trimed = self.__pre_processing(string)
        string_trimed = self.n_gram.process(string_trimed)

        Y = self.vectorizer.transform([string_trimed])
        Y_arr = Y.toarray().flatten()
        tfidf_sorting = np.argsort(Y_arr)[::-1]
        n = len(Y.data)
        top_n = list(zip(self.feature_array[tfidf_sorting], Y_arr[tfidf_sorting]))[:n]

        return top_n

    def __pre_processing(self, string):
        new_string = ""
        doc = self.nlp(string)
        for w in doc:
            if w.text != '\n' and not w.is_stop and not w.is_punct and not w.like_num:
                new_string += " " + w.lemma_
        return new_string

    #input: (1-dim) list of string
    #process: remove punctuation, stop_words, number, connect bigram with _
    #output: (1-dim) list of string
    def __pre_processing_list(self, string_list):
        new_string_list = []
        #remove punctuation and stop words for each string
        for string in string_list:
            new_string = self.__pre_processing(string)
            new_string_list.append(new_string)

        #forming bigram
        self.n_gram = _N_gram(new_string_list)
        new_string_list = [self.n_gram.process(s) for s in new_string_list]

        return new_string_list

class _N_gram:
    #input string list (1-dim)
    def __init__(self, string_list):
        new_string_list = [str.split(" ") for str in string_list]
        self.bigram = gensim.models.Phrases(new_string_list, )
        self.trigram = gensim.models.Phrases(self.bigram[new_string_list])

    #input a string
    #output a string with n_gram connted with _
    def process(self, string):
        string = string.split(" ")
        string = self.bigram[string]
        string = self.trigram[string]
        return " ".join(string)