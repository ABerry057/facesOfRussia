"""
Builds corpus from Project Gutenberg source.
"""
from tqdm import tqdm
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata

# run the following ONLY ONCE
# from gutenberg.acquire import get_metadata_cache
# cache = get_metadata_cache()
# cache.populate()
# print("Successful cache build!")

# the following are all the manually-selected text from pages 0-1 of search term 'Russia'
text_IDs_p01 = [21889,15269,58794,49782,23094,27484,51410,33005,
            21216,16544,12458,10713,33303,2803,39166,24181,
            28295,2480,49637,36945,50011,60432,26007,48992,
            51117,61557,60770,42132,51993,57185,40666,46510,
            5310,11980,58932,27103,5293,46019,18165,
            26090,30457,19714,22060,27366,54823,48737,50023,
            31860,12328,21461,60086,13806,60791,41091]

texts = {}
for ID in tqdm(text_IDs_p01):
    # tt = get_metadata('title', ID)
    # ta = get_metadata('author', ID)
    # td =  "YEAR"
    tc = strip_headers(load_etext(ID)).strip()
    # texts[ID] = {"title": tt, "author": ta, "date": td, "content": tc}
    texts[ID] = {"content": tc}

