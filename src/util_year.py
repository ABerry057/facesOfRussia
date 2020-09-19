#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility script to add years to reference.csv
"""
import pandas as pd
from tqdm import tqdm
from pathlib import Path


def utility_year():
    """Adds years to reference data table that come from
    manual research to make up for the lack of metadata from
    Gutenberg API.
    """
    parent_dir = Path(__file__).parents[1]

    reference_df = pd.read_csv(parent_dir / 'data/reference.csv')
    year_df = pd.read_csv(parent_dir / 'data/reference_backup.csv')

    year_dict = {}
    for ID in tqdm(year_df['ID'], desc='Getting years from ID'):
        year_dict[ID] = year_df[year_df['ID'] == ID]['date'].values[0]

    for ID in tqdm(year_df['ID'], desc='Adding years by ID'):
        if ID in reference_df['ID'].values:
            # print("Found ID to join with!")
            row_id = reference_df.loc[reference_df['ID'] == ID].index
            year = year_dict[ID]
            # print(f'Changing date to {year}')
            reference_df.at[row_id, 'date'] = year

    reference_df.to_csv(parent_dir / 'data/reference.csv', index=False)

