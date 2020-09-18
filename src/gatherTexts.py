"""
Builds raw text from Project Gutenberg source, outputting txt files and reference csv.
"""
from tqdm import tqdm
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_metadata
from gutenberg._domain_model.exceptions import CacheAlreadyExistsException
from pathlib import Path
import pandas as pd
import pickle
import shutil
import os


def gather_text(era):
    parent_dir = Path(__file__).parents[1]
    
    # run the following ONLY ONCE
    from gutenberg.acquire import get_metadata_cache
    print("Defining cache...")
    cache = get_metadata_cache()
    print("Populating cache...")
    try:
        cache.populate()
    except CacheAlreadyExistsException:
        pass
    print("Successful cache build!")
    
    
    # the following are all the manually-selected text from pages search term 'Russia', 'Moscow', and 'Soviet'
    text_IDs = pickle.load(open(parent_dir / 'data' / 'text_ids' / f'IDs_{era}.pickle', 'rb'))
    
    assert len(text_IDs) == len(set(text_IDs)) # test for no duplicate IDs
    
    #  output files for corpus
    #  delete and remake dir to hold raw text files
    if os.path.isdir(f'{parent_dir}/data/raw_texts'):
        print("Deleting existing raw text directory")
        shutil.rmtree(f'{parent_dir}/data/raw_texts')
        os.mkdir(f'{parent_dir}/data/raw_texts')
        print("Created new raw text directory")
    else:
        os.mkdir(f'{parent_dir}/data/raw_texts')
        print("Created new raw text directory")
    text_details = {}
    for ID in tqdm(text_IDs, desc="Gathering texts"):
        try:
            tt = next(iter(get_metadata('title', ID)))
        except StopIteration:
            pass
        try:
            ta = next(iter(get_metadata('author', ID)))
        except StopIteration:
            pass
        td =  "YEAR" # publication year not include in metadata, dummy variable
        tc = strip_headers(load_etext(ID)).strip().replace("\n", " ")
        text_details[ID] = {"title": tt, "author": ta, "date": td}    
        with open(f'{parent_dir}/data/raw_texts/{ID}.txt', 'w') as output:
            output.write(tc)
            
    # reference table file for document details
    df = pd.DataFrame.from_dict(text_details,
                           orient='index',
                           columns=['title', 'author', 'date'])
    df.index.name = "ID"
    df.to_csv(f'{parent_dir}/data/reference.csv')
    
# parent_dir = Path(__file__).parent.parent

# #  output files for corpus
# #  delete and remake dir to hold raw text files
# if os.path.isdir(f'{parent_dir}/data/raw_texts'):
#     shutil.rmtree(f'{parent_dir}/data/raw_texts')
# else:
#     os.mkdir(f'{parent_dir}/data/raw_texts')