
"""
Driver script for entire process.
"""
from gatherTexts import gt
from genCorpus import gc
from util_year import uy
from modeling import model
from visualization import vis
from tqdm import tqdm


def run_program():
    for i in tqdm(range(5), desc="Generating and visualizing topics..."):
        # this otherwise unnecessary for-loop enables the progress bar
        if i == 0:
            # gather texts
            gt()
        elif i == 1:
            # generate corpus
            gc()
        elif i == 2:
            # year utility script
            uy()
        elif i == 3:
            # modeling, n_topics is 8 by default, n_iterations is 3000 by default
            model()
        elif i == 4:
            # visualization
            vis()
    print("\nProcess complete.")


if __name__ == "__main__":
    run_program()
