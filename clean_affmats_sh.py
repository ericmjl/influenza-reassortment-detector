handle = "20150902_all_ird"

def get_header(n_nodes):
	header = '\
#!/bin/sh \n\
#$ -S /bin/sh \n\
#$ -cwd \n\
#$ -V\n\
#$ -m e\n\
#$ -M ericmjl@mit.edu \n\
#$ -pe whole_nodes {0}\n\
#############################################\n\n'.format(n_nodes)

	return header

import os

def check_dirs(dirname):
	if dirname not in os.listdir(os.getcwd()):
		os.mkdir(dirname)
	else:
		pass

check_dirs('shell_scripts')
check_dirs('distmats')
check_dirs('affmats')


for segment in range(1,9):
	with open('shell_scripts/clean_affmats{0}.sh'.format(segment), 'w') as f:
		f.write(get_header(n_nodes=1))

		f.write('cd ..\n')

		f.write('python clean_affmats.py {0} {1}'.format(handle, segment))

with open('shell_scripts/clean_affmats.sh', 'w') as f:
	f.write(get_header(n_nodes=1))

	for segment in range(1,9):
		f.write('qsub clean_affmats{0}.sh\n'.format(segment))
		f.write('sleep 180\n')
