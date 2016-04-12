# influenza-reassortment-detector
Scripts for running the influenza reassortment detector

# Instructions

## Requirements
 
- The code for this analysis were run on the [MIT Rous][1] cluster, which is equipped with the SunGrid Engine scheduler. This set of scripts was written with the assumption that they would be run on a computing cluster equipped with SGE, to deal with the large amount of data that results from it.
- Python 3.4 and packages:
    - pytables
    - pandas
    - networkx
    - numpy
    - biopython
- You should also be comfortable working at the command line.

## Conventions

- The variable `$HANDLE` refers to the unique identifier for the project at hand. 
- Each step listed below will have a high-level overview of the purpose of each of the scripts involved, followed by the exact command to enter in the terminal.
- The `$` character at the beginning of each line is for the terminal prompt, and does not need to be typed in.

## Steps

### Initialize directory

**Purpose:** To create the necessary directories, and ensure that the necessary script files are present.

**To run:** 

- `$ python check_dir.py`

### Preprocess CSV file

**Purpose:** The script `preprocessing.py` will identify isolates for which whole genome sequence are available, and clean the metadata associated with it.

**To run:** 

- `$ python preprocessing.py "$HANDLE"`

### Split FASTA file by segment

**Purpose:** The data downloaded from the [IRD][2] would be a single, large FASTA file. The scripts `sequence_splitter_sh.py` and `sequence_splitter.py` will split the single FASTA file into 8 FASTA files by segment.

**To run:**

- Open up the script `sequence_splitter_sh.py`, and change the `handle` variable at the top of the script to your `$HANDLE`.
- `$ python sequence_splitter_sh.py`
- `$ cd shell_scripts`
- `$ qsub sequence_splitter.sh`
- `$ cd ..`
- Wait until all of the jobs have finished running. Under the directory `/split_fasta/` you should see 8 FASTA files, one from each segment.
- This step should take on the order of minutes to complete, depending on your CPU speed. Memory requirements are not high.

### Generate alignment and distance matrix

**Purpose:** As the title suggests, perform a multiple sequence alignment on all of the sequences, and compute the distance matrix from the alignment.

**To run:**

- Open up the script `align_sh.py`, and modify the `handle` variable at the top of the script to your `$HANDLE`.
- `$ python align_sh.py`
- `$ cd shell_scripts`
- `$ qsub align.sh`
- `$ cd ..`
- Wait until all of the jobs have finished running. On a large dataset, this may take hours to days to finish, depending on CPU load.

### Convert distance matrix into similarity matrix and threshold

**Purpose:** In this step, the distance matrix will be converted into a similarity matrix, and thresholded based on previously-computed/defined thresholds.

**To run:**

- `$ python clean_affmats_sh.py $HANDLE`
- `$ cd shell_scripts`
- `$ qsub clean_affmats.sh`
- `$ cd ..`

Wait until all of the jobs have been completed.

Compute thresholds (if not pre-computed elsewhere)

- `$ qlogin`
- `$ cd /path/to/project/directory`
- `$ python thresholds.py $HANDLE`
- This step should take on the order of 30 minutes for a small dataset (~5000 isolates).
- When done, exit the `qlogin` session: `$ exit`

Compile the similarity matrices (affmats) together.

- `$ python compile_affmats_sh.py $HANDLE`
- `$ cd shell_scripts`
- `$ qsub compile_affmats.sh`
- `$ cd ..`
- Wait until all of the jobs have been completed.

### Sum similarity matrix

**Purpose:** This convenience step creates a summed similarity matrix from the thresholded similarity matrices. NOTE: Large amounts of RAM are required.

**To run:**

- Login to a compute node for interactive work, by running `$ qlogin`. For the complete set of IRD sequences, approximately 27GB of RAM should be required.
- `$ cd path/to/project` (remember to change the directory path as appropriate)
- `$ python full_affmat.py $HANDLE`
- When done, exit out of the `qlogin` session: `$ exit`

This step should take a few minutes. 

### Search for edges of maximal similarity

**Purpose:** The scripts here will search for clonal descent edges that represent maximal similarity.

**To run:**

- `$ python graph_initializer.py $HANDLE`
- Open up the script `max_edge_finder.sh`, and edit the `batch_size` variable. There is an art to determining the batch size, as a smaller batch size allows for faster runtimes per SGE job, but more jobs are required.
- `$ python max_edge_finder_sh.py $HANDLE`
- `$ cd shell_scripts`
- `$ qsub max_edge_finder.sh`
- `$ cd ..`
- Expect this step to take a long time (~1 day)
- Also note that the final batch will return exit code 1, which is normal.

### Combine found edges into a condensed graph.

**Purpose:** To combine the found edges into a single `networkx` graph.

**To run:**

- `$ python graph_combiner.py $HANDLE`
- This step should run within minutes.

### Compile a list of nodes to perform source pair searches on.

**Purpose:** To decide which edges' sinks to reconsider as likely to be reassortant instead of clonal descent. 

**To run:**

- Determine a percentile cutoff; in the manuscript, we used a 10th percentile cutoff, so the `$PERCENTILE` variable below was `10`.
- `$ python second_search.py $HANDLE $PERCENTILE`

### Perform source pair searches

**Purpose:** The set of scripts here will look amongst the isolates for the max similarity source pair.

**To run:**

- Open up the script `source_pair_sh.py` and change:
    - The number of compute slots and RAM requirement in the `get_header` function call.
    - The number of isolates to process per batch.
- Run the source pair finder: `$ python source_pair_sh.py $HANDLE`
- `$ cd shell_scripts`
- `$ qsub source_pair.sh`
- `$ cd ..`

Wait for the job to finish completing. This may take a day or so to complete.

### Generate final graph for analysis

**Purpose:** The scripts here will combine the edges together into a single graph, annotate PWIs, and check and clean the graph edges' integrity.

**To run:**

- `$ python source_pair_combiner.py $HANDLE`
- `$ python graph_pwi_finder.py $HANDLE`
- `$ python graph_cleaner.py $HANDLE`
- Each script should be fast and take on the order of minutes.

At this point, you should see a file: `$HANDLE_Final Graph.pkl`. This is the graph file that gets used with downstream analyses.




[1]: http://rous.mit.edu/
[2]: http://www.fludb.org/