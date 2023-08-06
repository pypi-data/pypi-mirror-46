import numpy as np

def genlouvain(B,limit=10000,verbose=False,randord=True,randmove=True):
    n=B.shape[0]
    if len(np.nonzero(B-B.transpose())[0])>0:
        raise AssertionError("B must be a symmetric matrix")
    S0=np.range(n)

    M=B # The modularity matrix


