handle = '20141103\ All\ IRD'

def get_header(n_nodes):
	header = '\
#!/bin/sh \n\
#$ -S /bin/sh \n\
#$ -cwd \n\
#$ -V\n\
#$ -m e\n\
#$ -M ericmjl@mit.edu \n\
#$ -pe whole_nodes {0}\n\
#$ -l mem_free=2G\n\
#############################################\n\n'.format(n_nodes)

	return header

import os
import pickle as pkl 
import numpy as np

def check_dirs(dirname):
	if dirname not in os.listdir(os.getcwd()):
		os.mkdir(dirname)
	else:
		pass


check_dirs('shell_scripts')
check_dirs('reassortant_edges')

with open('20141103 All IRD Isolates for Source Pair Search.pkllist', 'r') as f:
	isolates = pkl.load(f)


num_per_batch = 20 # number of isolates to process at a time.
total_isolates = len(isolates)

# Check to see which isolates have been completed.
os.chdir('reassortant_edges')
completed = [int(f.split('.')[0].split(' '.format(handle))[5]) for f in os.listdir(os.getcwd()) if f.split('.')[1] == 'pkl']
print(completed)
os.chdir('..')
not_completed = []

for start in np.arange(0, total_isolates):
	if start not in completed:
		not_completed.append(start)
		with open('shell_scripts/source_pair/source_pair{0}.sh'.format(start), 'w') as f:
			f.write(get_header(1))

			f.write('cd ..\n')
			f.write('cd ..\n')

			f.write('python source_pair.py {0} {1} {2}'.format(handle, start, start + 1))

with open('shell_scripts/source_pair_manual.sh', 'w') as f:
	f.write(get_header(1))
	f.write('cd source_pair\n')	
	for start in not_completed:
		f.write('qsub source_pair{0}.sh\n'.format(start))