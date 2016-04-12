import os
import networkx as nx
import sys


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


def check_dirs(dirname):
    if dirname not in os.listdir(os.getcwd()):
        os.mkdir(dirname)
    else:
        pass

if __name__ == '__main__':

    shhandle = sys.argv[1]
    pyhandle = shhandle

    check_dirs('edges')
    check_dirs('shell_scripts/max_edge_finder')

    G = nx.read_gpickle('{0} Initialized Graph.pkl'.format(pyhandle))

    batch_size = 1000

    for idx in range(0, len(G.nodes()), batch_size):
        with open('shell_scripts/max_edge_finder/max_edge_finder{0}.sh'.format(
                idx), 'w+') as f:
            f.write(get_header(n_nodes=4))

            f.write('cd ..\n')
            f.write('cd ..\n')

            f.write('python max_edge_finder.py {0} {1} {2}'.format(shhandle,
                                                                   idx,
                                                                   idx +
                                                                   batch_size))

    with open('shell_scripts/max_edge_finder.sh', 'w') as f:
        f.write(get_header(n_nodes=1))
        f.write('cd max_edge_finder\n')

        for idx in range(0, len(G.nodes()), batch_size):

            f.write('qsub max_edge_finder{0}.sh\n'.format(idx))
            f.write('sleep 5\n')
