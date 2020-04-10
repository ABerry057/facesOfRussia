"""
Visualization of topics.
"""
import pandas as pd
import seaborn as sns
from tqdm import tqdm
from pathlib import Path

parent_dir = Path(__file__).parent.parent

topics_df = pd.read_csv(f'{parent_dir}/data/topics.csv')

# sns.distplot(topics_df['year'])
# sns.lineplot(x="year",y="topic_0", data = topics_df)
sns.jointplot(x="year", y="topic_8", data=topics_df)
