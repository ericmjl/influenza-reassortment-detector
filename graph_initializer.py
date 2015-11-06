import pandas as pd
import networkx as nx 
import sys

class GraphInitializer(object):
	"""docstring for GraphInitializer"""
	def __init__(self, handle):
		super(GraphInitializer, self).__init__()
		self.handle = handle
		self.data = None
		self.G = nx.DiGraph()

	def run(self):
		self.read_data()
		self.create_initialized_graph()
		self.save_graph()

	def read_data(self):
		self.data = pd.read_csv('{0} Full Isolates.csv'.format(self.handle), index_col=0, parse_dates=['Collection Date'], na_filter=False)
		
	def create_initialized_graph(self):
		columns_of_interest = {'Collection Date':'collection_date',
							   'Host Species':'host_species',
							   'Country':'country',
							   'State/Province':'state',
							   'Strain Name':'strain_name',
							   'Subtype':'subtype'}
		cols = [i for i in columns_of_interest.keys()]
		for group, data in self.data.groupby(cols):
			attr_dict = dict()
			strain_name = ''
			for val in group:
				colname = cols[group.index(val)]
				if colname != 'Strain Name':
					attr_dict[columns_of_interest[colname]] = val
				if colname == 'Strain Name':
					strain_name = val
			self.G.add_node(strain_name, attr_dict=attr_dict)


	def save_graph(self):
		nx.write_gpickle(self.G, '{0} Initialized Graph.pkl'.format(self.handle))



if __name__ == '__main__':

	handle = sys.argv[1]

	gi = GraphInitializer(handle)
	gi.run()