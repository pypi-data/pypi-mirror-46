import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import champ
import igraph as ig
import csv
from time import time
import re
from subprocess import PIPE,Popen

def run_SBMBP_on_graph(graph,q):
    hw2_data_dir="/Users/whweir/Documents/UNC_SOM_docs/MATH890_networks_course/notebooks/homework2/"

    sbmbpfile=os.path.join(hw2_data_dir,'mode_net/sbm')
    outdir='smb_outdir'
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    tmp_grph_file=os.path.join(outdir,'temporary_graph_file.gml')
    graph.save(tmp_grph_file)

    parameters=[
        sbmbpfile,'learn',
        "-l",tmp_grph_file, #graph file
        '-q','{:d}'.format(q),
        '-M','{:}_q{:d}_marginals.txt'.format(tmp_grph_file,q), #outfile
        '-d','1', #use degree corrected
        '-i','1' #initialize randomly
    ]
    process=Popen(parameters,stderr=PIPE,stdout=PIPE)
    stdout,stderr=process.communicate()
    if process.returncode!=0:
        raise RuntimeError("running SBMBP failed : {:}".format(stderr))

    #this is the file where the marginals are stored ( i.e what community is most
    # likely for each node)
    marginal_file='{:}_q{:d}_marginals.txt'.format(tmp_grph_file,q)
    marginals=[]
    partition=[]
    inmargs=False
    inpartition=False
    #file has custom format.  Somewhat crude parsingof it
    with open(marginal_file,'r') as f:

        for i,line in enumerate(f.readlines()):
            if re.search("\A\s*\Z",line): #only while space
                continue
            if i==0:
                fin_vals=dict([tuple(val.split('=')) for val in line.split()])
                for k,val in fin_vals.items():
                    fin_vals[k]=float(val)

            if re.search('argmax_marginals',line):
                inmargs=False
                inpartition=False
                continue
            elif re.search('marginals:',line):
                inmargs=True
                inpartition=False
                continue
            if re.search('argmax_configuration',line):
                inmargs=False
                inpartition=True
                continue

            if inmargs:
                marginals.append(line.split())
            if inpartition:
                partition=line.split()

    partition=np.array(partition,dtype=int)
    marginals=np.array(marginals,dtype=float)
    return marginals

def test_madoff_sbm():
    hw2_data_dir = "/Users/whweir/Documents/UNC_SOM_docs/MATH890_networks_course/notebooks/homework2/"
    madoff = os.path.join(hw2_data_dir, "data/madoff.graphml.gz")
    mygraph=ig.Graph.Read_GraphMLz(madoff)
    # marval_graph=os.path.join(hw2_data_dir,'marvel.graphml')
    # mygraph=ig.Graph.Read_GML(pol_blogs)
    # reader = csv.reader(open(madoff))
    # mygraph = ig.Graph.TupleList(reader)
    all_partitions = []
    for q in range(2, 5):
        t = time()
        for i in range(10):
            marg = run_SBMBP_on_graph(graph=mygraph, q=q)
            part = np.argmax(marg, axis=1)
            # each partition has to be in a dictionary of this form to add in
            all_partitions.append({'partition': part})
        print("q={:},time:{:.4f}".format(q, time() - t))

    sbm_part_ens = champ.PartitionEnsemble(graph=mygraph, maxpt=3)
    sbm_part_ens.add_partitions(partitions=all_partitions)
    print(len(sbm_part_ens.ind2doms))
    print("Champ set= {:d}/{:d}".format(len(sbm_part_ens.ind2doms.keys()), sbm_part_ens.numparts))
    print('end')

def run_SBMBP_on_graph(graph,q):
    hw2_data_dir="/Users/whweir/Documents/UNC_SOM_docs/MATH890_networks_course/notebooks/homework2/"
    sbmbpfile=os.path.join(hw2_data_dir,'mode_net/sbm')
    outdir=os.path.join(hw2_data_dir,'smb_outdir')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    tmp_grph_file=os.path.join(outdir,'temporary_graph_file.gml')
    graph.save(tmp_grph_file)

    parameters=[
        sbmbpfile,'learn',
        "-l",tmp_grph_file, #graph file
        '-q','{:d}'.format(q),
        '-M','{:}_q{:d}_marginals.txt'.format(tmp_grph_file,q), #outfile
        '-d','1', #use degree corrected
        '-i','1' #initialize randomly
    ]
    process=Popen(parameters,stderr=PIPE,stdout=PIPE)
    stdout,stderr=process.communicate()
    if process.returncode!=0:
        raise RuntimeError("running SBMBP failed : {:}".format(stderr))

    #this is the file where the marginals are stored ( i.e what community is most
    # likely for each node)
    marginal_file='{:}_q{:d}_marginals.txt'.format(tmp_grph_file,q)
    marginals=[]
    partition=[]
    inmargs=False
    inpartition=False
    #file has custom format.  Somewhat crude parsingof it
    with open(marginal_file,'r') as f:

        for i,line in enumerate(f.readlines()):
            if re.search("\A\s*\Z",line): #only while space
                continue
            if i==0:
                fin_vals=dict([tuple(val.split('=')) for val in line.split()])
                for k,val in fin_vals.items():
                    fin_vals[k]=float(val)

            if re.search('argmax_marginals',line):
                inmargs=False
                inpartition=False
                continue
            elif re.search('marginals:',line):
                inmargs=True
                inpartition=False
                continue
            if re.search('argmax_configuration',line):
                inmargs=False
                inpartition=True
                continue

            if inmargs:
                marginals.append(line.split())
            if inpartition:
                partition=line.split()

    partition=np.array(partition,dtype=int)
    marginals=np.array(marginals,dtype=float)
    return marginals

def test_windows_louvain():


    np.random.seed(0)
    test_graph = ig.Graph.Erdos_Renyi(n=1000, p=.1)
    ens = champ.parallel_louvain(test_graph, numprocesses=20, numruns=20, start=0, fin=4, maxpt=4, progress=True)
    t = time()



def test_directed_louvain():
    hw2_data_dir="/Users/whweir/Documents/UNC_SOM_docs/MATH890_networks_course/notebooks/homework2/data"
    pol_blogs = os.path.join(hw2_data_dir,"polblogs/polblogs.gml")
    # marval_graph=os.path.join(hw2_data_dir,'marvel.graphml')
    mygraph=ig.Graph.Read_GML(pol_blogs)
    # mygraph=ig.Graph.Read_GraphML(marval_graph)
    # mygraph.to_undirected()
    print("num nodes",mygraph.vcount())
    print("num edges",mygraph.ecount())
    print('node attributes',mygraph.vs.attributes())
    print('edge attributes',mygraph.es.attributes())
    part_ens = champ.parallel_louvain(graph=mygraph, start=0, fin=2, numruns=5, numprocesses=1)
    print("Champ set= {:d}/{:d}".format(len(part_ens.ind2doms.keys()), part_ens.numparts))
    # part_ens.save(os.path.join(hw2_data_dir,"my_part_ens.hdf5"))

    # all_partitions = []
    # for q in range(2, 3):
    #     t = time()
    #     for i in range(2):
    #         marg = run_SBMBP_on_graph(graph=mygraph, q=q)
    #         part = np.argmax(marg, axis=1)
    #         # each partition has to be in a dictionary of this form to add in
    #         all_partitions.append({'partition': part})
    #     print("q={:},time:{:.4f}".format(q, time() - t))
    #
    # sbm_part_ens = champ.PartitionEnsemble(graph=mygraph, maxpt=3)
    # sbm_part_ens.add_partitions(partitions=all_partitions)
    # sbm_part_ens.save(os.path.join(hw2_data_dir,"sbm_part_ens.hdf5"))
    #
    # new_part=champ.PartitionEnsemble()
    # new_part.open(os.path.join(hw2_data_dir,"sbm_part_ens.hdf5"))


    print('here')
def main():
    test_madoff_sbm()
    return 0


if __name__=='__main__':
    sys.exit(main())