from sklearn.cluster import AffinityPropagation
import numpy as np
import pandas as pd
import sys


def compute_threshold(affmat):
    """
    This function uses affinity propagation to cluster the sequences, and then
    computes minimum of minimum in-cluster pairwise identities to be used as a
    threshold value.
    """
    ap = AffinityPropagation(affinity='precomputed')
    ap.fit(affmat)

    clusters = pd.DataFrame([i for i in zip(affmat.index, ap.labels_)])
    clusters = clusters.set_index(0)
    clusters.columns = ['Cluster']

    minval = 1
    for group in clusters.groupby('Cluster'):
        accessions = group[1].index
        subset = affmat[accessions].loc[accessions, :]

        if np.matrix(subset).min() < minval:
            minval = np.matrix(subset).min()

    return minval

if __name__ == '__main__':
    handle = sys.argv[1]

    segments = range(1, 9)
    threshold_values = []
    # segment_affmats = dict()
    for segment in segments:
        print('Currently on Segment {0}'.format(segment))
        print('Reading in affmat...')
        affmat = pd.read_hdf('{0} Segment Affmats.h5'.format(handle),
                             index_col=0, key='segment{0}'.format(segment))
        affmat.columns = affmat.index
        print('Thresholding affmat...')
        tv = compute_threshold(affmat)
        threshold_values.append((segment, tv))

    thresholds = pd.DataFrame(threshold_values).set_index(1)
    thresholds.to_csv('thresholds.csv', header=None)
