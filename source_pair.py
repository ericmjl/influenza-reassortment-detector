import networkx as nx 
import numpy as np
import pickle as pkl
import pandas as pd
import tables as tb
import sys

from itertools import combinations

class SourcePairSearcher(object):
    """
    SourcePairSearcher

    Identifies isolates for which a source pair search will be performed. 
    """
    def __init__(self, handle, isolate_num, segment_stores):
        super(SourcePairSearcher, self).__init__()
        self.handle = handle
        # Open access the list of isolates for which source pairs are to be found.
        with open('{0} Isolates for Source Pair Search.pkllist'.format(self.handle), 'rb') as f:
            self.sink = pkl.load(f)[isolate_num]
            print(self.sink)

        self.isolate_num = isolate_num

        self.G = nx.read_gpickle('{0} Initialized Graph.pkl'.format(self.handle))
        # self.hdf5store = tb.open_file('{0} Segment Affmats.h5'.format(self.handle))
        self.older_nodes = []
        self.segment_stores = segment_stores

        self.maxpwi = 0
        self.sources = dict()


    def run(self):
        self.get_nodes_earlier_in_time()
        for n in range(1, 5):
            combs = self.segment_combinations(n)
            for comb in combs:
                print('Currently on combination:')
                print('{0}'.format(comb))
                comb1 = self.sum_subset_segment_pwis(comb[0])
                comb2 = self.sum_subset_segment_pwis(comb[1])

                sumpwi = comb1.max() + comb2.max()
                print("Sum PWI: {0}".format(sumpwi))
                if sumpwi < self.maxpwi:
                    pass
                else:
                    filtered1 = comb1[comb1 == comb1.max()]
                    filtered2 = comb2[comb2 == comb2.max()]

                    if sumpwi > self.maxpwi and not np.isnan(sumpwi):
                        self.sources = dict()
                        self.maxpwi = sumpwi

                    self.sources[comb[0]] = [i for i in filtered1.index]
                    self.sources[comb[1]] = [i for i in filtered2.index]


        print(self.maxpwi)

        self.add_edges()
        self.extract_nodes()
        self.save_graph()

    def add_edges(self):
        for segs, isolates in self.sources.items():
            for source in isolates:
                d = {'edge_type':'reassortant', 'pwi':self.maxpwi, 'segments':dict()}
                for s in segs:
                    d['segments'][s] = None
                self.G.add_edge(source, self.sink, attr_dict=d)

    def save_graph(self):
        nx.write_gpickle(self.G, 'reassortant_edges/{0} Reassortant Edges {1}.pkl'.format(self.handle, self.isolate_num))
    
    def extract_nodes(self):
        nodes_to_extract = set()
        for n1, n2 in self.G.edges():
            nodes_to_extract.add(n1)
            nodes_to_extract.add(n2)

        self.G = self.G.subgraph(nodes_to_extract)


    def get_segment_store(self, segment):
        """
        This helper function gets the particular store from the hdf5 set of stores.
        """

        self.segment_stores[segment] = pd.read_hdf('{0} Thresholded Segment Affmats.h5'.format(self.handle), key='segment{0}'.format(segment))

    def segment_combinations(self, n):
        """
        Here:
            n = number of segments from first source.
        Therefore, logically:
            !n = complement of segments from second source.
        """

        segments = set(range(1,9))
        return [(tuple(set(i)), tuple(segments.difference(i))) for i in combinations(segments, n)]

    def get_nodes_earlier_in_time(self):
        print('Getting earlier nodes...')
        isolate_date = self.G.node[self.sink]['collection_date']
        self.older_nodes = [n for n, d in self.G.nodes(data=True) if d['collection_date'] < isolate_date]


    def get_col(self, segment):
        """
        Gets the column of PWIs for the sink as a Pandas dataframe, filtered only to 
        older nodes.
        """
        df = self.segment_stores[segment].loc[self.older_nodes,self.sink]
        print(df)
        return df

    def sum_subset_segment_pwis(self, segments):
        """
        Returns the summed PWIs for a given subset of segments
        """
        sumpwis = None
        for i, segment in enumerate(segments):
            pwis = self.get_col(segment)
            if i == 0:
                sumpwis = pwis
            if i > 0:
                sumpwis = sumpwis + pwis

        sumpwis
        return sumpwis




    
if __name__ == '__main__':
    handle = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])

    def get_segment_store(segment):
        """
        This helper function gets the particular store from the hdf5 set of stores.
        """

        return pd.read_hdf('{0} Thresholded Segment Affmats.h5'.format(handle), key='segment{0}'.format(segment))

    segment_stores = dict()

    for segment in range(1,9):
        print('Getting segment {0} store'.format(segment))
        segment_stores[segment] = get_segment_store(segment)

    for i in range(start, end):
        sps = SourcePairSearcher(handle, i, segment_stores)
        sps.run()