import numpy as np
from itertools import combinations
import itertools
from skbio.stats.ordination import pcoa
from skbio import DistanceMatrix
import matplotlib.pyplot as plt
import pandas as pd
import biom
import skbio
from q2_types.feature_table import FeatureTable, Frequency
from scipy.spatial.distance import squareform
import pickle

def cscs(features: biom.Table, css_edges: str, cosine_threshold: float= 0.6, normalization: bool = True)-> skbio.DistanceMatrix:
    edges = pd.read_csv(css_edges, sep ="\t")
    css = pair_to_dist(edges,cosine_threshold = cosine_threshold)
    featuresm = features.matrix_data
    data = [pd.SparseSeries(featuresm[i].toarray().ravel()) for i in np.arange(featuresm.shape[0])]
    featurespd = pd.SparseDataFrame(data, index=features.ids('observation'),
                             columns=features.ids('sample'))
    featurespd.insert(loc=0, column='#OTU ID', value= featurespd.index)
    featurespd['#OTU ID'] = pd.to_numeric(featurespd['#OTU ID'])
    featurespd.index = range(len(featurespd))
    featurespd = featurespd.loc[featurespd['#OTU ID'].argsort()]
    cscs = similarity2dissimilarity(make_dm_symmetric(make_distance_matrix(featurespd, css, weighted=True, normalization = normalization)))
    return(skbio.DistanceMatrix(cscs, ids = cscs.index))

def pair_to_dist(edges,cosine_threshold):
    edges.loc[edges['Cosine']<cosine_threshold,'Cosine'] = 0
    n = sorted(list(pd.unique(edges[['CLUSTERID1','CLUSTERID2']].values.ravel('K'))))
    d = pd.DataFrame(0, index=n, columns=n)
    
    for index, row in edges.iterrows():
        d.loc[row['CLUSTERID1'],row['CLUSTERID2']] = row['Cosine']
        d.loc[row['CLUSTERID2'],row['CLUSTERID1']] = row['Cosine']
    
    return d

def single_distance(index, spn, sample_names, features, css):
    # Get sample names to be compared
    name_i = spn[index, 0]
    name_j = spn[index, 1]

    # Get their indices
    i = int(np.where(sample_names == name_i)[0])
    j = int(np.where(sample_names == name_j)[0])

    feature_union = np.where(features[:, [i, j]].sum(axis=1) > 0)[0]

    css_tmp = css[feature_union[:, None], feature_union]

    a = features[feature_union, i]
    b = features[feature_union, j]

    abt = np.matrix(a).T * np.matrix(b)
    aat = np.matrix(a).T * np.matrix(a)
    bbt = np.matrix(b).T * np.matrix(b)

    cssAB = np.multiply(css_tmp, abt)

    d = np.sum(cssAB) / np.max([np.sum(np.multiply(css_tmp, aat)),
                                np.sum(np.multiply(css_tmp, bbt))])

    return d


def calc_distances(features, css, sample_names):
    assert css.shape[0] == features.shape[0]
    np.fill_diagonal(css.get_values(), 1)
    css = np.matrix(css.get_values())
    spn = np.array(list(combinations(sample_names, 2)))

    distlist = []
    for I in range(spn.shape[0]):
        distlist.append(
            single_distance(index=I, spn=spn, sample_names=sample_names,
                            features=features.get_values()[:, 1:], css=css))

    return distlist

def make_distance_matrix(features_orig, css, weighted=True, cosine_threshold = 0.5, normalization = True):
    features = features_orig.copy()
    sample_names = features.columns[1:].values
    
    if normalization == True:
        colSums = features.iloc[:,1:].sum(axis=0)
        norm = features.iloc[:,1:].div(colSums)
        features.update(norm)
        #print(features)

    if not weighted:
        # Convert to absence/presence
        pd.options.mode.chained_assignment = None
        subset = features.loc[:, features.columns[1:]]
        subset[subset.loc[:, :] > 0] = 1
        features.loc[:, features.columns[1:]] = subset

    dist_list = calc_distances(features, css, sample_names)

    matrix = np.zeros([len(sample_names), len(sample_names)])
    value_index = -1
    for j in range(len(sample_names)):
        for i in range(len(sample_names)):
            if i > j:
                value_index += 1
                matrix[i, j] = dist_list[value_index]
    return pd.DataFrame(data=matrix, index=sample_names, columns=sample_names)


def make_dm_symmetric(matrix_orig):
    matrix = matrix_orig.copy().get_values()
    sym_matrix = matrix_orig.copy()
    sample_names = sym_matrix.columns.tolist()
    sym_matrix = sym_matrix.get_values()
    n = sym_matrix.shape[0]
    for j in range(n):
        for i in range(n):
            if i > j:
                sym_matrix[j, i] = matrix[i, j]

    assert (sym_matrix == sym_matrix.T).all()

    return pd.DataFrame(sym_matrix, sample_names, sample_names)

def similarity2dissimilarity(input_df):
    ones = np.ones(input_df.shape)
    new_values = np.array(ones - input_df)
    np.fill_diagonal(new_values, 0)
    out_df = pd.DataFrame(new_values, input_df.columns, input_df.index)

    return out_df
