"""
Generates MALLET format corpus from raw texts.
"""
import os
import pickle
from tqdm import tqdm
from gensim import corpora
from gensim.utils import simple_preprocess

import nltk
from nltk.stem import WordNetLemmatizer
from pathlib import Path
from nltk.corpus import stopwords


def generate_corpus():
    """Uses NLTK features to process, lemmatize,
    and remove stopwords from a given corpus.
    Saves the result in a pickled bag-of-words for
    subsequent processing by MALLET.
    """
    nltk.download('stopwords')  # run once

    stop_words = stopwords.words('english')
    stop_words += ['wa', 'ha']  # included for all topics otherwise
    parent_dir = Path(__file__).parents[1]
    txt_dir = parent_dir / 'data' / 'raw_texts'

    lemmatizer = WordNetLemmatizer()

    processed_text_list = []
    # sort in ascending order by ID
    files = sorted(os.listdir(txt_dir),
                   key=lambda x: int(x.replace(".txt", ""))
                   )

    for file in tqdm(files, desc="Load and preprocess"):
        with open((txt_dir / file), 'r') as raw:
            text = raw.read()
        text_list = simple_preprocess(text)
        lemma_list = [lemmatizer.lemmatize(word) for word in text_list]
        stopped_list = [word for word in lemma_list if word not in stop_words]
        processed_text_list.append(stopped_list)

    # # create dictionary from preprocessed text
    dictionary = corpora.Dictionary(processed_text_list)
    bow_corpus = [dictionary.doc2bow(text) for text in processed_text_list]
    IDs = [int(file.replace('.txt', '')) for file in files]
    mallet_pack = (dictionary, bow_corpus, IDs)

    # # save BoW corpus as pickle
    pickle.dump(mallet_pack, open(parent_dir / 'data' / 'corpus.pickle', "wb"))


if __name__ == "__main__":
    generate_corpus()
