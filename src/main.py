
"""
Driver script for entire process.
"""
from util_split import source_and_split
from gather_texts import gather_text
from generate_corpus import generate_corpus
from util_year import utility_year
from modeling import model_topics
from visualization import visualize
from tqdm import tqdm


def run_program():
    """
    Driver function for the text collection, processing,
    topic modeling, and visualization scripts.
    """
    era = input("Select '19th' or '20th' as era for analysis: ")
    for i in tqdm(range(6), desc="Generating and visualizing topics..."):
        # this loop is necessary for the progress bar
        if i == 0:
            source_and_split()
        elif i == 1:
            gather_text(era)
        elif i == 2:
            generate_corpus()
        elif i == 3:
            utility_year()
        elif i == 4:
            # n_topics is 8 by default, n_iterations is 300 by default
            model_topics(era=era)
        elif i == 5:
            # visualization
            visualize(era)
    print("\nProcess complete.")


if __name__ == "__main__":
    run_program()
