import numpy as np
from itertools import combinations,islice
from skbio.stats.ordination import pcoa
from skbio import DistanceMatrix
from scipy.sparse import dok_matrix
import skbio
import pandas as pd
import biom
from q2_types.feature_table import FeatureTable, Frequency
from scipy.spatial.distance import squareform
import pickle
from multiprocessing import Process, Queue 
from collections import defaultdict
import itertools

def cscs(features: biom.Table, css_edges: str, cosine_threshold: float= 0.6, normalization: bool = True, weighted: bool = True)-> skbio.DistanceMatrix:
    observationids = {x:index for index, x in enumerate(features.ids(axis='observation'))}
    edgesdok = dok_matrix((features.shape[0], features.shape[0]), dtype=np.float32)
    for line in open(css_edges, "r"):
        if line.find("CLUSTERID1") > -1:
            continue
        linesplit = line.split("\t")
        if float(linesplit[4]) < cosine_threshold:
            edgesdok[observationids[linesplit[0]], observationids[linesplit[1]]] = 0.0
        else:
            edgesdok[observationids[linesplit[0]], observationids[linesplit[1]]] = float(linesplit[4])
        edgesdok.setdiag(1)

    if normalization:
        features = features.norm(axis='sample', inplace=False)
    if weighted == False:
        features = features.pa #TODO: make new option in cscs()

    sample_names = features.ids()
    cscs = parallel_make_distance_matrix(features, edgesdok,  sample_names)
    cscs = 1 - cscs 
    print(cscs)
    return(skbio.DistanceMatrix(cscs, ids = cscs.index))

def compute_sum(sampleA, sampleB, edges):
    outer = sampleA.multiply(sampleB.transpose())
    finaldok = outer.multiply(edges)
    if finaldok.nnz == 0:
        return(0)
    else:
        return(finaldok.data[0])

def single_distance(sampleA, sampleB, edges):
    """ Compute the distance between one pair of samples
    """
    cssab = compute_sum(sampleA, sampleB, edges)
    cssaa = compute_sum(sampleA, sampleA, edges)
    cssbb = compute_sum(sampleB, sampleB, edges)
    return(cssab/max(cssaa, cssbb))

def worker(input, output, edges):
    for worker_samples in iter(input.get, "STOP"):
        
        #print(worker_samples)
        results=[]
        for index, sampleA, sampleB in worker_samples:
            results.append((index, single_distance(sampleA, sampleB, edges)))
        output.put([(index, result) for index, result in results])

def split_every(n, iterable):
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

def parallel_make_distance_matrix(features, edges,  sample_names):
    #Parallel stuff
    NUMBER_OF_PROCESSES = 8
    work_chunk_size = 5
    
    # Create queues
    task_queue = Queue()
    done_queue = Queue()
    
    #Scientific stuff
    dist =  np.zeros([features.shape[1], features.shape[1]])
    
    feature_combinations = itertools.combinations(range(0,features.shape[1]), 2)
    comb_chunks_list = list([chunk for chunk in split_every(work_chunk_size, feature_combinations)])
    for chunk_index, chunk_comb in enumerate(comb_chunks_list):
        task_queue.put([(chunk_index*work_chunk_size + comb_index, features[:,comb[0]], features[:,comb[1]]) for comb_index, comb in enumerate(chunk_comb)])
        
    # Start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue, edges)).start()
        
    indexed_distances = []
    for i in range(len(comb_chunks_list)):
        indexed_distances.extend(done_queue.get())
        
    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')
        
    distances = list([d for i, d in sorted(indexed_distances, key=lambda id_tuple: id_tuple[0])])
    
    xs,ys = np.triu_indices(dist.shape[0],k=1)
    dist[xs,ys] = distances
    dist[ys,xs] = distances
    dist[ np.diag_indices(dist.shape[0]) ] = 1
    distdf = pd.DataFrame(dist, sample_names, sample_names)
    return(distdf)
