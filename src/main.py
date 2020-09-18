
"""
Driver script for entire process.
"""
from gatherTexts import gather_text
from genCorpus import generate_corpus
from util_year import utility_year
from modeling import model_topics
from visualization import visualize
from tqdm import tqdm


def run_program():
    era = input("Select '19th' or '20th' as era for analysis: ")
    for i in tqdm(range(5), desc="Generating and visualizing topics..."):
        # this loop is necessary for the progress bar
        if i == 0:
            gather_text(era)
        elif i == 1:
            generate_corpus()
        elif i == 2:
            utility_year()
        elif i == 3:
            # n_topics is 8 by default, n_iterations is 300 by default
            model_topics(era=era)
        elif i == 4:
            # visualization
            visualize(era)
    print("\nProcess complete.")


if __name__ == "__main__":
    run_program()
