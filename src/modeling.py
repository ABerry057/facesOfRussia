"""
Performs MALLET-based LDA topic modeling from generated corpus.
"""
import pickle
from collections import OrderedDict
import pandas as pd
from tqdm import tqdm
from gensim.models.wrappers import LdaMallet
from pathlib import Path


def model_topics(era, n_topics=8, n_iterations=2500):
    parent_dir = Path(__file__).parents[1]
    seed = 1921
    
    dictionary, bow_corpus, IDs = pickle.load(open(parent_dir / 'data/corpus.pickle', 'rb'))
    path_to_mallet_binary = parent_dir / 'src//mallet-2.0.8/bin/mallet'
    
    model = LdaMallet(path_to_mallet_binary,
                      corpus=bow_corpus,
                      num_topics=n_topics,
                      id2word=dictionary,
                      iterations=n_iterations,
                      random_seed=seed)
    
    def doc_by_topic(vector):
        return sorted(vector, key=lambda x: x[1], reverse=True)
    
    topics_table = {}
    docs = list(model.load_document_topics())
    for i in tqdm(range(len(IDs)), desc='Reading results into dataframe'):
        doc = docs[i]
        topic_percentages = [t[1] for t in doc]
        topics_table[IDs[i]] = topic_percentages
        
    reference = pd.read_csv(parent_dir / 'data/reference.csv')
    title_dict = OrderedDict()
    for ID in tqdm(reference['ID'], desc='Getting titles from ID'):
        title_dict[ID] = reference[reference['ID'] == ID]['title'].values[0]
        
    year_dict = OrderedDict()
    for ID in tqdm(reference['ID'], desc='Getting years from ID'):
        year_dict[ID] = reference[reference['ID'] == ID]['date'].values[0]
    
    column_names = [f'topic_{i}' for i in range(0,n_topics)]
    results = pd.DataFrame.from_dict(topics_table,
                                     orient='index',
                                     columns=column_names)
    results.index.name = "ID"
    results.insert(0, "title", title_dict.values())  # add titles
    results.insert(1, "ID", IDs) # add ids
    results.insert(2, "year", year_dict.values())  # add years
    
    # save results to file
    results.to_csv(parent_dir / 'data' / f'{era}_topics.csv', index=False)
    
    # save topic words to file
    topics = model.show_topics(num_topics=-1)
    with open(parent_dir / 'data' / f'{era}_topics.txt', 'a') as output:
        output.writelines(str(line)+'\n' for line in topics)

