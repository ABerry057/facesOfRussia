"""
Generates MALLET format corpus from raw texts.
"""
import os
import pickle
from tqdm import tqdm
from gensim import corpora
from gensim.utils import simple_preprocess

import nltk
# nltk.download('stopwords')  # run once
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
from nltk.stem import WordNetLemmatizer
from pathlib import Path

parent_dir = Path(__file__).parent.parent
txt_dir = f'{parent_dir}/data/raw_texts'

lemmatizer = WordNetLemmatizer()

pro_text_list = []
for file in tqdm(os.listdir(txt_dir), desc="Load and preprocess"):
    with open(f'{txt_dir}/{file}', 'r') as raw:
        text = raw.read()
    text_list = simple_preprocess(text)
    lemma_list = [lemmatizer.lemmatize(word) for word in text_list]
    stopped_list = [word for word in lemma_list if word not in stop_words]
    pro_text_list += stopped_list
pro_text_list = [pro_text_list]
# create dictionary from preprocessed text
dictionary = corpora.Dictionary(pro_text_list)
bow_corpus = [dictionary.doc2bow(text) for text in pro_text_list]
mallet_pack = (dictionary, bow_corpus)
# save BoW corpus as pickle
pickle.dump(mallet_pack, open(f'{parent_dir}/data/corpus.pickle', "wb" ) )