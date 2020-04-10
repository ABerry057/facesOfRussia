"""
Builds raw text from Project Gutenberg source, outputting txt files and reference csv.
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
# text_IDs_test = [21889, 15269, 58794]


# the following are all the manually-selected text from pages search term 'Russia', 'Moscow', and 'Soviet'
text_IDs = [21889,15269,58794,49782,23094,27484,51410,33005,
            21216,16544,12458,10713,33303,2803,39166,24181,26051,
            28295,2480,49637,50011,60432,26007,48992,46813,
            51117,61557,60770,42132,51993,57185,46510,45098,42967,
            5310,11980,58932,27103,46019,18165,1349,12349,10972,
            26090,30457,27366,48737,50023,20880,22095,41237,45845,
            31860,12328,21461,60086,13806,60791,41091,38357,15921,
            40907,32370,59095,56611,48373,61235,8158,8873,10132,
            45167,26390,22523,25625,55244,46587,54507,57804,60315,
            54059,31554,16930,60258,46023,35540,5996,24981,22004,
            53108,16981,49278,27733,7320,7973,18643,45099,37723,
            37724,3488,19534,57750,51594,37889,37947,45299,17350,
            3485,16613,60173]

assert len(text_IDs) == len(set(text_IDs)) # test for no duplicate IDs



# output file for corpus
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
