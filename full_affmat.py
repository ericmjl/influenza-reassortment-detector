import pandas as pd
import sys

class FullAffmatCompiler(object):
    """docstring for FullAffmatCompiler"""
    def __init__(self, handle):
        super(FullAffmatCompiler, self).__init__()
        self.handle = handle
        self.summed_affmat = pd.DataFrame()
        self.current_df = None
        self.affmats = dict()

    def run(self):
        for segment in range(1,9):
            print('Currently processing segment {0}'.format(segment))
            self.affmats[segment] = self.read_affmat(segment)

        self.summed_affmat = self.affmats[1] + self.affmats[2] + self.affmats[3] + self.affmats[4] + self.affmats[5] + self.affmats[6] + self.affmats[7] + self.affmats[8]

        self.summed_affmat.to_hdf(path_or_buf='{0} Summed Affmats.h5'.format(self.handle), key='full', mode='w')

    def read_affmat(self, segment):
        key = 'segment{0}'.format(segment)
        return pd.read_hdf('{0} Thresholded Segment Affmats.h5'.format(self.handle), key=key)

if __name__ == '__main__':
    handle = sys.argv[1]

    fac = FullAffmatCompiler(handle)
    fac.run()