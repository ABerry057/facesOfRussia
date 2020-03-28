"""
Performs MALLET-based LDA topic modeling from generated corpus.
"""

from gensim.test.utils import common_corpus, common_dictionary
from gensim.models.wrappers import LdaMallet

path_to_mallet_binary = "/home/alex/mallet-2.0.8/mallet-2.0.8/bin/mallet"
model = LdaMallet(path_to_mallet_binary, corpus=common_corpus, num_topics=20, id2word=common_dictionary)
vector = model[common_corpus[0]]  # LDA topics of a documents