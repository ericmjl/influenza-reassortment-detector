import networkx as nx 
import numpy as np
import pickle as pkl
import pandas as pd
import tables as tb
import sys
import os

from itertools import combinations

class SourcePairCombiner(object):
	"""
	SourcePairCombiner

	Combines the source pairs found into a full complement graph to yield a 
	"complete set" graph.

	One of two things happen for every source pair in the reassortant_edges graph. 
	Either:
	1. If the sink node has a full complement in_edge, then compare the reassoratnt_edge PWI to 
	   see if it beats out the full complement in_edge. If it does, replace, else pass.
	2. If the sink node doesn't have any full complement in_edges, then add in the source pair edges.
	"""
	def __init__(self, handle):
		super(SourcePairCombiner, self).__init__()
		self.handle = handle
		self.dirhandle = 'reassortant_edges'
		self.G = nx.read_gpickle('{0} Full Complement Graph.pkl'.format(self.handle))
		self.current_sourcepair = None # current sourcepair graph
		self.current_noi = None # current node of interest


	def run(self):
		for f in os.listdir('{0}'.format(self.dirhandle)):
			self.current_sourcepair = nx.read_gpickle('{0}/{1}'.format(self.dirhandle, f))
			# print(self.current_sourcepair.edges())
			if len(self.current_sourcepair.edges()) > 0:
				self.current_noi = self.get_node_of_interest()
				if self.noi_has_in_edge() == False:
					self.G.add_nodes_from(self.current_sourcepair.nodes(data=True))
					self.G.add_edges_from(self.current_sourcepair.edges(data=True))

				if self.noi_has_in_edge() == True:
					reassortant_pwi = self.get_reassortant_pwi()
					full_pwi = self.get_full_pwi()

					if reassortant_pwi > full_pwi:
						self.remove_full_edge()
						self.G.add_nodes_from(self.current_sourcepair.nodes(data=True))
						self.G.add_edges_from(self.current_sourcepair.edges(data=True))

		nx.write_gpickle(self.G, '{0} Full and Reassortant Graph.pkl'.format(self.handle))

	def noi_has_in_edge(self):
		if len(self.G.in_edges(self.current_noi)) > 0:
			return True
		else:
			return False

	def get_node_of_interest(self):
		noi = set()
		for n1, n2 in self.current_sourcepair.edges():
			noi.add(n2)
		print(noi)

		if len(noi) > 1:
			raise ValueError('There are more than one nodes of interest.')
		return list(noi)[0]

	# def add_reassortant_edges(self):
	# 	for n1, n2, d in self.current_sourcepair.edges(data=True):
	# 		self.G.add_edge(n1, n2, attr_dict=d)

	def remove_full_edge(self):
		for n1, n2 in self.G.in_edges(self.current_noi):
			self.G.remove_edge(n1, n2)

	def get_reassortant_pwi(self):
		# Note: I know this isn't very efficient, but they're all quite small...
		pwi = 0
		for n1, n2, d in self.current_sourcepair.edges(data=True):
			pwi = d['pwi']

		return pwi

	def get_full_pwi(self):
		pwi = 0
		for n1, n2, d in self.G.in_edges(self.current_noi, data=True):
			pwi = d['pwi']

		return pwi

	
if __name__ == '__main__':
	handle = sys.argv[1]

	sps = SourcePairCombiner(handle)
	sps.run()