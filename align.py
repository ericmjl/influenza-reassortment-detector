"""
This script runs a multiple sequence alignment of the nucleotide sequences.
"""
import os
import sys
from Bio.Align.Applications import ClustalOmegaCommandline

class Aligner(object):
	"""docstring for Aligner"""
	def __init__(self, handle, segment):
		super(Aligner, self).__init__()
		self.handle = handle
		self.segment = segment

	def run(self):
		self.align()
		print('Alignment of Segment {0} complete.'.format(self.segment))

	def align(self):
		infile = 'split_fasta/{0} Segment {1}.fasta'.format(self.handle, self.segment)
		outfile = 'alignments/{0} Segment {1} Aligned.fasta'.format(self.handle, self.segment)
		distmat = 'distmats/{0} Segment {1} Distmat.txt'.format(self.handle, self.segment)
		cline = ClustalOmegaCommandline(infile=infile, 
										outfile=outfile, 
										distmat_out=distmat, 
										distmat_full=True,
										max_hmm_iterations=1,
										verbose=True,
										force=True)
		cline()



if __name__ == '__main__':
	
	handle = sys.argv[1]
	segment = int(sys.argv[2])

	a = Aligner(handle, segment)
	a.run()