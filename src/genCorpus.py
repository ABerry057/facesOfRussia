"""
Generates MALLET format corpus from raw texts.
"""
import os
from tqdm import tqdm
from gensim import corpora
from gensim.utils import simple_preprocess, lemmatize

import nltk
# nltk.download('stopwords')  # run once
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
from pathlib import Path

parent_dir = Path(__file__).parent.parent
txt_dir = f'{parent_dir}/data/raw_texts'

p_text_list = []
for file in tqdm(os.listdir(txt_dir), desc="Load and preprocess"):
    with open(f'{txt_dir}/{file}', 'r') as raw:
        text = lemmatize(raw.read(), stopwords=frozenset(stop_words))
    text_list = simple_preprocess(text)
    p_text_list += text_list