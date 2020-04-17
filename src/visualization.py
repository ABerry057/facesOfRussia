"""
Visualization of topics.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from pathlib import Path


def vis():
    parent_dir = Path(__file__).parent.parent
    figure_dir = f'{parent_dir}/figures'
    topics_df = pd.read_csv(f'{parent_dir}/data/topics.csv')
    num_topics = len(topics_df.columns) - 3
    topics = [f'topic_{i}' for i in range(num_topics)]
    
    # join plots for topic frequency and time
    for i in tqdm(range(num_topics),desc="Generating joint plots"):
        ax = sns.jointplot(x="year",
                            y=f'topic_{i}',
                            kind="scatter",
                            color="red",
                            data=topics_df)
        ax.set_axis_labels("Year", f'Topic {i} Frequency')
        ax.savefig(f'{figure_dir}/topic_{i}_jointplot.png',
                      dpi=600)
        del ax
        plt.clf()
        
    # All topic frequencies line chart
    long_df = topics_df.set_index('year')
    long_df = long_df.reset_index()
    long_df = pd.melt(long_df, id_vars="year", value_vars=topics)
    # make wider plot
    plt.figure(figsize=(20, 4))
    ax = sns.lineplot(x="year", y="value", hue="variable", ci=None, data = long_df)
    ax.set_xlabel("Year")
    ax.set_ylabel(f'Topic Frequency')
    ax.figure.savefig(f'{figure_dir}/line_chart.png',dpi=600)

if __name__ == "__main__":
    vis()
