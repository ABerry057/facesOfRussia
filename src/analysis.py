"""
Performs MALLET-based LDA topic modeling from generated corpus.
"""
import pickle
from gensim.models.wrappers import LdaMallet
from pathlib import Path

parent_dir = Path(__file__).parent.parent
seed = 19

dictionary, bow_corpus = pickle.load(open(f'{parent_dir}/data/corpus.pickle', 'rb'))
path_to_mallet_binary = f'{parent_dir}/src//mallet-2.0.8/bin/mallet'

model = LdaMallet(path_to_mallet_binary,
                  corpus=bow_corpus,
                  num_topics=20,
                  id2word=dictionary,
                  iterations=5000,
                  random_seed=seed)

vector = model[bow_corpus[0]]  # LDA topics of a documents