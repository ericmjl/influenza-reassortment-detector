import networkx as nx 
import sys
import pandas as pd

class GraphPWIFinder(object):
	"""docstring for GraphPWIFinder"""
	def __init__(self, handle, segment_stores):
		super(GraphPWIFinder, self).__init__()
		self.handle = handle
		self.G = nx.read_gpickle('{0} Full and Reassortant Graph.pkl'.format(self.handle))
		# self.store = tb.open_file('{0} Segment Affmats.h5'.format(self.handle))
		self.segment_stores = segment_stores

	def get_pwi(self, segment, source, sink):
		pwi = self.segment_stores[segment].loc[source, sink]

		return pwi

	def save_output(self):
		nx.write_gpickle(self.G, '{0} Graph with PWIs.pkl'.format(self.handle))

	def run(self):
		for sc, sk, d in self.G.edges(data=True):
			for seg, val in d['segments'].items():
				pwi = self.get_pwi(seg, sc, sk)
				self.G.edge[sc][sk]['segments'][seg] = pwi
			print(self.G.edge[sc][sk])

		self.save_output()


if __name__ == '__main__':
	handle = sys.argv[1]

	segment_stores = dict()
	for i in range(1,9):
		print('Getting segment {0} store.'.format(i))
		segment_stores[i] = pd.read_hdf('{0} Thresholded Segment Affmats.h5'.format(handle), key='segment{0}'.format(i))

	gc = GraphPWIFinder(handle, segment_stores)
	gc.run()

