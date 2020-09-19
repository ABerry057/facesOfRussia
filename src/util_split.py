"""
Source and split text ID utility

"""
import pandas as pd
from pathlib import Path
import pickle


def read_ID_list(file_name, data_dir):
    """Reads the ID list from a previously-created text file.

    Parameters
    ----------
    file_name : [POSIX path]
       Name of text file holding text IDs for Gutenberg API.
    data_dir : POSIX path
        Directory pointing to project data

    Returns
    -------
    list
        List of text IDs for analysis
    """
    with open(data_dir / file_name, 'r') as ID_file:
        text_IDs = ID_file.read().split(',')
    text_IDs = [int(id) for id in text_IDs]
    return text_IDs


def split_IDs_by_date(text_IDs, threshold, reference_df, data_dir):
    """Splits text IDs into two groups according to a text's publication
    date. The Gutenberg API does not supply publication metadata so this
    might have to be gathered manually.
    Saves the separated IDs into pickle files.

    Parameters
    ----------
    text_IDs : list
        List of text IDs for analysis
    threshold : int
        Year with which to split corpus (Ex. 1900)
    reference_df : dataframe
        Table mapping and ID to a text's publication date
    data_dir : POSIX path
        Directory pointing to project data
    """
    IDs_before = []
    IDs_after = []
    for ID in text_IDs:
        if reference_df[reference_df['ID'] == ID]['date'].values[0] >= threshold:
            IDs_before.append(ID)
        else:
            IDs_after.append(ID)

    pickle.dump(IDs_before, open(data_dir / 'text_IDs' / 'IDs_19th.pickle', "wb"))
    pickle.dump(IDs_after, open(data_dir / 'text_IDs' / 'IDs_20th.pickle', "wb"))


def source_and_split():
    """Sources text IDs from supplied file and performs splitting
    and saving process.
    """
    parent_dir = Path(__file__).parents[1]
    data_dir = parent_dir / 'data'
    text_IDs = read_ID_list('russia_IDs.txt', data_dir)

    reference_bdf = pd.read_csv(data_dir / 'reference_backup.csv')

    year_threshold = 1900
    split_IDs_by_date(text_IDs, year_threshold, reference_bdf, data_dir)


if __name__ == "__main__":
    source_and_split()
