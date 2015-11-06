"""
This script performs data preprocessing.
"""

import pandas as pd
import sys

from Bio import SeqIO

class SequenceSplitter(object):
	"""docstring for SequenceSplitter"""
	def __init__(self, handle, segment):
		super(SequenceSplitter, self).__init__()
		self.handle = handle
		self.df = None
		self.fasta = None
		self.segment = segment

	def run(self):
		self.read_full_isolates()
		self.read_full_fasta()
		self.write_segment_fasta()

	def read_full_isolates(self):
		self.df = pd.read_csv('{0} Full Isolates.csv'.format(self.handle), parse_dates=['Collection Date'], na_filter=False)

	def read_full_fasta(self):
		self.fasta = SeqIO.to_dict(SeqIO.parse('{0} Sequences.fasta'.format(self.handle), 'fasta'))

	def write_segment_fasta(self):
		accessions = self.df.groupby('Segment').get_group(segment)['Sequence Accession'].values

		if set(accessions).issubset(set(self.fasta.keys())):
			sequences = [record for accession, record in self.fasta.items() if accession in accessions]

			with open('split_fasta/{0} Segment {1}.fasta'.format(self.handle, segment), 'w+') as f:
				SeqIO.write(sequences, f, 'fasta')

		else:
			raise Exception("Not all requested accessions in original download.")


if __name__ == '__main__':
	handle = sys.argv[1]
	segment = int(sys.argv[2])

	p = SequenceSplitter(handle, segment)
	p.run()
