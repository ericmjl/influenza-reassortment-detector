handle = "20150902_all_ird"

header = '\
#!/bin/sh \n\
#$ -S /bin/sh \n\
#$ -cwd \n\
#$ -V\n\
#$ -m e\n\
#$ -M ericmjl@mit.edu \n\
#$ -pe whole_nodes 1\n\
#############################################\n \n\
'

import os

def check_dirs(dirname):
	if dirname not in os.listdir(os.getcwd()):
		os.mkdir(dirname)
	else:
		pass

check_dirs('shell_scripts')
check_dirs('split_fasta')


for segment in range(1,9):
	with open('shell_scripts/sequence_splitter{0}.sh'.format(segment), 'w') as f:
		f.write(header)

		f.write('cd ..\n')

		f.write('python sequence_splitter.py {0} {1}'.format(handle, segment))

with open('shell_scripts/sequence_splitter.sh', 'w') as f:
	f.write(header)

	for segment in range(1,9):
		f.write('qsub sequence_splitter{0}.sh\n'.format(segment))
