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
    """Creates a reference data table for texts from the given era.
    Saves the table with text ID, title, author, and dummy year variable.
    Loads text IDs from previously-created pickle file for appropriate era.
    Saves text content in separate directory for subsequent topic modeling.

    Parameters
    ----------
    era : str
        Century by which to divie the corpus.
        Either '19th' or '20th'.
    """
    parent_dir = Path(__file__).parents[1]

    # run the following once to acquire the metadata cache
    # not needed for subsequent runs
    from gutenberg.acquire import get_metadata_cache
    print("Defining cache...")
    cache = get_metadata_cache()
    print("Populating cache...")
    try:
        cache.populate()
    except CacheAlreadyExistsException:
        pass
    finally:
        print("Successful cache build!")

    # the following are manually-selected texts from search results for:
    #  'Russia', 'Moscow', and 'Soviet'
    text_IDs = pickle.load(open(parent_dir / 'data' / 'text_IDs' / f'IDs_{era}.pickle', 'rb'))
    assert len(text_IDs) == len(set(text_IDs))  # test for no duplicate IDs

    #  output files for corpus

    #  delete and remake dir to hold raw text files if needed
    if os.path.isdir(parent_dir / 'data' / 'raw_texts'):
        print("Deleting existing raw text directory")
        shutil.rmtree(parent_dir / 'data' / 'raw_texts')
        os.mkdir(parent_dir / 'data' / 'raw_texts')
        print("Created new raw text directory")
    else:
        os.mkdir(parent_dir / 'data' / 'raw_texts')
        print("Created new raw text directory")

    text_details = {}
    for ID in tqdm(text_IDs, desc="Gathering texts"):
        try:
            text_title = next(iter(get_metadata('title', ID)))
        except StopIteration:
            pass
        try:
            text_author = next(iter(get_metadata('author', ID)))
        except StopIteration:
            pass
        text_date = "YEAR"  # year not included in metadata, dummy variable
        text_content = strip_headers(load_etext(ID)).strip().replace("\n", " ")
        text_details[ID] = {"title": text_title,
                            "author": text_author,
                            "date": text_date
                            }
        with open(parent_dir / 'data' / f'raw_texts/{ID}.txt', 'w') as output:
            output.write(text_content)

    # reference table file for document details
    df = pd.DataFrame.from_dict(text_details,
                                orient='index',
                                columns=['title', 'author', 'date']
                                )
    df.index.name = "ID"
    df.to_csv(f'{parent_dir}/data/reference.csv')
