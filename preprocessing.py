"""
This script performs data preprocessing.
"""

import pandas as pd
import sys

from Bio import SeqIO

class Preprocessor(object):
    """docstring for Preprocessor"""
    def __init__(self, handle):
        super(Preprocessor, self).__init__()
        self.handle = handle
        self.df = None
        self.fasta = None

        # Curate a list of strain names to exclude from the analysis.
        self.strain_name_exclusions = ['little yellow-shouldered bat']

    def run(self):

        self.read_dataframe()
        self.clean_strain_names()
        self.remove_excluded_strains()
        self.remove_isolates_with_bad_names()
        self.clean_host_species()
        self.impute_location()
        self.remove_low_quality_accessions()
        self.impute_dates()
        self.get_complete_genome_isolates()
        self.save_full_isolates()

    def remove_excluded_strains(self):
        for name in self.strain_name_exclusions:
            self.df = self.df[self.df['Strain Name'].str.contains(name) == False]

    def remove_isolates_with_bad_names(self):
        print('Removing isolates with bad names...')
        allowed_lengths = [4, 5]
        names_to_drop = set()
        for row, data in self.df.iterrows():
            strain_name = data['Strain Name'].split('/')

            if len(strain_name) not in allowed_lengths:
                names_to_drop.add(data['Strain Name'])

        for name in names_to_drop:
            self.df = self.df[self.df['Strain Name'] != name]

        print('Isolates with bad names removed.')


    def read_dataframe(self):
        """
        Reads the CSV file containing the data into memory.
        """
        print('Reading DataFrame into memory...')
        self.df = pd.read_csv('{0} Sequences.csv'.format(self.handle), parse_dates=['Collection Date'], na_filter=False)
        print('DataFrame read into memory.')

    def read_fasta(self):
        print('Reading FASTA file into memory...')
        self.fasta = SeqIO.to_dict(SeqIO.parse('{0} Sequences.fasta'.format(self.handle), 'fasta'))
        print('FASTA file read into memory.')

    def clean_strain_names(self):
        """
        This function removes parentheses from the strain names, leaving only
        the strain name without any other info.
        """
        print('Cleaning strain names...')
        self.df['Strain Name'] = self.df['Strain Name'].str.replace("\\", "/")
        self.df['Strain Name'] = self.df['Strain Name'].str.split("(").apply(lambda x: max(x, key=len))
        print('Strain names cleaned.')

    def clean_host_species(self):
        """
        Host species are usually stored as IRD:hostname. 
        """
        print('Cleaning host species names...')
        self.df['Host Species'] = self.df['Host Species'].str.split(':').str[-1]
        print('Host species names cleaned.')

    def impute_location(self):
        print('Imputing location data...')
        self.df['State/Province'] = self.df['Strain Name'].str.split("/").apply(lambda x: x[1] if len(x) == 4 else x[2])
        print('Location imputed.')

    def impute_dates(self):
        print('Imputing collection date data...')
        self.df['Collection Date'] = pd.to_datetime(self.df['Collection Date'])
        print('Collection dates imputed.')

    def remove_low_quality_accessions(self):
        print('Removing low quality accessions...')
        self.df = self.df[self.df['Sequence Accession'].str.contains('\*') == False]
        print('Low quality accessions removed.')

    def get_complete_genome_isolates(self):
        print('Filtering to completed genomes only...')
        rows_to_drop = []

        for name, df in self.df.groupby('Strain Name'):
            if len(df) == 8 and set(df['Segment'].values) == set(range(1,9)):
                pass
            else:
                rows_to_drop.extend(df.index)

        self.df = self.df.drop(rows_to_drop)

        print('Filtering complete.')

    def save_full_isolates(self):
        print('Saving data table comprising only isolates with full genomes...')
        self.df.to_csv('{0} Full Isolates.csv'.format(self.handle))
        print('Full genome isolates saved.')


    def write_segment_fasta(self, segnum):
        print('Writing segment FASTA files...')
        accessions = self.df.groupby('Segment').get_group(segnum)['Sequence Accession'].values

        if set(accessions).issubset(set(self.fasta.keys())):
            sequences = [record for accession, record in self.fasta.items() if accession in accessions]

            with open('{0} Segment {1}.fasta'.format(self.handle, segnum), 'w+') as f:
                SeqIO.write(sequences, f, 'fasta')

        else:
            raise Exception("Not all requested accessions in original download.")

        print('Segment FASTA files written.')

if __name__ == '__main__':
    handle = sys.argv[1]

    p = Preprocessor(handle)
    p.run()
