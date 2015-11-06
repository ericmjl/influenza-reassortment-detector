"""
Author: Eric J. Ma

Makes sure that the necessary files and directories are present.
"""

import os

# Make sure that the Python scripts are present.
files = os.listdir(os.getcwd())

expected = ['align_sh.py', 'align.py', 'clean_affmats_sh.py', 
            'clean_affmats.py', 'compile_affmats_sh.py', 'compile_affmats.py',
            'full_affmat.py', 'graph_combiner.py', 'graph_initializer.py', 
            'max_edge_finder_sh.py', 'max_edge_finder.py', 
            'node_data_imputer.py', 'preprocessing.py', 'second_search.py', 
            'sequence_splitter_sh.py', 'sequence_splitter.py', 
            'source_pair_combiner.py', 'source_pair_manual_sh.py', 
            'source_pair_sh.py', 'tables_functions.py']

for e in expected:
    assert e in files

print('All necessary files are present.')

# --------------------------------------------------------------------------- #
# Make sure that the directories are present. Use the same logic as above.
dirs = ['alignments', 'distmats', 'edges', 'reassortant_edges', 
        'shell_scripts', 'split_fasta', 'sge_outputs']

for d in dirs:
    if d not in os.listdir(os.getcwd()):
        os.mkdir(d)
    assert d in os.listdir(os.getcwd())

print('All necessary directories are present.')