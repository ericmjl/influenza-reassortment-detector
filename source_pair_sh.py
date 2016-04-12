import os
import pickle as pkl
import numpy as np
import sys


def get_header(n_nodes, ram):
    header = '\
#!/bin/sh \n\
#$ -S /bin/sh \n\
#$ -cwd \n\
#$ -V\n\
#$ -m e\n\
#$ -M ericmjl@mit.edu \n\
#$ -pe whole_nodes {0}\n\
#$ -l mem_free={1}G\n\
#############################################\n\n'.format(n_nodes, ram)
    return header


def check_dirs(dirname):
    if dirname not in os.listdir(os.getcwd()):
        os.mkdir(dirname)
    else:
        pass

if __name__ == '__main__':

    handle = sys.argv[1]

    check_dirs('shell_scripts')
    check_dirs('reassortant_edges')
    check_dirs('shell_scripts/source_pair')

    with open('{0} Isolates for Source Pair Search.pkllist'.format(handle),
              'rb') as f:
        isolates = pkl.load(f)

    num_per_batch = 550  # number of isolates to process at a time.
    total_isolates = len(isolates)

    for start in np.arange(0, total_isolates, num_per_batch):
        with open('shell_scripts/source_pair/source_pair{0}.sh'.format(start),
                  'w') as f:
            f.write(get_header(6, 20))

            f.write('cd ..\n')
            f.write('cd ..\n')

            f.write('python source_pair.py {0} {1} {2}'.format(handle,
                    start, start + num_per_batch))

    with open('shell_scripts/source_pair.sh', 'w') as f:
        f.write(get_header(1, 1))
        f.write('cd source_pair\n')
        for start in np.arange(0, total_isolates, num_per_batch):
            f.write('qsub source_pair{0}.sh\n'.format(start))
            f.write('sleep 5\n')
