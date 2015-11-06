import os
import pandas as pd 
import networkx as nx
import sys

class DataImputer(object):
	"""docstring for DataImputer"""
	def __init__(self, handle, graph_handle):
		super(DataImputer, self).__init__()
		self.handle = handle
		self.initialG = nx.read_gpickle('{0} Initialized Graph.pkl'.format(handle))
		self.G = nx.read_gpickle('{0} {1}'.format(handle, graph_handle))

	def run(self):
		self.impute_data()
		self.save_data()

	def impute_data(self):
		self.G.add_nodes_from(self.initialG.nodes(data=True))

	def save_data(self):
		nx.write_gpickle(self.G, '{0}'.format(graph_handle))

if __name__ == '__main__':
	handle = sys.argv[1]
	graph_handle = sys.argv[2]


	di = DataImputer(handle, graph_handle)
	di.run()
