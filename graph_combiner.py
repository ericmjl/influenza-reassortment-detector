import pandas as pd
import networkx as nx 
import sys
import os

class GraphCombiner(object):
    """docstring for GraphCombiner"""
    def __init__(self, handle):
        super(GraphCombiner, self).__init__()
        self.handle = handle
        self.G = nx.read_gpickle('{0} Initialized Graph.pkl'.format(handle))
        self.current_g = None

    def run(self):
        for f in os.listdir('edges'):
            print(f)
            if f.split('.')[1] == 'pkl':
                
                f = 'edges/{0}'.format(f)

                self.current_g = nx.read_gpickle(f)
                self.copy_nodes_and_edges()

        nx.write_gpickle(self.G, '{0} Full Complement Graph.pkl'.format(self.handle))
        print('{0} Nodes'.format(len(self.G.nodes())))
        print('{0} Edges'.format(len(self.G.edges())))



    def copy_nodes_and_edges(self):
        for n, d in self.current_g.nodes(data=True):
            self.G.add_node(n, attr_dict=d)

        if len(self.current_g.edges()) > 0:
            for n1, n2, d in self.current_g.edges(data=True):
                self.G.add_edge(n1, n2, attr_dict=d)

if __name__ == '__main__':

    handle = sys.argv[1]

    gc = GraphCombiner(handle)
    gc.run()
