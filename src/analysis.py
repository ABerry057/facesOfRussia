"""
Performs MALLET-based LDA topic modeling from generated corpus.
"""
import pickle
from collections import OrderedDict
import pandas as pd
from tqdm import tqdm
from gensim.models.wrappers import LdaMallet
from pathlib import Path

parent_dir = Path(__file__).parent.parent
seed = 1917
num_topics = 30

dictionary, bow_corpus, IDs = pickle.load(open(f'{parent_dir}/data/corpus.pickle', 'rb'))
path_to_mallet_binary = f'{parent_dir}/src//mallet-2.0.8/bin/mallet'

model = LdaMallet(path_to_mallet_binary,
                  corpus=bow_corpus,
                  num_topics=num_topics,
                  id2word=dictionary,
                  iterations=5000,
                  random_seed=seed)

def doc_by_topic(vector):
    return sorted(vector, key=lambda x: x[1], reverse=True)

topics_table = []
for i in tqdm(range(len(IDs)), desc='Reading results into dataframe'):
    doc = list(model.load_document_topics())[i]
    topic_percentages = [t[1] for t in doc]
    row = [IDs[i]] + topic_percentages
    topics_table.append(row)
    
reference = pd.read_csv(f'{parent_dir}/data/reference.csv')
title_dict = OrderedDict()
for ID in tqdm(reference['ID'], desc='Getting titles from ID'):
    title_dict[str(ID)] = reference[reference['ID'] == ID]['title'].values[0]
    
year_dict = OrderedDict()
for ID in tqdm(reference['ID'], desc='Getting years from ID'):
    year_dict[str(ID)] = reference[reference['ID'] == ID]['date'].values[0]

column_names = ['ID'] + [f'topic_{i}' for i in range(0,num_topics)]
results = pd.DataFrame(topics_table, columns = column_names)
results.insert(1, "title", title_dict.values()) # add titles
results.insert(2, "year", year_dict.values()) # add years

# save results to file
results.to_csv(f'{parent_dir}/data/topics.csv')

# save topic words to file
topics = model.show_topics(num_topics=-1)
with open(f'{parent_dir}/data/topics.txt', 'a') as output:
    output.writelines(str(line)+'\n' for line in topics)