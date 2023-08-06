from __future__ import print_function

import champ
import modbp
import scipy.io as scio
import os
import igraph as ig
import louvain
from math import inf,ceil
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count
import numpy as np
import pickle
from time import time
GAMMA_END = 3.0
OMEGA_END = 3.0
NGAMMA = 5
NOMEGA = 5
PROGRESS_LENGTH = 50
optimiser = louvain.Optimiser()


def sorted_tuple(t):
    sort_map = {x[0]: i for i, x in enumerate(sorted(zip(*np.unique(t, return_index=True)), key=lambda x: x[1]))}
    return tuple(sort_map[x] for x in t)


def run_champ(G_intralayer, G_interlayer, layer_vec):
    intralayer_edges = [(e.source, e.target) for e in G_intralayer.es]
    interlayer_edges = [(e.source, e.target) for e in G_interlayer.es]
    MLPE = champ.louvain_ext.parallel_multilayer_louvain(intralayer_edges=intralayer_edges,
                                                         interlayer_edges=interlayer_edges,
                                                         layer_vec=layer_vec, gamma_range=[0, GAMMA_END],
                                                         ngamma=NGAMMA, omega_range=[0, OMEGA_END], nomega=NOMEGA,
                                                         numprocesses=4, maxpt=(GAMMA_END, OMEGA_END), progress=True)
    MLPE.plot_2d_modularity_domains()
    plt.show()
    return MLPE.partitions.tolist()


def one_run(G_intralayer, G_interlayer, layer_vec, gamma, omega):
    G_interlayer.es['weight'] = [omega] * G_interlayer.ecount()
    wl_part = louvain.RBConfigurationVertexPartitionWeightedLayers(G_intralayer, resolution_parameter=gamma,
                                                                   layer_vec=layer_vec, weights='weight')
    wli_part = louvain.CPMVertexPartition(G_interlayer, resolution_parameter=0.0, weights='weight')
    optimiser.optimise_partition_multiplex([wl_part, wli_part])
    return wl_part.membership


def repeated_multilayer_louvain(G_intralayer, G_interlayer, layer_vec, gammas, omegas, threads=cpu_count()):
    pool = Pool(processes=threads)
    start = time()
    partitions = [pool.apply_async(one_run, (G_intralayer, G_interlayer, layer_vec, g, o))
                  for g in gammas for o in omegas]

    total = len(partitions)
    iter_per_char = ceil(total / PROGRESS_LENGTH)
    start = time()

    def get_and_progress(i, p):
        res = p.get(timeout=600)
        i += 1
        print("\rLouvain Progress: [{}{}], Time: {:.1f} s / {:.1f} s"
              "".format("#" * (i // iter_per_char),
                        "-" * (total // iter_per_char - i // iter_per_char),
                        time() - start,
                        (time() - start) * (total / i)), end="", flush=True)
        return res

    partitions = [get_and_progress(i, p) for i, p in enumerate(partitions)]
    print()
    return partitions


def run_alternate(G_intralayer, G_interlayer, layer_vec):
    if 'weight' not in G_intralayer.es:
        G_intralayer.es['weight'] = [1.0] * G_intralayer.ecount()
    if 'weight' not in G_interlayer.es:
        G_interlayer.es['weight'] = [1.0] * G_interlayer.ecount()
    return repeated_multilayer_louvain(G_intralayer, G_interlayer, layer_vec,
                                       np.linspace(0, GAMMA_END, NGAMMA),
                                       np.linspace(0, OMEGA_END, NOMEGA))


def plot_alternate(G_intralayer, G_interlayer, layer_vec, partitions):
    if 'weight' not in G_intralayer.es:
        G_intralayer.es['weight'] = [1.0] * G_intralayer.ecount()
    if 'weight' not in G_interlayer.es:
        G_interlayer.es['weight'] = [1.0] * G_interlayer.ecount()

    def part_color(membership):
        membership_val = hash(sorted_tuple(membership))
        return tuple((membership_val / x) % 1.0 for x in [157244317, 183849443, 137530733])

    denser_gammas = np.linspace(0, GAMMA_END, 200)
    denser_omegas = np.linspace(0, OMEGA_END, 200)

    intralayer_part = louvain.RBConfigurationVertexPartitionWeightedLayers(G_intralayer, layer_vec=layer_vec,
                                                                           weights='weight')
    G_interlayer.es['weight'] = [1.0] * G_interlayer.ecount()
    interlayer_part = louvain.CPMVertexPartition(G_interlayer, resolution_parameter=0.0, weights='weight')

    total = len(partitions)
    iter_per_char = ceil(total / PROGRESS_LENGTH)
    current = 0
    start = time()

    # best_partitions = List(quality, partition, gamma, omega)
    best_partitions = [[(-inf,) * 4] * len(denser_omegas) for _ in range(len(denser_gammas))]
    for p in partitions:
        intralayer_part.set_membership(p)
        interlayer_part.set_membership(p)
        interlayer_base_quality = interlayer_part.quality()  # interlayer quality at omega=1.0
        for g_index, gamma in enumerate(denser_gammas):
            intralayer_quality = intralayer_part.quality(resolution_parameter=gamma)
            for o_index, omega in enumerate(denser_omegas):
                # omega * interlayer.quality() matches CPMVertexPartition.quality()
                # with omega as interlayer edge weights (as of 7/2)
                Q = intralayer_quality + omega * interlayer_base_quality
                if Q > best_partitions[g_index][o_index][0]:
                    best_partitions[g_index][o_index] = (Q, p, gamma, omega)

        current += 1
        print("\rSweep Progress: [{}{}], Time: {:.1f} s / {:.1f} s"
              "".format("#" * (current // iter_per_char),
                        "-" * (total // iter_per_char - current // iter_per_char),
                        time() - start,
                        (time() - start) * (total / current)), end="", flush=True)

    print("\nPlotting...", flush=True)

    gammas, omegas, colors = zip(*[(x[2], x[3], part_color(x[1])) for row in best_partitions for x in row])
    plt.scatter(gammas, omegas, color=colors, s=1, marker='s')
    plt.xlabel("gamma")
    plt.ylabel("omega")
    plt.show()

#Generate ML-SBM
# n = 200
# q = 2
# nlayers = 5
# nblocks = q
# c = 8
# ep = .1
# eta = .1
# pin = (n * c / (2.0)) / ((n / float(q)) * (n / float(q) - 1) / 2.0 * float(q) + ep * (q * (q - 1) / 2.0) * (np.power(n / (q * 1.0), 2.0)))
#
# pout = ep * pin
#
# prob_mat = np.identity(nblocks) * pin + (np.ones((nblocks, nblocks)) - np.identity(nblocks)) * pout
#
# ml_sbm = modbp.MultilayerSBM(n, comm_prob_mat=prob_mat, layers=nlayers, transition_prob=eta)
# mgraph = modbp.MultilayerGraph(intralayer_edges=ml_sbm.intraedges, interlayer_edges=ml_sbm.interedges,
#                                layer_vec=ml_sbm.layer_vec,
#                                comm_vec=ml_sbm.get_all_layers_block())
#
# G_intralayer, G_interlayer = champ.create_multilayer_igraph_from_edgelist(intralayer_edges=mgraph.intralayer_edges,interlayer_edges=mgraph.interlayer_edges,layer_vec=mgraph.layer_vec)

#SENATE DATA
senate_dir = '/Users/whweir/Documents/UNC_SOM_docs/Mucha_Lab/Mucha_Python/modularity_domains/multilayer_senate'
senate_data_file = os.path.join(senate_dir, 'multisenate0.5.mat')
sendata = scio.loadmat(senate_data_file)

A = sendata['A']
C = sendata['C']
sesid = sendata['Ssess'][:, 0]
parties = sendata['Sparty'][:, 0]
sessions = np.unique(sesid)
sess2layer = dict(zip(sessions, range(len(sessions))))
layer_vec = np.array(list(map(lambda x: sess2layer[x], sesid)))
G_intralayer,G_interlayer=champ.create_multilayer_igraph_from_adjacency(A=A,C=C,layer_vec=layer_vec)

# G_intralayer, G_interlayer = pickle.load(open("iter1.p", "rb"))
# layer_vec=mgraph.layer_vec
# n_per_layer = 150
# num_layers = 15
# layer_vec = [i // n_per_layer for i in range(n_per_layer * num_layers)]

print("\nCHAMP louvain:")
champ_partitions = run_champ(G_intralayer, G_interlayer, layer_vec)
print("\n'manual' louvain:")
partitions = run_alternate(G_intralayer, G_interlayer, layer_vec)

print("\n'manual' CHAMP (with CHAMP louvain):")
plot_alternate(G_intralayer, G_interlayer, layer_vec, champ_partitions)
print("\n'manual' CHAMP (with manual louvain):")
plot_alternate(G_intralayer, G_interlayer, layer_vec, partitions)