import tables as tb 
import pandas as pd 
import sys

class AffmatCleaner(object):
    """docstring for AffmatCleaner"""
    

    def __init__(self, handle, segment):
        super(AffmatCleaner, self).__init__()
        self.handle = handle
        self.accession_strains = None
        self.segment = segment
        self.distmat = None
        self.affmat = None

    def run(self):
        self.compile_accessions_strains()
        # for segment in range(1,9):
        print('Segment: {0}'.format(self.segment))

        print('Cleaning distmat...')
        self.clean_distmat()

        print('Reading Distmat...')
        self.read_distmat()

        print('Saving affmat...')
        self.save_affmat()

        print('Removing intermediate distmat...')
        self.remove_intermediate_distmat()

    def compile_accessions_strains(self):
        """
        Sets the accession_strains dictionary such that keys are accessions, 
        and values are strain names.
        """

        df = pd.read_csv('{0} Full Isolates.csv'.format(self.handle), index_col=0, parse_dates=['Collection Date'])
        self.accession_strains = dict(zip(df['Sequence Accession'], df['Strain Name']))
        # self.accession_strains.set_index('Sequence Accession', inplace=True)

    def clean_distmat(self):
        """
        Replaces accession numbers with strain names.
        Removes any double spaces (which are detected as double commas)
        """
        oldname = 'distmats/{0} Segment {1} Distmat.txt'.format(self.handle, self.segment)
        newname = 'distmats/{0} Segment {1} Distmat Renamed.txt'.format(self.handle, self.segment)
        with open(oldname, 'rb') as oldf:
            with open(newname, 'w+') as newf:
                for line in oldf.readlines():
                    line = line.decode('utf-8')
                    if len(line.split(' ')) == 1:
                        newf.write(str(line))
                    else:
                        newline = line.replace(' ', ',')
                        while ',,' in newline:
                            newline = newline.replace(',,', ',')
                        accession = newline.split(',')[0]
                        # Replace accession number with strain name
                        newline = newline.replace(accession, self.accession_strains[accession])
                        newf.write(str(newline))


    def read_distmat(self):
        """
        Reads the distmat into memory.
        """
        self.distmat = pd.read_csv('distmats/{0} Segment {1} Distmat Renamed.txt'.format(self.handle, self.segment), index_col=0, delimiter=',', skiprows=1, header=None)
        self.distmat.columns = self.distmat.index

    def save_affmat(self):
        """
        Saves the affmat to an HDF5 store.
        """
        self.affmat = (1 - self.distmat)
        self.affmat.to_hdf('{0} Segment Affmats.h5'.format(self.handle), mode='a', key='segment{0}'.format(self.segment))

    def remove_intermediate_distmat(self):
        import os
        os.remove('distmats/{0} Segment {1} Distmat Renamed.txt'.format(self.handle, self.segment))



if __name__ == '__main__':

    handle = sys.argv[1]
    segment = int(sys.argv[2])

    ac = AffmatCleaner(handle, segment)
    ac.run()





