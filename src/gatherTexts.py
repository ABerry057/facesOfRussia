"""
Builds raw text from Project Gutenberg source, outputting txt file.
"""
from tqdm import tqdm
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_metadata
from pathlib import Path
import pandas as pd

parent_dir = Path(__file__).parent.parent

# run the following ONLY ONCE
# from gutenberg.acquire import get_metadata_cache
# print("Defining cache...")
# cache = get_metadata_cache()
# print("Populating cache...")
# cache.populate()
# print("Successful cache build!")

# uncomment the following to build a toy corpus
# text_IDs_p02 = [21889, 15269, 58794]


# the following are all the manually-selected text from pages 0-2 of search term 'Russia'
text_IDs_p02 = [21889,15269,58794,49782,23094,27484,51410,33005,
            21216,16544,12458,10713,33303,2803,39166,24181,
            28295,2480,49637,36945,50011,60432,26007,48992,
            51117,61557,60770,42132,51993,57185,40666,46510,
            5310,11980,58932,27103,5293,46019,18165,
            26090,30457,19714,22060,27366,54823,48737,50023,
            31860,12328,21461,60086,13806,60791,41091, 38357,
            40907,32370,59095,56611,48373,61235,8158,8873,10132,
            45167,26390,22523,25625,22655,55244,46587,54507,
            54059,31554,16930,60258,46023,35540,5996,24981,22004,
            53108,16981,49278,27733,7320,7973,18643,45099,37723,
            37724,3488,19534,57750,51594,37889,37947,45299,]



# output file for corpus
text_details = {}
for ID in tqdm(text_IDs_p02, desc="Gathering texts"):
    try:
        tt = next(iter(get_metadata('title', ID)))
    except StopIteration:
        pass
    try:
        ta = next(iter(get_metadata('author', ID)))
    except StopIteration:
        pass  
    td =  "YEAR"
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