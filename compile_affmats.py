import tables as tb 
import pandas as pd 
import sys
import os


class AffmatCompiler(object):
    """

    """
    

    def __init__(self, handle):
        super(AffmatCompiler, self).__init__()
        self.handle = handle
        self.thresholds = None

    def run(self):
        print('Reading thresholds...')
        self.read_thresholds()
        
        for segment in range(1,9):
            print('Segment: {0}'.format(segment))

            print('Reading affmat...')
            self.read_affmat(segment)

            print('Thresholding and saving affmat...')
            self.save_affmat(segment)

    def read_thresholds(self):
        self.thresholds = pd.read_csv('thresholds.csv', header=None)
        self.thresholds = dict(zip(self.thresholds[0], self.thresholds[1]))

    def read_affmat(self, segment):
        """
        Reads the segment affmat into memory.
        """
        self.affmat = pd.read_hdf('{0} Segment Affmats.h5'.format(self.handle), index_col=0, key='segment{0}'.format(segment))
        self.affmat.columns = self.affmat.index

    def save_affmat(self, segment):
        """
        Thresholds the particular segment affmat. Then appends it to the HDF5
        store on disk.

        Saves the affmat to an HDF5 store.
        """

        threshold_value = self.thresholds[segment]
        self.affmat = self.affmat[self.affmat > threshold_value]

        self.affmat.to_hdf('{0} Thresholded Segment Affmats.h5'.format(self.handle), mode='a', key='segment{0}'.format(segment))

    def remove_intermediate_distmat(self, segment):
        os.remove('distmats/{0} Segment {1} Distmat Renamed.txt'.format(self.handle, segment))



if __name__ == '__main__':

    handle = sys.argv[1]

    ac = AffmatCompiler(handle)
    ac.run()





