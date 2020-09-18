"""
Visualization of topics.
"""
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()


def joint_plot(num_topics, df, era, topic, save_path):
    if era == '20th':
        era_color = 'red'
    else:
        era_color = 'blue'
    ax = sns.jointplot(x="year",
                       y=topic,
                       kind="scatter",
                       color=era_color,
                       data=df)
    ax.set_axis_labels("Year", f'{topic.capitalize()} Frequency')
    ax.savefig(save_path / 'joint_plots' / f'{era}_{topic}_jointplot.png',
               dpi=600
               )
    del ax
    plt.clf()


def line_plot(df, era, topics, save_path):
    print("Generating line plot...")
    long_df = df.set_index('year')
    long_df = long_df.reset_index()
    long_df = pd.melt(long_df, id_vars="year", value_vars=topics)
    long_df.rename({"variable": "Topic"}, axis=1, inplace=True)
    # make wider plot
    plt.figure(figsize=(20, 6))
    ax = sns.lineplot(x="year",
                      y="value",
                      hue="Topic",
                      ci=None,
                      data=long_df,
                      legend='brief'
                      )
    ax.set_xlabel("Year")
    ax.set_ylabel(f'Topic Frequency')
    ax.set_title(f"Topic Frequencies over the {era}-century Portion of the Corpus")
    ax.figure.savefig(save_path / 'line_plots' / f'{era}_lineplot.png',
                      dpi=600
                      )


def bar_plot(df, era, save_path):
    print("Generating bar plot...")
    totals = df.drop(['title', 'ID', 'year'], axis=1).sum(axis=0)
    normalized = totals/totals.sum() * 100
    norm_df = pd.DataFrame(normalized).reset_index()
    norm_df.columns = ['topic', 'percent']
    plt.figure(figsize=(10, 10))
    ax = sns.barplot(x=norm_df['topic'],
                     y=norm_df['percent'],
                     )
    # add values above bars
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x()+p.get_width()/2,
                height + 0.25,
                f"{round(height,2)}%",
                fontsize=12,
                ha='center')
    ax.set_xlabel("Topic")
    ax.set_ylabel(f'Percent of Corpus')
    ax.set_title(f"Topic Composition of the {era}-century Portion of the Corpus")
    ax.figure.savefig(save_path / 'bar_plots' / f'{era}_barplot.png',
                      dpi=600
                      )


def visualize(era):
    parent_dir = Path(__file__).parents[1]
    figure_dir = parent_dir / 'figures'
    topics_df = pd.read_csv(parent_dir / f'data/{era}_topics.csv')
    num_topics = len(topics_df.columns) - 3
    topics = [f'topic_{i}' for i in range(num_topics)]

    # join plots for topic frequency and time
    for i in tqdm(range(num_topics), desc="Generating joint plots"):
        topic = f'topic_{i}'
        joint_plot(num_topics, topics_df, era, topic, figure_dir)
    
    # total percentages of corpus by topic
    bar_plot(topics_df, era, figure_dir)

    # All topic frequencies line chart
    line_plot(topics_df, era, topics, figure_dir)

    print("Visualization complete")

if __name__ == "__main__":
    visualize('20th')
