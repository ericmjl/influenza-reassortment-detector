import networkx as nx 
import numpy as np
import pickle as pkl
import sys

class SecondSearchIdentifier(object):
	"""
	SecondSearchIdentifier

	Identifies isolates for which a source pair search will be performed. 
	"""
	def __init__(self, handle, percentile):
		super(SecondSearchIdentifier, self).__init__()
		self.handle = handle
		self.percentile = percentile
		self.G = None
		self.pwi_distribution = []
		self.cutoff_pwi = None
		self.source_pair_nodes = []

	def run(self):
		self.G = nx.read_gpickle('{0} Full Complement Graph.pkl'.format(self.handle))
		self.identify_sourceless_isolates()
		self.get_pwi_distribution()
		self.compute_cutoff_pwi()
		self.identify_lowpwi_isolates()
		self.write_second_search_list()
	
	def identify_sourceless_isolates(self):
		for n, d in self.G.nodes(data=True):
			if len(self.G.in_edges(n)) == 0:
				self.source_pair_nodes.append(n)

	def get_pwi_distribution(self):
		for n1, n2, d in self.G.edges(data=True):
			self.pwi_distribution.append(d['pwi'])

	def compute_cutoff_pwi(self):
		self.cutoff_pwi = np.percentile(self.pwi_distribution, self.percentile)

	def identify_lowpwi_isolates(self):
		for n1, n2, d in self.G.edges(data=True):
			if d['pwi'] < self.cutoff_pwi:
				self.source_pair_nodes.append(n2)

	def write_second_search_list(self):
		with open('{0} Isolates for Source Pair Search.pkllist'.format(self.handle), 'wb') as f:
			pkl.dump(self.source_pair_nodes, f)


if __name__ == '__main__':
	handle = sys.argv[1]
	percentile = int(sys.argv[2])

	ssi = SecondSearchIdentifier(handle, percentile)
	ssi.run()