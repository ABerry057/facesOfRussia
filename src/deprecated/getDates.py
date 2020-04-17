"""
Gets dates from probable ISBN codes.
"""

from tqdm import tqdm
from isbnlib import isbn_from_words, meta
import pandas as pd

from pathlib import Path

parent_dir = Path(__file__).parent.parent

ref_df = pd.read_csv(f'{parent_dir}/data/reference.csv')

isbns = []
for _,row in tqdm(ref_df.iterrows(), desc='Retrieving ISBNs'):
    title = row['title']
    author = row['author']
    try:
        isbn = isbn_from_words(title + author)
        if isbn is None:
            isbn = '0'
    except UnboundLocalError:
        isbn = '0'
    isbns.append(isbn)

dates = []
for i in tqdm(isbns, desc='Retrieving dates'):
    if i == '0':
        date = 0
    else:
        date = meta(str(i))
    dates.append(date['Year'])