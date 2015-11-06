import tables as tb
import sys 
import networkx as nx
import numpy as np
import pandas as pd

class MaxEdgeFinder(object):
	"""docstring for MaxEdgeFinder"""
	def __init__(self, handle, node_idx):
		super(MaxEdgeFinder, self).__init__()
		self.handle = handle
		self.df = None # full transmission store; conventionally I have used the letter 'f' for brevity
		self.G = None # graph - conventionally, I use G for brevity
		self.node_idx = node_idx
		self.isolate = None
		self.earlier_nodes = []
		self.row = None # row of PWIs from the data store
		self.older_pwis = None
		self.best_older_nodes = None
		self.maxpwi = 0.0

	def run(self):
		self.open_summed_affmats()
		self.open_initialized_network()
		self.get_isolate()
		self.get_nodes_earlier_in_time()
		# self.get_pwis_for_sink()
		self.get_older_pwis()
		self.get_maxpwi()
		self.get_earlier_nodes_of_highest_pwi()
		self.add_best_older_nodes()
		self.write_graph()


	def open_summed_affmats(self):
		"""
		Opens the full transmission HDF5 store.
		"""
		print('Opening summed affmats...')
		self.df = pd.read_hdf('{0} Summed Affmats.h5'.format(self.handle), key='full')

	def open_initialized_network(self):
		"""
		Opens the initialized network.
		"""
		print('Opening initialized network...')
		self.G = nx.read_gpickle('{0} Initialized Graph.pkl'.format(self.handle))

	def get_isolate(self):
		self.isolate = sorted(self.G.nodes())[self.node_idx]
		print('Isolate: {0}'.format(self.isolate))

	def get_nodes_earlier_in_time(self):
		print('Getting earlier nodes...')
		isolate_date = self.G.node[self.isolate]['collection_date']
		
		for n, d in self.G.nodes(data=True):
			if d['collection_date'] < isolate_date:
				self.earlier_nodes.append(n)

	# def get_pwis_for_sink(self):
	# 	print('Getting PWIs for isolate...')
	# 	self.df = self.df.loc[self.isolate]

	def get_older_pwis(self):
		print('Getting older PWIs...')
		self.older_pwis = self.df.loc[self.isolate].loc[self.earlier_nodes].fillna(0)
		print(self.older_pwis)

	def get_maxpwi(self):
		self.maxpwi = self.older_pwis.max()
		print('MaxPWI: {0}'.format(self.maxpwi))

	def get_earlier_nodes_of_highest_pwi(self):
		print('Getting nodes of highest MaxPWI...')
		if self.older_pwis.max() > 0:
			bestmatch_pos = self.older_pwis[self.older_pwis == self.older_pwis.max()]
			print(bestmatch_pos)

			self.best_older_nodes = list(bestmatch_pos.index)
		else:
			self.best_older_nodes = []
		print('Best older nodes:')
		print(self.best_older_nodes)

	def add_best_older_nodes(self):
		if len(self.best_older_nodes) > 0:
			for source in self.best_older_nodes:
				segments_dict={i:None for i in range(1,9)}
				self.G.add_edge(source, self.isolate, pwi=self.maxpwi, edge_type='full_complement', segments=segments_dict)

	def write_graph(self):
		"""
		Note: Only writes the subgraph induced by nodes involved in an edge, if an edge is found.
		Note: If no edge is found, then write to a text file the name of the node that has no edge.
		"""
		print('Writing graph...')
		nodes_involved = set()
		if len(self.G.edges()) > 0:
			for sc, sk in self.G.edges():
				nodes_involved.add(sc)
				nodes_involved.add(sk)

			subG = self.G.subgraph(nodes_involved)
			nx.write_gpickle(subG, 'edges/{0} Job {1} Edges.pkl'.format(self.handle, self.node_idx))
		else:
			print('No edges found.')
			with open('edges/{0} Job {1} Edges.txt'.format(self.handle, self.node_idx), 'w') as f:
				f.write("No edges found for {0}".format(self.isolate))
			subG = self.G.subgraph(self.isolate)
			nx.write_gpickle(subG, 'edges/{0} Job {1} Edges.pkl'.format(self.handle, self.node_idx))


if __name__ == '__main__':
	handle = sys.argv[1]
	node_idx_start = int(sys.argv[2])
	node_idx_end = int(sys.argv[3])

	for node_idx in range(node_idx_start, node_idx_end):

		mef = MaxEdgeFinder(handle, node_idx)
		mef.run()






