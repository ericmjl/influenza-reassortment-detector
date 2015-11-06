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
#$ -l mem_free=2G\n\
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

with open('shell_scripts/compile_affmats.sh', 'w') as f:
	f.write(get_header(n_nodes=1))
	f.write('cd .. \n')
	f.write('python compile_affmats.py {0}\n'.format(handle))
